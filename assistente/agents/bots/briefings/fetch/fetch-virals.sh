#!/bin/bash
# fetch-virals.sh - Virais por fonte (HN + YouTube + Reddit + Twitter + Google News)
# Reddit via RSS, HN API pública, Twitter via API/RSSHub.
# Cache: 6h | Output: /tmp/virals.json

set -e

CACHE_FILE="/tmp/virals.json"
LAST_GOOD_FILE="/tmp/virals_last_good.json"
CACHE_TTL=21600  # 6h

# Check cache
if [ -f "$CACHE_FILE" ]; then
  cache_age=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0)))
  if [ $cache_age -lt $CACHE_TTL ]; then
    echo "Using cached virals ($(($cache_age/3600))h old)..." >&2
    cat "$CACHE_FILE"
    exit 0
  fi
fi

echo "Fetching virals (HN + YouTube + Reddit + Twitter + Google News)..." >&2

if [ -f ~/.config/secrets.env ]; then
  set -a; . ~/.config/secrets.env; set +a
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RSS_PARSER="$SCRIPT_DIR/parse_rss.py"
PYTHON_BIN="${PYTHON_BIN:-python3}"

YOUTUBE_KEY="${YOUTUBE_API_KEY:-}"
YT_MIN_VIEWS="${YT_MIN_VIEWS:-50000}"
YT_LIMIT="${YT_LIMIT:-5}"
YT_MAX_AGE_HOURS="${YT_MAX_AGE_HOURS:-24}"
YT_REGION_BR="${YT_REGION_BR:-BR}"
YT_REGION_WORLD="${YT_REGION_WORLD:-US}"
YT_LANG_BR="${YT_LANG_BR:-pt}"
YT_LANG_WORLD="${YT_LANG_WORLD:-en}"
REDDIT_MODE="${REDDIT_MODE:-rss}"
REDDIT_LIMIT="${REDDIT_LIMIT:-5}"
REDDIT_USER_AGENT="${REDDIT_USER_AGENT:-briefings-bot/1.0}"
REDDIT_MAX_AGE_HOURS="${REDDIT_MAX_AGE_HOURS:-24}"
NEWS_MODE="${NEWS_MODE:-rss}"
NEWS_LIMIT="${NEWS_LIMIT:-5}"
NEWS_EDU_EXTRA_LIMIT="${NEWS_EDU_EXTRA_LIMIT:-1}"
NEWS_MAX_AGE_HOURS="${NEWS_MAX_AGE_HOURS:-24}"
NEWS_USER_AGENT="${NEWS_USER_AGENT:-briefings-bot/1.0}"
TWITTER_MODE="${TWITTER_MODE:-off}"
TWITTER_LIMIT="${TWITTER_LIMIT:-5}"
TWITTER_USER_AGENT="${TWITTER_USER_AGENT:-briefings-bot/1.0}"
TWITTER_RSSHUB_HOSTS="${TWITTER_RSSHUB_HOSTS:-rsshub.app rsshub.in rsshub.rssforever.com rsshub.io rsshub.wizbox.top}"
TWITTER_BEARER_TOKEN="${TWITTER_BEARER_TOKEN:-}"
TWITTER_ENV_FILE="${TWITTER_ENV_FILE:-/home/ubuntu/clawd/sessions/personajes/.env}"
TWITTER_PYTHON_BIN="${TWITTER_PYTHON_BIN:-}"
TWITTER_MIN_SCORE="${TWITTER_MIN_SCORE:-100}"
TWITTER_LANGS="${TWITTER_LANGS:-pt,en}"
TWITTER_MAX_AGE_HOURS="${TWITTER_MAX_AGE_HOURS:-24}"

curl_file() {
  local url="$1"
  local out="$2"
  curl -s -L --max-time 12 --retry 2 --retry-connrefused --retry-all-errors --retry-delay 1 \
    -o "$out" "$url" 2>/dev/null || true
}

curl_text() {
  local url="$1"
  local ua="$2"
  curl -s -L --max-time 12 --retry 2 --retry-connrefused --retry-all-errors --retry-delay 1 \
    -H "User-Agent: $ua" "$url" 2>/dev/null || true
}

curl_text_doh() {
  local url="$1"
  local ua="$2"
  local host
  host=$(echo "$url" | sed -E 's#^[a-z]+://([^/]+).*#\1#' | cut -d: -f1)
  [ -z "$host" ] && return 0
  local ip
  ip=$(curl -s --max-time 6 -H 'accept: application/dns-json' \
    "https://1.1.1.1/dns-query?name=$host&type=A" | \
    jq -r '.Answer[]? | select(.type==1) | .data' 2>/dev/null | head -n 1)
  [ -z "$ip" ] && return 0
  curl -s -L --max-time 12 --resolve "$host:443:$ip" \
    -H "Host: $host" -H "User-Agent: $ua" "$url" 2>/dev/null || true
}

