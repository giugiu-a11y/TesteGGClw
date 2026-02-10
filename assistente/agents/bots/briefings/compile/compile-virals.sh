#!/bin/bash
# compile-virals.sh - Virals por fonte (HN/Reddit/YouTube/Twitter)
# Output: /tmp/briefing-virals.txt

virals=$(cat /tmp/virals.json)

get_hn() {
  local jqpath="$1"
  echo "$virals" | jq -r "$jqpath[0:5][]? |
    \"• \\(.title[0:90]) — \\(.source // \"Hacker News\") (\\(.score) pts)\"" | awk 'NF{print; print ""}'
}

get_yt() {
  local jqpath="$1"
  echo "$virals" | jq -r "$jqpath[0:5][]? |
    \"🎬 \\(.views // 0) views — \\(.channel // \"Canal\") — \\(.title[0:90])\"" | awk 'NF{print; print ""}'
}

get_rss() {
  local jqpath="$1"
  echo "$virals" | jq -r "$jqpath[0:5][]? |
    \"• \\(.title[0:90]) — \\(.source // \"RSS\")\"" | awk 'NF{print; print ""}'
}

get_twitter() {
  local jqpath="$1"
  echo "$virals" | jq -r "$jqpath[0:5][]? |
    \"• \\(.title[0:90]) — \\(.source // \"Twitter\") (\\(.likes // 0)L \\(.retweets // 0)RT)\"" | \
    sed -E 's/https?:\/\/\S+//g; s/[[:space:]]+/ /g; s/[[:space:]]+$//' | awk 'NF{print; print ""}'
}

get_news() {
  local jqpath="$1"
  echo "$virals" | jq -r "$jqpath[0:5][]? |
    \"• \\(.title[0:90]) — \\(.source // \"Google News\")\"" | awk 'NF{print; print ""}'
}

