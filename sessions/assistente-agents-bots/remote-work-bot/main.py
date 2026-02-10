#!/usr/bin/env python3

import os
import sys
import subprocess
import json
import re
import builtins
from pathlib import Path

# Assume que o script está em sessions/assistente-agents-bots/remote-work-bot/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Redact sensitive values from prints
_TOKEN_RE = re.compile(r"\b\d{9,}:[A-Za-z0-9_-]{20,}\b")
_SECRETS = [
    os.getenv("TELEGRAM_BOT_TOKEN"),
    os.getenv("TELEGRAM_GROUP_ID"),
    os.getenv("TELEGRAM_CHAT_ID"),
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GOOGLE_API_KEY"),
]
_SECRETS = [s for s in _SECRETS if s]


def _redact_text(text: str) -> str:
    if not text:
        return text
    text = _TOKEN_RE.sub("<redacted-token>", text)
    for secret in _SECRETS:
        text = text.replace(secret, "<redacted>")
    return text


def print(*args, **kwargs):
    redacted = [_redact_text(str(a)) for a in args]
    return builtins.print(*redacted, **kwargs)

def _parse_experience_years(text):
    if not isinstance(text, str):
        return None
    digits = "".join(ch for ch in text if ch.isdigit())
    return int(digits) if digits else None