# ═══════════════════════════════════════════════════════════
# HACKER NEWS (API pública, sem rate limit agressivo)
# ═══════════════════════════════════════════════════════════

echo "  Hacker News..." >&2

# Fetch top 200 story IDs
hn_top_tmp=$(mktemp /tmp/hn_top_XXXX.json)
hn_best_tmp=$(mktemp /tmp/hn_best_XXXX.json)
curl_file "https://hacker-news.firebaseio.com/v0/topstories.json" "$hn_top_tmp"
curl_file "https://hacker-news.firebaseio.com/v0/beststories.json" "$hn_best_tmp"
if [ ! -s "$hn_top_tmp" ]; then
  curl_file "https://hacker-news.firebaseio.com/v0/topstories.json" "$hn_top_tmp"
fi
if [ ! -s "$hn_best_tmp" ]; then
  curl_file "https://hacker-news.firebaseio.com/v0/beststories.json" "$hn_best_tmp"
fi
top_ids=$(jq '.[0:200]' "$hn_top_tmp" 2>/dev/null || echo '[]')
best_ids=$(jq '.[0:100]' "$hn_best_tmp" 2>/dev/null || echo '[]')
rm -f "$hn_top_tmp" "$hn_best_tmp"

# Combine and dedupe
all_ids=$(echo "$top_ids $best_ids" | jq -s 'add | unique | .[0:250]' 2>/dev/null || echo '[]')

# Fetch story details (batch of 100 for better coverage)
stories='[]'
for id in $(echo "$all_ids" | jq -r '.[:100][]' 2>/dev/null); do
  item=$(curl -s "https://hacker-news.firebaseio.com/v0/item/$id.json" 2>/dev/null)
  if [ -n "$item" ] && [ "$item" != "null" ]; then
    stories=$(echo "$stories" | jq --argjson item "$item" '. + [$item]')
  fi
done

# Filter function: search title for keywords (case insensitive)
filter_hn() {
  local keywords="$1"
  echo "$stories" | jq --arg kw "$keywords" '
    [.[] | select(.title != null and .score != null) |
     select(.title | ascii_downcase | test($kw; "i"))] |
     sort_by(-.score) | .[0:3] |
     [.[] | {
       title: .title[0:80],
       score,
       source: "Hacker News",
       published: (.time | todateiso8601),
       url: ("https://news.ycombinator.com/item?id=" + (.id|tostring))
     }]
  '
}

# 1. Carreira (Career) - broad tech career terms
hn_carreira=$(filter_hn "career|job|hiring|interview|salary|layoff|resign|quit|work|startup|founder|ceo|manager")

# 2. Internacionalização (International)
hn_intl=$(filter_hn "relocat|visa|immigra|abroad|international|expat|moving|country|europe|asia|canada|australia")

# 3. Estudar fora (Study abroad / Academia / Research)
hn_estudar=$(filter_hn "university|college|scholarship|phd|masters|graduat|student|degree|research|academic|paper|science|stanford|mit|harvard|berkeley")

# 4. Educação (Education) - broad learning terms
hn_edu=$(filter_hn "learn|education|course|training|teach|bootcamp|mooc|lesson|book|reading|study")

# 5. Trabalho remoto (Remote work)
hn_remoto=$(filter_hn "remote|wfh|work from home|distributed|async|nomad|hybrid|office|commut|freelanc")

# 6. Inglês (English/Communication/Writing)
hn_ingles=$(filter_hn "language|english|communicat|writing|speak|grammar|blog|document|read")

# 7. Skills (Tech skills - most HN content)
hn_skills=$(filter_hn "programming|skill|tutorial|coding|developer|engineer|tech|code|build|project|tool|software")

# ═══════════════════════════════════════════════════════════
# YOUTUBE (se disponível e quota OK)
# ═══════════════════════════════════════════════════════════

echo "  YouTube..." >&2

url_encode() {
  "$PYTHON_BIN" - <<'PY' "$1"
import sys, urllib.parse
print(urllib.parse.quote(sys.argv[1]))
PY
}

yt_published_after() {
  "$PYTHON_BIN" - <<'PY'
from datetime import datetime, timedelta, timezone
import os
hours = int(os.environ.get("YT_MAX_AGE_HOURS", "24") or "24")
ts = datetime.now(timezone.utc) - timedelta(hours=hours)
print(ts.isoformat().replace("+00:00", "Z"))
PY
}