{
  echo "🔥 VIRAIS — $(date '+%d/%m/%Y %H:%M')"
  echo "Fontes separadas | 7 Tópicos"
  echo ""
  
  echo "===== GOOGLE NEWS (BR) ====="
  echo "📌 1. CARREIRA"
  get_news '.google_news.carreira.br'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_news '.google_news.internacionalizacao.br'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_news '.google_news.estudar_fora.br'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_news '.google_news.educacao.br'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_news '.google_news.trabalho_remoto.br'
  echo ""

  echo "📌 6. INGLÊS"
  get_news '.google_news.ingles.br'
  echo ""

  echo "📌 7. SKILLS"
  get_news '.google_news.skills.br'
  echo ""

  echo "===== GOOGLE NEWS (MUNDO) ====="
  echo "📌 1. CARREIRA"
  get_news '.google_news.carreira.mundo'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_news '.google_news.internacionalizacao.mundo'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_news '.google_news.estudar_fora.mundo'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_news '.google_news.educacao.mundo'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_news '.google_news.trabalho_remoto.mundo'
  echo ""

  echo "📌 6. INGLÊS"
  get_news '.google_news.ingles.mundo'
  echo ""

  echo "📌 7. SKILLS"
  get_news '.google_news.skills.mundo'
  echo ""

  echo "===== REDDIT (BR) ====="
  echo "📌 1. CARREIRA"
  get_rss '.reddit.carreira.br'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_rss '.reddit.internacionalizacao.br'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_rss '.reddit.estudar_fora.br'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_rss '.reddit.educacao.br'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_rss '.reddit.trabalho_remoto.br'
  echo ""

  echo "📌 6. INGLÊS"
  get_rss '.reddit.ingles.br'
  echo ""

  echo "📌 7. SKILLS"
  get_rss '.reddit.skills.br'
  echo ""

  echo "===== REDDIT (MUNDO) ====="
  echo "📌 1. CARREIRA"
  get_rss '.reddit.carreira.mundo'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_rss '.reddit.internacionalizacao.mundo'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_rss '.reddit.estudar_fora.mundo'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_rss '.reddit.educacao.mundo'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_rss '.reddit.trabalho_remoto.mundo'
  echo ""

  echo "📌 6. INGLÊS"
  get_rss '.reddit.ingles.mundo'
  echo ""

  echo "📌 7. SKILLS"
  get_rss '.reddit.skills.mundo'
  echo ""

  echo "===== YOUTUBE (BR) ====="
  echo "📌 1. CARREIRA"
  get_yt '.youtube.carreira.br'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_yt '.youtube.internacionalizacao.br'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_yt '.youtube.estudar_fora.br'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_yt '.youtube.educacao.br'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_yt '.youtube.trabalho_remoto.br'
  echo ""

  echo "📌 6. INGLÊS"
  get_yt '.youtube.ingles.br'
  echo ""

  echo "📌 7. SKILLS"
  get_yt '.youtube.skills.br'
  echo ""

  echo "===== YOUTUBE (MUNDO) ====="
  echo "📌 1. CARREIRA"
  get_yt '.youtube.carreira.mundo'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_yt '.youtube.internacionalizacao.mundo'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_yt '.youtube.estudar_fora.mundo'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_yt '.youtube.educacao.mundo'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_yt '.youtube.trabalho_remoto.mundo'
  echo ""

  echo "📌 6. INGLÊS"
  get_yt '.youtube.ingles.mundo'
  echo ""

  echo "📌 7. SKILLS"
  get_yt '.youtube.skills.mundo'
  echo ""

  echo "===== TWITTER (BR) ====="
  echo "📌 1. CARREIRA"
  get_twitter '.twitter.carreira.br'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_twitter '.twitter.internacionalizacao.br'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_twitter '.twitter.estudar_fora.br'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_twitter '.twitter.educacao.br'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_twitter '.twitter.trabalho_remoto.br'
  echo ""

  echo "📌 6. INGLÊS"
  get_twitter '.twitter.ingles.br'
  echo ""

  echo "📌 7. SKILLS"
  get_twitter '.twitter.skills.br'
  echo ""

  echo "===== TWITTER (MUNDO) ====="
  echo "📌 1. CARREIRA"
  get_twitter '.twitter.carreira.mundo'
  echo ""

  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_twitter '.twitter.internacionalizacao.mundo'
  echo ""

  echo "📌 3. ESTUDAR FORA"
  get_twitter '.twitter.estudar_fora.mundo'
  echo ""

  echo "📌 4. EDUCAÇÃO"
  get_twitter '.twitter.educacao.mundo'
  echo ""

  echo "📌 5. TRABALHO REMOTO"
  get_twitter '.twitter.trabalho_remoto.mundo'
  echo ""

  echo "📌 6. INGLÊS"
  get_twitter '.twitter.ingles.mundo'
  echo ""

  echo "📌 7. SKILLS"
  get_twitter '.twitter.skills.mundo'
  echo ""
  
  echo "===== HACKER NEWS ====="
  echo "📌 1. CARREIRA"
  get_hn '.hackernews.carreira'
  echo ""
  
  echo "📌 2. INTERNACIONALIZAÇÃO"
  get_hn '.hackernews.internacionalizacao'
  echo ""
  
  echo "📌 3. ESTUDAR FORA"
  get_hn '.hackernews.estudar_fora'
  echo ""
  
  echo "📌 4. EDUCAÇÃO"
  get_hn '.hackernews.educacao'
  echo ""
  
  echo "📌 5. TRABALHO REMOTO"
  get_hn '.hackernews.trabalho_remoto'
  echo ""
  
  echo "📌 6. INGLÊS"
  get_hn '.hackernews.ingles'
  echo ""
  
  echo "📌 7. SKILLS"
  get_hn '.hackernews.skills'
  
} > /tmp/briefing-virals.txt

# Split em partes por fonte
rm -f /tmp/briefing-virals-part*.txt /tmp/briefing-virals-parts.txt 2>/dev/null || true
awk '
BEGIN { part=0; pre=""; }
{
  if ($0 ~ /^===== /) {
    part++;
    file=sprintf("/tmp/briefing-virals-part%d.txt", part);
    if (part==1 && pre!="") { printf "%s", pre > file; }
    print $0 > file;
  } else {
    if (part==0) { pre = pre $0 "\n"; }
    else { print $0 > file; }
  }
}
END {
  if (part==0 && pre!="") {
    file="/tmp/briefing-virals-part1.txt";
    printf "%s", pre > file;
    part=1;
  }
}
' /tmp/briefing-virals.txt
ls /tmp/briefing-virals-part*.txt 2>/dev/null | sort > /tmp/briefing-virals-parts.txt

# Verificar tamanho
size=$(wc -c < /tmp/briefing-virals.txt)
echo "=== Briefing: $size chars ===" >&2

cat /tmp/briefing-virals.txt