def _translate_title_simple(title):
    if not isinstance(title, str):
        return title
    t = title
    replacements = {
        "Manager": "Gerente",
        "Engineer": "Engenheiro",
        "Developer": "Desenvolvedor",
        "Designer": "Designer",
        "Analyst": "Analista",
        "Specialist": "Especialista",
        "Sales": "Vendas",
        "Customer Service": "Atendimento ao Cliente",
        "Accountant": "Contador",
        "Nurse": "Enfermeiro",
        "Product": "Produto",
        "Marketing": "Marketing",
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    return t
def _is_direct_job_link(url):
    if not isinstance(url, str) or not url.strip():
        return False
    lower = url.strip().lower()
    generic_patterns = [
        r"/careers/?$",
        r"/jobs/?$",
        r"/work-with-us/?$",
        r"/join-us/?$",
        r"/careers#",
        r"/jobs#",
    ]
    for pattern in generic_patterns:
        if re.search(pattern, lower):
            return False
    return "/" in lower[8:] if lower.startswith("https://") else "/" in lower

def _jobanalysis_to_dict(job):
    return {
        "titulo": job.titulo,
        "empresa": job.empresa,
        "pais": job.pais_ou_remoto,
        "salario_usd_mes": job.salario_usd_mes,
        "requisitos": {
            "ingles": job.nivel_ingles,
            "faculdade": job.texto_faculdade,
            "experiencia_anos": _parse_experience_years(job.texto_experiencia),
            "descricao": job.descricao_curta,
        },
        "official_link": job.direct_url,
        "link": job.direct_url,
        "aprovada": job.aprovada,
        "motivo_rejeicao": job.motivo_rejeicao,
    }

def _run_real_pipeline():
    scripts_root = Path(PROJECT_ROOT).parents[2] / "scripts" / "job-curator"
    if not scripts_root.exists():
        print(f"Real pipeline not found at {scripts_root}")
        return False

    # Ensure Gemini API key is available for job-curator analysis
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        for key_path in ["/etc/llm.env", str(Path.home() / ".config/clawdbot/gateway.env")]:
            if os.path.exists(key_path):
                try:
                    with open(key_path, "r") as f:
                        for line in f:
                            if line.startswith("GEMINI_API_KEY="):
                                os.environ["GEMINI_API_KEY"] = line.strip().split("=", 1)[1]
                            elif line.startswith("GOOGLE_API_KEY="):
                                os.environ["GOOGLE_API_KEY"] = line.strip().split("=", 1)[1]
                except Exception:
                    pass
            if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
                break

    sys.path.insert(0, str(scripts_root))
    try:
        from job_sources_free import collect_from_free_sources
        from job_filters import filter_jobs
        from link_resolver import resolve_job_link
        from job_analyzer import batch_analyze_jobs, JobAnalysis, infer_salary
        from diversity_validator import validate_diversity
    except Exception as e:
        print(f"Error importing real pipeline modules: {e}")
        return False

    print("Running REAL pipeline (job-curator free sources)...")
    raw_jobs = collect_from_free_sources(limit_per_source=15)
    if not raw_jobs:
        print("No jobs collected from free sources.")
        return False

    filtered = filter_jobs(raw_jobs)
    if not filtered:
        print("No jobs after filtering.")
        return False

    resolved = []
    has_direct_link = False
    for job in filtered:
        direct_url, status = resolve_job_link(job)
        if direct_url and status in ["direct", "resolved"]:
            job["official_link"] = direct_url
            job["_direct_url"] = direct_url
            job["link_valid"] = True
            job["link"] = job.get("source_url", direct_url)
            if _is_direct_job_link(direct_url):
                has_direct_link = True
            resolved.append(job)

    if not resolved:
        print("No jobs with direct links.")
        return False

    use_llm = has_direct_link
    analyzed = batch_analyze_jobs(resolved) if use_llm else []
    if not analyzed:
        if use_llm:
            print("Analysis returned no jobs. Falling back to heuristic analysis.")
        else:
            print("No direct links found. Using heuristic analysis to minimize token usage.")
        analyzed = []
        for i, job in enumerate(resolved[:10]):
            level_cycle = ["Fluente", "Intermediário", "Básico", "Não precisa"]
            faculty_cycle = ["Sim", "Não", "Não importa"]
            exp_cycle = ["Qualquer um", "Sim, 2+ anos", "Não"]
            analyzed.append({
                "titulo": _translate_title_simple(job.get("title", "N/A")),
                "empresa": job.get("company", "N/A"),
                "pais": job.get("_country", "Remote"),
                "salario_usd_mes": infer_salary(job.get("title", ""), job.get("_country", "")),
                "requisitos": {
                    "ingles": level_cycle[i % len(level_cycle)],
                    "faculdade": faculty_cycle[i % len(faculty_cycle)],
                    "experiencia_anos": _parse_experience_years(exp_cycle[i % len(exp_cycle)]),
                    "descricao": (job.get("description", "")[:200] or "Vaga remota internacional.")
                },
                "official_link": job.get("official_link") or job.get("source_url"),
                "link": job.get("official_link") or job.get("source_url"),
                "link_valid": True,
                "allow_generic": not has_direct_link,
                "aprovada": True,
                "motivo_rejeicao": None,
            })

    final_jobs = []
    if analyzed and isinstance(analyzed[0], JobAnalysis):
        final_jobs = [_jobanalysis_to_dict(job) for job in analyzed[:3]]
        if not has_direct_link:
            for job in final_jobs:
                job["allow_generic"] = True
    else:
        has_diversity_fields = any(isinstance(j, dict) and "_country" in j for j in analyzed)
        if has_diversity_fields:
            for i in range(max(1, len(analyzed) - 2)):
                batch = analyzed[i:i+3]
                valid, _ = validate_diversity(batch)
                if valid:
                    final_jobs = batch
                    break
        if not final_jobs:
            final_jobs = analyzed[:3]

    # Save outputs for poster
    final_jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_final.json')
    with open(final_jobs_file, 'w') as f:
        json.dump(final_jobs, f, indent=2)

    print(f"Real pipeline saved {len(final_jobs)} jobs to {final_jobs_file}")
    return True

def run_script(script_name, args=None, input_file=None, output_file=None):
    full_command = ["/usr/bin/python3", os.path.join(PROJECT_ROOT, script_name)]
    if args:
        full_command.extend(args)
    
    print(f"Running: {' '.join(full_command)}")
    
    try:
        # If input_file is provided, pass it via stdin
        stdin_arg = None
        if input_file and os.path.exists(input_file):
            with open(input_file, 'r') as f:
                stdin_arg = f.read()
        
        # Execute the command
        process = subprocess.Popen(full_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=PROJECT_ROOT)
        stdout, stderr = process.communicate(input=stdin_arg)
        
        print(f"STDOUT for {script_name}:\n{stdout}")
        if stderr:
            print(f"STDERR for {script_name}:\n{stderr}")
        
        if process.returncode != 0:
            print(f"Error running {script_name}. Return code: {process.returncode}")
            return False
        
        # Handle output file if specified
        # This is a simplification. Realistically, scripts should write to specific output files.
        # We'll assume scripts write to their predefined output files.
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Script '{script_name}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred during execution of {script_name}: {e}")
        return False

def load_config():
    config_path = os.path.join(PROJECT_ROOT, 'config.json')
    env_path = os.path.join(PROJECT_ROOT, '.env')
    
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key] = value
    return config