fetch_yt() {
  local query="$1"
  local region="$2"
  local lang="$3"
  [ -z "$YOUTUBE_KEY" ] && { echo '[]'; return; }
  local enc
  enc=$(url_encode "$query")
  local published_after
  published_after=$(yt_published_after)
  local url="https://www.googleapis.com/youtube/v3/search?part=snippet&q=$enc&order=viewCount&type=video&maxResults=$YT_LIMIT&publishedAfter=$published_after&key=$YOUTUBE_KEY"
  [ -n "$region" ] && url="${url}&regionCode=$region"
  [ -n "$lang" ] && url="${url}&relevanceLanguage=$lang"
  resp=$(curl -4 -s --max-time 8 --retry 2 --retry-connrefused --retry-all-errors --retry-delay 1 \
    "$url" 2>/dev/null || true)
  
  # Check quota exceeded
  if echo "$resp" | jq -e '.error.errors[0].reason == "quotaExceeded"' >/dev/null 2>&1; then
    echo '[]'
    return
  fi
  
  ids=$(echo "$resp" | jq -r '.items[]?.id.videoId' 2>/dev/null | paste -sd, -)
  [ -z "$ids" ] && { echo '[]'; return; }
  stats=$(curl -4 -s --max-time 8 --retry 2 --retry-connrefused --retry-all-errors --retry-delay 1 \
    "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=$ids&key=$YOUTUBE_KEY" 2>/dev/null || true)
  echo "$stats" | jq --argjson min_views "$YT_MIN_VIEWS" --argjson limit "$YT_LIMIT" --arg region "$region" --arg lang "$lang" '
    [.items[]? | {
      title: .snippet.title[0:80],
      channel: .snippet.channelTitle,
      views: (.statistics.viewCount | tonumber? // 0),
      url: ("https://www.youtube.com/watch?v=" + .id),
      region: $region,
      lang: $lang
    } | select(.views >= $min_views)] | .[0:$limit]
  ' 2>/dev/null || echo '[]'
}

yt_carreira_br=$(fetch_yt "carreira emprego entrevista salário" "$YT_REGION_BR" "$YT_LANG_BR")
yt_carreira_world=$(fetch_yt "career advice interview salary" "$YT_REGION_WORLD" "$YT_LANG_WORLD")
yt_intl_br=$(fetch_yt "trabalhar no exterior visto intercâmbio" "$YT_REGION_BR" "$YT_LANG_BR")
yt_intl_world=$(fetch_yt "work abroad relocation visa international career" "$YT_REGION_WORLD" "$YT_LANG_WORLD")
yt_estudar_br=$(fetch_yt "estudar fora bolsa universidade" "$YT_REGION_BR" "$YT_LANG_BR")
yt_estudar_world=$(fetch_yt "study abroad scholarship university masters phd" "$YT_REGION_WORLD" "$YT_LANG_WORLD")
yt_edu_br=$(fetch_yt "educação curso online ensino" "$YT_REGION_BR" "$YT_LANG_BR")
yt_edu_world=$(fetch_yt "education course training bootcamp learn" "$YT_REGION_WORLD" "$YT_LANG_WORLD")
yt_remoto_br=$(fetch_yt "trabalho remoto home office" "$YT_REGION_BR" "$YT_LANG_BR")
yt_remoto_world=$(fetch_yt "remote work work from home distributed async" "$YT_REGION_WORLD" "$YT_LANG_WORLD")
yt_ingles_br=$(fetch_yt "aprender inglês fluência IELTS TOEFL" "$YT_REGION_BR" "$YT_LANG_BR")
yt_ingles_world=$(fetch_yt "learn english english fluency IELTS TOEFL" "$YT_REGION_WORLD" "$YT_LANG_WORLD")
yt_skills_br=$(fetch_yt "habilidades programação aprender a programar" "$YT_REGION_BR" "$YT_LANG_BR")
yt_skills_world=$(fetch_yt "programming skills coding developer tools" "$YT_REGION_WORLD" "$YT_LANG_WORLD")

# ═══════════════════════════════════════════════════════════
# GOOGLE NEWS (RSS) - BR e Mundo
# ═══════════════════════════════════════════════════════════

echo "  Google News (RSS)..." >&2

fetch_google_news_rss() {
  local query="$1"
  local hl="$2"
  local gl="$3"
  local ceid="$4"
  local enc
  enc=$(url_encode "$query")
  local url="https://news.google.com/rss/search?q=$enc&hl=$hl&gl=$gl&ceid=$ceid"
  local xml
  xml=$(curl_text "$url" "$NEWS_USER_AGENT")
  if [ -z "$xml" ]; then
    xml=$(curl_text_doh "$url" "$NEWS_USER_AGENT")
  fi
  if [ -z "$xml" ]; then
    echo '[]'
    return
  fi
  echo "$xml" | "$PYTHON_BIN" "$RSS_PARSER" - "$NEWS_LIMIT" "$NEWS_MAX_AGE_HOURS" 2>/dev/null | \
    jq '.items | map(. + {source:"Google News"})' 2>/dev/null || echo '[]'
}

if [ "$NEWS_MODE" = "rss" ]; then
  news_carreira_br=$(fetch_google_news_rss "carreira OR empregabilidade OR mercado de trabalho OR contratação OR demissão OR layoff OR salário OR promoção OR currículo OR entrevista OR \"mudança de carreira\" OR \"certificação\" OR \"habilidades\" OR \"profissões em alta\" OR \"setores que contratam\"" "pt-BR" "BR" "BR:pt-419")
  news_carreira_world=$(fetch_google_news_rss "career OR employability OR labor market OR hiring OR layoffs OR salary OR promotion OR resume OR interview OR career change OR certifications OR skills OR hiring trends" "en-US" "US" "US:en")

  news_intl_br=$(fetch_google_news_rss "internacionalização OR trabalhar fora OR visto OR imigração" "pt-BR" "BR" "BR:pt-419")
  news_intl_world=$(fetch_google_news_rss "immigration OR visa OR expat OR relocation OR international" "en-US" "US" "US:en")

  news_estudar_br=$(fetch_google_news_rss "estudar fora OR intercâmbio OR bolsa exterior OR universidade" "pt-BR" "BR" "BR:pt-419")
  news_estudar_world=$(fetch_google_news_rss "study abroad OR scholarship OR university OR masters OR phd" "en-US" "US" "US:en")

  news_edu_br=$(fetch_google_news_rss "educação OR cursos OR ensino" "pt-BR" "BR" "BR:pt-419")
  news_edu_world=$(fetch_google_news_rss "education OR courses OR learning" "en-US" "US" "US:en")
  news_edu_br_extra=$(NEWS_LIMIT="$NEWS_EDU_EXTRA_LIMIT" fetch_google_news_rss "edtech OR fusão OR aquisição educação" "pt-BR" "BR" "BR:pt-419")
  news_edu_world_extra=$(NEWS_LIMIT="$NEWS_EDU_EXTRA_LIMIT" fetch_google_news_rss "edtech OR merger OR acquisition education" "en-US" "US" "US:en")
  news_edu_br=$(echo "$news_edu_br" "$news_edu_br_extra" | jq -s 'add | unique_by(.title) | .[0:6]' 2>/dev/null || echo '[]')
  news_edu_world=$(echo "$news_edu_world" "$news_edu_world_extra" | jq -s 'add | unique_by(.title) | .[0:6]' 2>/dev/null || echo '[]')

  news_remoto_br=$(fetch_google_news_rss "trabalho remoto OR home office OR híbrido" "pt-BR" "BR" "BR:pt-419")
  news_remoto_world=$(fetch_google_news_rss "remote work OR work from home OR hybrid work" "en-US" "US" "US:en")

  news_ingles_br=$(fetch_google_news_rss "inglês OR aprender inglês OR fluência" "pt-BR" "BR" "BR:pt-419")
  news_ingles_world=$(fetch_google_news_rss "learn english OR language learning OR IELTS OR TOEFL" "en-US" "US" "US:en")

  news_skills_br=$(fetch_google_news_rss "skills OR habilidades OR programação OR tecnologia" "pt-BR" "BR" "BR:pt-419")
  news_skills_world=$(fetch_google_news_rss "skills OR programming OR developer OR tech skills" "en-US" "US" "US:en")
else
  news_carreira_br='[]'
  news_carreira_world='[]'
  news_intl_br='[]'
  news_intl_world='[]'
  news_estudar_br='[]'
  news_estudar_world='[]'
  news_edu_br='[]'
  news_edu_world='[]'
  news_remoto_br='[]'
  news_remoto_world='[]'
  news_ingles_br='[]'
  news_ingles_world='[]'
  news_skills_br='[]'
  news_skills_world='[]'
fi

# ═══════════════════════════════════════════════════════════
# REDDIT (RSS público) - sem API
# ═══════════════════════════════════════════════════════════

echo "  Reddit (RSS)..." >&2

fetch_reddit_rss_sub() {
  local sub="$1"
  local limit="$2"
  local xml
  xml=$(curl_text "https://www.reddit.com/r/$sub/.rss" "$REDDIT_USER_AGENT")
  if [ -z "$xml" ]; then
    xml=$(curl_text "https://old.reddit.com/r/$sub/.rss" "$REDDIT_USER_AGENT")
  fi
  if [ -z "$xml" ]; then
    xml=$(curl_text_doh "https://www.reddit.com/r/$sub/.rss" "$REDDIT_USER_AGENT")
  fi
  if [ -z "$xml" ]; then
    xml=$(curl_text_doh "https://old.reddit.com/r/$sub/.rss" "$REDDIT_USER_AGENT")
  fi
  if [ -z "$xml" ]; then
    echo '[]'
    return
  fi
  echo "$xml" | "$PYTHON_BIN" "$RSS_PARSER" - "$limit" "$REDDIT_MAX_AGE_HOURS" 2>/dev/null | \
    jq --arg sub "$sub" '.items | map(. + {source:"Reddit", subreddit:$sub})' 2>/dev/null || echo '[]'
}

fetch_reddit_topic() {
  local subs="$1"
  local limit="$2"
  local all='[]'
  for sub in $subs; do
    items=$(fetch_reddit_rss_sub "$sub" "$limit")
    all=$(echo "$all" "$items" | jq -s 'add' 2>/dev/null || echo '[]')
  done
  echo "$all" | jq ".[0:$limit]" 2>/dev/null || echo '[]'
}

if [ "$REDDIT_MODE" = "rss" ]; then
  reddit_carreira_br=$(fetch_reddit_topic "carreiras empregos Brasil brdev rjdev" "$REDDIT_LIMIT")
  reddit_carreira_world=$(fetch_reddit_topic "careerguidance jobs cscareerquestions careeradvice resumes" "$REDDIT_LIMIT")

  reddit_intl_br=$(fetch_reddit_topic "foradecasa brasil" "$REDDIT_LIMIT")
  reddit_intl_world=$(fetch_reddit_topic "iwantout immigration expats digitalnomad" "$REDDIT_LIMIT")

  reddit_estudar_br=$(fetch_reddit_topic "estudarfora brasil" "$REDDIT_LIMIT")
  reddit_estudar_world=$(fetch_reddit_topic "studyabroad gradadmissions scholarships college" "$REDDIT_LIMIT")

  reddit_edu_br=$(fetch_reddit_topic "educacao professores brasil" "$REDDIT_LIMIT")
  reddit_edu_world=$(fetch_reddit_topic "education onlinecourses teachers learnprogramming" "$REDDIT_LIMIT")

  reddit_remoto_br=$(fetch_reddit_topic "trabalhoremoto brasil" "$REDDIT_LIMIT")
  reddit_remoto_world=$(fetch_reddit_topic "remotework digitalnomad workfromhome freelancing" "$REDDIT_LIMIT")

  reddit_ingles_br=$(fetch_reddit_topic "ingles brasil languagelearning" "$REDDIT_LIMIT")
  reddit_ingles_world=$(fetch_reddit_topic "EnglishLearning languagelearning IELTS TOEFL" "$REDDIT_LIMIT")

  reddit_skills_br=$(fetch_reddit_topic "programacao brdev brasil" "$REDDIT_LIMIT")
  reddit_skills_world=$(fetch_reddit_topic "learnprogramming programming datascience devops productivity" "$REDDIT_LIMIT")
else
  reddit_carreira_br='[]'
  reddit_carreira_world='[]'
  reddit_intl_br='[]'
  reddit_intl_world='[]'
  reddit_estudar_br='[]'
  reddit_estudar_world='[]'
  reddit_edu_br='[]'
  reddit_edu_world='[]'
  reddit_remoto_br='[]'
  reddit_remoto_world='[]'
  reddit_ingles_br='[]'
  reddit_ingles_world='[]'
  reddit_skills_br='[]'
  reddit_skills_world='[]'
fi

# ═══════════════════════════════════════════════════════════
# TWITTER (RSSHub keyword) - pode exigir auth na instância
# ═══════════════════════════════════════════════════════════

echo "  Twitter..." >&2

fetch_twitter_keyword() {
  local keyword="$1"
  local limit="$2"
  local enc
  enc=$(url_encode "$keyword")
  for host in $TWITTER_RSSHUB_HOSTS; do
    local url="https://$host/twitter/keyword/$enc"
    local xml
    xml=$(curl_text "$url" "$TWITTER_USER_AGENT")
    [ -z "$xml" ] && continue
    items=$(echo "$xml" | "$PYTHON_BIN" "$RSS_PARSER" - "$limit" 2>/dev/null | jq '.items' 2>/dev/null || echo '[]')
    if [ "$(echo "$items" | jq 'length' 2>/dev/null || echo 0)" -gt 0 ]; then
      echo "$items" | jq 'map(. + {source:"Twitter"})' 2>/dev/null || echo '[]'
      return
    fi
  done
  echo '[]'
}

fetch_twitter_api() {
  local keyword="$1"
  local limit="$2"
  local require_terms="$3"
  local langs="$4"
  local pybin="$TWITTER_PYTHON_BIN"
  if [ -z "$pybin" ] && [ -x /home/ubuntu/clawd/sessions/personajes/venv/bin/python ]; then
    pybin="/home/ubuntu/clawd/sessions/personajes/venv/bin/python"
  fi
  [ -z "$pybin" ] && pybin="python3"
  TWITTER_ENV_FILE="$TWITTER_ENV_FILE" TWITTER_BEARER_TOKEN="$TWITTER_BEARER_TOKEN" \
    TWITTER_MIN_SCORE="$TWITTER_MIN_SCORE" TWITTER_LANGS="${langs:-$TWITTER_LANGS}" \
    TWITTER_MAX_AGE_HOURS="$TWITTER_MAX_AGE_HOURS" \
    TWITTER_REQUIRE_TERMS="$require_terms" \
    "$pybin" "$SCRIPT_DIR/twitter_api.py" "$keyword" "$limit" 2>/dev/null || echo '[]'
}

if [ "$TWITTER_MODE" = "rsshub" ]; then
  twitter_carreira_br=$(fetch_twitter_keyword "(emprego OR vaga OR entrevista OR salário OR demissão)" "$TWITTER_LIMIT")
  twitter_carreira_world=$(fetch_twitter_keyword "(job OR hiring OR interview OR salary OR layoff)" "$TWITTER_LIMIT")

  twitter_intl_br=$(fetch_twitter_keyword "(visto OR imigração OR intercâmbio OR trabalhar fora)" "$TWITTER_LIMIT")
  twitter_intl_world=$(fetch_twitter_keyword "(visa OR immigration OR relocation OR expat)" "$TWITTER_LIMIT")

  twitter_estudar_br=$(fetch_twitter_keyword "(estudar fora OR bolsa OR universidade)" "$TWITTER_LIMIT")
  twitter_estudar_world=$(fetch_twitter_keyword "(study abroad OR scholarship OR university OR masters OR phd)" "$TWITTER_LIMIT")

  twitter_edu_br=$(fetch_twitter_keyword "(educação OR edtech OR escola OR ensino OR professor)" "$TWITTER_LIMIT")
  twitter_edu_world=$(fetch_twitter_keyword "(education OR edtech OR school OR teacher)" "$TWITTER_LIMIT")

  twitter_remoto_br=$(fetch_twitter_keyword "(trabalho remoto OR home office OR remoto)" "$TWITTER_LIMIT")
  twitter_remoto_world=$(fetch_twitter_keyword "(remote work OR work from home OR distributed)" "$TWITTER_LIMIT")

  twitter_ingles_br=$(fetch_twitter_keyword "(inglês OR aprender inglês OR fluência)" "$TWITTER_LIMIT")
  twitter_ingles_world=$(fetch_twitter_keyword "(learn english OR IELTS OR TOEFL OR english learning)" "$TWITTER_LIMIT")

  twitter_skills_br=$(fetch_twitter_keyword "(habilidades OR programação OR aprender a programar OR tecnologia)" "$TWITTER_LIMIT")
  twitter_skills_world=$(fetch_twitter_keyword "(programming OR coding OR developer OR data science OR skills)" "$TWITTER_LIMIT")
elif [ "$TWITTER_MODE" = "api" ] || [ "$TWITTER_MODE" = "oauth1" ]; then
  twitter_carreira_br=$(fetch_twitter_api "(emprego OR vaga OR entrevista OR salário OR demissão)" "$TWITTER_LIMIT" "emprego,vaga,entrevista,salário,demissão" "pt")
  twitter_carreira_world=$(fetch_twitter_api "(job OR hiring OR interview OR salary OR layoff)" "$TWITTER_LIMIT" "job,hiring,interview,salary,layoff" "en")

  twitter_intl_br=$(fetch_twitter_api "(visto OR imigração OR intercâmbio OR trabalhar fora)" "$TWITTER_LIMIT" "visto,imigração,intercâmbio,trabalhar fora" "pt")
  twitter_intl_world=$(fetch_twitter_api "(visa OR immigration OR relocation OR expat)" "$TWITTER_LIMIT" "visa,immigration,relocation,expat" "en")

  twitter_estudar_br=$(fetch_twitter_api "(estudar fora OR bolsa OR universidade)" "$TWITTER_LIMIT" "estudar fora,bolsa,universidade" "pt")
  twitter_estudar_world=$(fetch_twitter_api "(study abroad OR scholarship OR university OR masters OR phd)" "$TWITTER_LIMIT" "study abroad,scholarship,university,masters,phd" "en")

  twitter_edu_br=$(fetch_twitter_api "(educação OR edtech OR escola OR ensino OR professor)" "$TWITTER_LIMIT" "educação,edtech,escola,ensino,professor" "pt")
  twitter_edu_world=$(fetch_twitter_api "(education OR edtech OR school OR teacher)" "$TWITTER_LIMIT" "education,edtech,school,teacher" "en")

  twitter_remoto_br=$(fetch_twitter_api "(trabalho remoto OR home office OR remoto)" "$TWITTER_LIMIT" "trabalho remoto,home office,remoto" "pt")
  twitter_remoto_world=$(fetch_twitter_api "(remote work OR work from home OR distributed)" "$TWITTER_LIMIT" "remote work,work from home,distributed" "en")

  twitter_ingles_br=$(fetch_twitter_api "(inglês OR aprender inglês OR fluência)" "$TWITTER_LIMIT" "inglês,aprender inglês,fluência" "pt")
  twitter_ingles_world=$(fetch_twitter_api "(learn english OR IELTS OR TOEFL OR english learning)" "$TWITTER_LIMIT" "learn english,IELTS,TOEFL,english learning" "en")

  twitter_skills_br=$(fetch_twitter_api "(habilidades OR programação OR aprender a programar OR tecnologia)" "$TWITTER_LIMIT" "habilidades,programação,aprender a programar,tecnologia" "pt")
  twitter_skills_world=$(fetch_twitter_api "(programming OR coding OR developer OR data science OR skills)" "$TWITTER_LIMIT" "programming,coding,developer,data science,skills" "en")
else
  twitter_carreira_br='[]'
  twitter_carreira_world='[]'
  twitter_intl_br='[]'
  twitter_intl_world='[]'
  twitter_estudar_br='[]'
  twitter_estudar_world='[]'
  twitter_edu_br='[]'
  twitter_edu_world='[]'
  twitter_remoto_br='[]'
  twitter_remoto_world='[]'
  twitter_ingles_br='[]'
  twitter_ingles_world='[]'
  twitter_skills_br='[]'
  twitter_skills_world='[]'
fi

# ═══════════════════════════════════════════════════════════
# COMPILAR JSON
# ═══════════════════════════════════════════════════════════

output=$(jq -n \
  --argjson hn_carreira "$hn_carreira" \
  --argjson hn_intl "$hn_intl" \
  --argjson hn_estudar "$hn_estudar" \
  --argjson hn_edu "$hn_edu" \
  --argjson hn_remoto "$hn_remoto" \
  --argjson hn_ingles "$hn_ingles" \
  --argjson hn_skills "$hn_skills" \
  --argjson yt_carreira_br "$yt_carreira_br" \
  --argjson yt_carreira_world "$yt_carreira_world" \
  --argjson yt_intl_br "$yt_intl_br" \
  --argjson yt_intl_world "$yt_intl_world" \
  --argjson yt_estudar_br "$yt_estudar_br" \
  --argjson yt_estudar_world "$yt_estudar_world" \
  --argjson yt_edu_br "$yt_edu_br" \
  --argjson yt_edu_world "$yt_edu_world" \
  --argjson yt_remoto_br "$yt_remoto_br" \
  --argjson yt_remoto_world "$yt_remoto_world" \
  --argjson yt_ingles_br "$yt_ingles_br" \
  --argjson yt_ingles_world "$yt_ingles_world" \
  --argjson yt_skills_br "$yt_skills_br" \
  --argjson yt_skills_world "$yt_skills_world" \
  --argjson news_carreira_br "$news_carreira_br" \
  --argjson news_carreira_world "$news_carreira_world" \
  --argjson news_intl_br "$news_intl_br" \
  --argjson news_intl_world "$news_intl_world" \
  --argjson news_estudar_br "$news_estudar_br" \
  --argjson news_estudar_world "$news_estudar_world" \
  --argjson news_edu_br "$news_edu_br" \
  --argjson news_edu_world "$news_edu_world" \
  --argjson news_remoto_br "$news_remoto_br" \
  --argjson news_remoto_world "$news_remoto_world" \
  --argjson news_ingles_br "$news_ingles_br" \
  --argjson news_ingles_world "$news_ingles_world" \
  --argjson news_skills_br "$news_skills_br" \
  --argjson news_skills_world "$news_skills_world" \
  --argjson reddit_carreira_br "$reddit_carreira_br" \
  --argjson reddit_carreira_world "$reddit_carreira_world" \
  --argjson reddit_intl_br "$reddit_intl_br" \
  --argjson reddit_intl_world "$reddit_intl_world" \
  --argjson reddit_estudar_br "$reddit_estudar_br" \
  --argjson reddit_estudar_world "$reddit_estudar_world" \
  --argjson reddit_edu_br "$reddit_edu_br" \
  --argjson reddit_edu_world "$reddit_edu_world" \
  --argjson reddit_remoto_br "$reddit_remoto_br" \
  --argjson reddit_remoto_world "$reddit_remoto_world" \
  --argjson reddit_ingles_br "$reddit_ingles_br" \
  --argjson reddit_ingles_world "$reddit_ingles_world" \
  --argjson reddit_skills_br "$reddit_skills_br" \
  --argjson reddit_skills_world "$reddit_skills_world" \
  --argjson twitter_carreira_br "$twitter_carreira_br" \
  --argjson twitter_carreira_world "$twitter_carreira_world" \
  --argjson twitter_intl_br "$twitter_intl_br" \
  --argjson twitter_intl_world "$twitter_intl_world" \
  --argjson twitter_estudar_br "$twitter_estudar_br" \
  --argjson twitter_estudar_world "$twitter_estudar_world" \
  --argjson twitter_edu_br "$twitter_edu_br" \
  --argjson twitter_edu_world "$twitter_edu_world" \
  --argjson twitter_remoto_br "$twitter_remoto_br" \
  --argjson twitter_remoto_world "$twitter_remoto_world" \
  --argjson twitter_ingles_br "$twitter_ingles_br" \
  --argjson twitter_ingles_world "$twitter_ingles_world" \
  --argjson twitter_skills_br "$twitter_skills_br" \
  --argjson twitter_skills_world "$twitter_skills_world" \
  '{
    hackernews: {
      carreira: $hn_carreira,
      internacionalizacao: $hn_intl,
      estudar_fora: $hn_estudar,
      educacao: $hn_edu,
      trabalho_remoto: $hn_remoto,
      ingles: $hn_ingles,
      skills: $hn_skills
    },
    reddit: {
      carreira: { br: $reddit_carreira_br, mundo: $reddit_carreira_world },
      internacionalizacao: { br: $reddit_intl_br, mundo: $reddit_intl_world },
      estudar_fora: { br: $reddit_estudar_br, mundo: $reddit_estudar_world },
      educacao: { br: $reddit_edu_br, mundo: $reddit_edu_world },
      trabalho_remoto: { br: $reddit_remoto_br, mundo: $reddit_remoto_world },
      ingles: { br: $reddit_ingles_br, mundo: $reddit_ingles_world },
      skills: { br: $reddit_skills_br, mundo: $reddit_skills_world }
    },
    twitter: {
      carreira: { br: $twitter_carreira_br, mundo: $twitter_carreira_world },
      internacionalizacao: { br: $twitter_intl_br, mundo: $twitter_intl_world },
      estudar_fora: { br: $twitter_estudar_br, mundo: $twitter_estudar_world },
      educacao: { br: $twitter_edu_br, mundo: $twitter_edu_world },
      trabalho_remoto: { br: $twitter_remoto_br, mundo: $twitter_remoto_world },
      ingles: { br: $twitter_ingles_br, mundo: $twitter_ingles_world },
      skills: { br: $twitter_skills_br, mundo: $twitter_skills_world }
    },
    youtube: {
      carreira: { br: $yt_carreira_br, mundo: $yt_carreira_world },
      internacionalizacao: { br: $yt_intl_br, mundo: $yt_intl_world },
      estudar_fora: { br: $yt_estudar_br, mundo: $yt_estudar_world },
      educacao: { br: $yt_edu_br, mundo: $yt_edu_world },
      trabalho_remoto: { br: $yt_remoto_br, mundo: $yt_remoto_world },
      ingles: { br: $yt_ingles_br, mundo: $yt_ingles_world },
      skills: { br: $yt_skills_br, mundo: $yt_skills_world }
    },
    google_news: {
      carreira: { br: $news_carreira_br, mundo: $news_carreira_world },
      internacionalizacao: { br: $news_intl_br, mundo: $news_intl_world },
      estudar_fora: { br: $news_estudar_br, mundo: $news_estudar_world },
      educacao: { br: $news_edu_br, mundo: $news_edu_world },
      trabalho_remoto: { br: $news_remoto_br, mundo: $news_remoto_world },
      ingles: { br: $news_ingles_br, mundo: $news_ingles_world },
      skills: { br: $news_skills_br, mundo: $news_skills_world }
    },
    timestamp: now | floor
  }')

if [ -f "$LAST_GOOD_FILE" ]; then
  output=$(echo "$output" | jq --slurpfile last "$LAST_GOOD_FILE" '
    def last: ($last[0] // {});
    def sum_hn: ([.hackernews[] | length] | add);
    def sum_reddit: ([.reddit[] | (.br|length) + (.mundo|length)] | add);
    def sum_youtube: ([.youtube[] | (.br|length) + (.mundo|length)] | add);
    def sum_twitter: ([.twitter[] | (.br|length) + (.mundo|length)] | add);
    def sum_news: (
      [.google_news[] | (.br|length) + (.mundo|length)] | add
    );
    (if sum_hn == 0 and (last.hackernews? != null) then .hackernews = last.hackernews else . end)
    | (if sum_reddit == 0 and (last.reddit? != null) then .reddit = last.reddit else . end)
    | (if sum_youtube == 0 and (last.youtube? != null) then .youtube = last.youtube else . end)
    | (if sum_twitter == 0 and (last.twitter? != null) then .twitter = last.twitter else . end)
    | (if sum_news == 0 and (last.google_news? != null) then .google_news = last.google_news else . end)
  ')
fi

if echo "$output" | jq -e '
  ([.hackernews[] | length] | add) +
  ([.reddit[] | (.br|length) + (.mundo|length)] | add) +
  ([.youtube[] | (.br|length) + (.mundo|length)] | add) +
  ([.twitter[] | (.br|length) + (.mundo|length)] | add) +
  ([.google_news[] | (.br|length) + (.mundo|length)] | add)
  > 0
' >/dev/null 2>&1; then
  echo "$output" > "$LAST_GOOD_FILE"
fi

echo "$output" | tee "$CACHE_FILE"
echo "Done! Saved to $CACHE_FILE" >&2