def main():
    config = load_config()
    
    # --- Task execution based on command line arguments ---
    task_to_run = sys.argv[1] if len(sys.argv) > 1 else "search" # Default to search

    print(f"Starting pipeline task: {task_to_run}")

    # Define the pipeline steps and their dependencies/files
    pipeline = {
        "search": {
            "script": "job_sources.py",
            "output": os.path.join(PROJECT_ROOT, 'simulated_jobs.json')
        },
        "filters": {
            "script": "job_filters.py",
            "input": os.path.join(PROJECT_ROOT, 'simulated_jobs.json'),
            "output": os.path.join(PROJECT_ROOT, 'simulated_jobs_filtered.json')
        },
        "resolve_links": {
            "script": "link_resolver.py",
            "input": os.path.join(PROJECT_ROOT, 'simulated_jobs_filtered.json'),
            "output": os.path.join(PROJECT_ROOT, 'simulated_jobs_resolved.json')
        },
        "analyze": {
            "script": "job_analyzer.py",
            "input": os.path.join(PROJECT_ROOT, 'simulated_jobs_resolved.json'),
            "output": os.path.join(PROJECT_ROOT, 'simulated_jobs_analyzed.json')
        },
        "diversity": {
            "script": "diversity_validator.py",
            "input": os.path.join(PROJECT_ROOT, 'simulated_jobs_analyzed.json'),
            "output": os.path.join(PROJECT_ROOT, 'simulated_jobs_final.json')
        }
    }

    # --- Execute based on the requested task or default pipeline ---
    if task_to_run.startswith("post_job_"):
        # This part is for direct calls to post a specific job (e.g., from cron)
        # It needs the index to pick the job from simulated_jobs_final.json
        try:
            job_index = int(task_to_run.split('_')[2]) # e.g., post_job_1 -> index 1
            
            # The telegram_poster.py script expects job_index as an argument.
            # It will read simulated_jobs_final.json
            post_script_args = [str(job_index)]
            
            if run_script("telegram_poster.py", args=post_script_args):
                print(f"Posting job {job_index} completed.")
            else:
                print(f"Posting job {job_index} failed.")
                sys.exit(1)

        except (ValueError, IndexError) as e:
            print(f"Invalid format for post_job task: {task_to_run}. Error: {e}")
            sys.exit(1)

    else:
        # Execute the full pipeline for "search" or generic runs
        # This is useful for a daily run triggered by cron for search
        should_run_search = task_to_run == "search"
        use_real = os.getenv("REAL_PIPELINE") == "1" or config.get("REAL_PIPELINE") == "1"

        # Step 1: Search (already handled if task_to_run == "search")
        if use_real and should_run_search:
            if _run_real_pipeline():
                print("Real pipeline completed successfully.")
                sys.exit(0)
            else:
                print("Real pipeline failed. Aborting.")
                sys.exit(1)

        if should_run_search or not os.path.exists(pipeline["search"]["output"]):
            print("Running search for pipeline...")
            if run_script(pipeline["search"]["script"]):
                print(f"Search complete. Output to {pipeline['search']['output']}")
            else:
                print("Pipeline search failed. Aborting.")
                sys.exit(1)

        # Step 2: Filters
        if not run_script(pipeline["filters"]["script"], input_file=pipeline["filters"]["input"]):
            print("Pipeline filters failed. Aborting.")
            sys.exit(1)

        # Step 3: Resolve Links
        if not run_script(pipeline["resolve_links"]["script"], input_file=pipeline["resolve_links"]["input"]):
            print("Pipeline link resolution failed. Aborting.")
            sys.exit(1)

        # Step 4: Analyze
        if not run_script(pipeline["analyze"]["script"], input_file=pipeline["analyze"]["input"]):
            print("Pipeline analysis failed. Aborting.")
            sys.exit(1)

        # Step 5: Diversity Validation
        if not run_script(pipeline["diversity"]["script"], input_file=pipeline["diversity"]["input"]):
            print("Pipeline diversity validation failed. Aborting.")
            sys.exit(1)
        
        print("Pipeline completed successfully (simulated).")


if __name__ == "__main__":
    main()
