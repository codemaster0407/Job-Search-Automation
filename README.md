# 📄 Job Search Automation

An AI-powered tool that automatically tailors your CV and generates a cover letter for any job role — using your master CV context and a job description as inputs.

---

## 🗂️ Repository Structure

```
Job-Search-Automation/
├── main.py                  # Core CV generation pipeline (CLI)
├── app.py                   # Streamlit UI for CV form input (experimental)
├── Config.py                # Path configuration constants
├── prompt.txt               # Prompt template reference
├── requirements.txt         # Python dependencies
│
├── master_data/
│   ├── master_cv_context.txt    # Your complete professional background (source of truth)
│   └── job_description.txt      # Paste the target job description here
│
├── llm_call/
│   ├── groq_api.py          # Groq LLM API wrapper (streaming completions)
│   └── hugging_face_call.py # HuggingFace alternative (optional)
│
├── utils/
│   ├── cv_save.py           # Orchestrates saving CV, cover letter, PDF, and metadata
│   ├── doc_create.py        # Builds .docx files for CV and cover letter
│   ├── docx_2_pdf.py        # Converts .docx → PDF
│   ├── csv_creater.py       # CSV utilities for job tracking
│   └── string_parser.py     # String helper utilities
│
├── job_search/
│   ├── ireland_jobs.py      # Scraper for Irish job boards
│   ├── uk_jobs.py           # Scraper for UK job boards
│   └── resume_customise.py  # Resume customisation helpers
│
├── scraper_utils/
│   ├── web_scraper.py       # Core web scraping utilities (Selenium/requests)
│   └── crawler.py           # URL crawler helper
│
└── jobs_csv/
    └── <CompanyName>/       # Auto-generated per job application
        ├── Chaitanya Srikanth CV - <Company>.docx
        ├── Chaitanya Srikanth CV - <Company>.pdf
        ├── Cover Letter - <Company>.docx
        ├── Cover Letter - <Company>.pdf
        └── job_metadata.json
```

---

## ⚡ How `main.py` Works

`main.py` is the core pipeline that generates a tailored CV and cover letter for a given job role. Here is the step-by-step flow:

```
master_data/master_cv_context.txt  ──┐
                                      ├──▶  create_prompt()  ──▶  groq_api_call()  ──▶  save_cv()
master_data/job_description.txt    ──┘
```

### Step-by-step breakdown

#### 1. Read Inputs (`Config.py` paths)

```python
# Config.py
MASTER_CV_PATH      = 'master_data/master_cv_context.txt '
JOB_DESCRIPTION_PATH = 'master_data/job_description.txt'
```

`main.py` reads both files at startup:

```python
with open(Config.JOB_DESCRIPTION_PATH, 'r') as file:
    job_description = file.read()

with open(Config.MASTER_CV_PATH, 'r') as file:
    master_cv_content = file.read()
```

#### 2. Build the Prompt — `create_prompt()`

`create_prompt()` injects both inputs into a detailed system prompt that instructs the LLM to:

| Instruction | Detail |
|---|---|
| **Experience points** | Action-oriented, measurable impact, ATS-optimised, no personal pronouns |
| **Skills** | Reorder by relevance to the job, remove inapplicable ones |
| **Achievements** | Filter and include only role-relevant achievements |
| **Seniority level** | Auto-detected from experience requirements in the JD |
| **Cover letter** | Tailored, JSON-safe single-block format |

#### 3. LLM Call — `groq_api.groq_api_call()`

The prompt is sent to the Groq API (`llm_call/groq_api.py`) using streaming completions. The model returns a **JSON string** with the following keys:

```json
{
  "full_time_experience_points": ["..."],
  "internship_experience_points": ["..."],
  "mentoring_experience": ["..."],
  "skills": ["..."],
  "databases": ["..."],
  "cloud": ["..."],
  "achievements": ["..."],
  "cover_letter": "...",
  "job_title": "...",
  "company_name": "...",
  "job_seniority_level": "..."
}
```

#### 4. Save Outputs — `save_cv()`

`utils/cv_save.py` takes the parsed JSON and:

1. Creates a folder under `jobs_csv/<CompanyName>/`
2. Calls `doc_create.create_cv_docx()` → builds a formatted `.docx` CV using `python-docx`
3. Calls `doc_create.create_cover_letter_docx()` → builds a cover letter `.docx`
4. Converts both `.docx` files to **PDF** via `docx_2_pdf.docx_to_pdf()`
5. Dumps the full LLM JSON output to `job_metadata.json` for reference

---

## 🧠 `master_data/` — Source of Truth

| File | Purpose |
|---|---|
| `master_cv_context.txt` | Complete professional background — all work experience, skills, achievements, education. This is what the LLM uses to populate the tailored CV. |
| `job_description.txt` | Paste the full job description here before running `main.py`. |

> **Tip:** Keep `master_cv_context.txt` comprehensive and up to date. The LLM selects and reformats bullet points from this context — the richer it is, the better the output.

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
GROQ_KEY=your_groq_api_key_here
```

Get a free Groq API key from [console.groq.com](https://console.groq.com).

### Run CV Generation

1. Paste the job description into `master_data/job_description.txt`
2. Run the pipeline:

```bash
python main.py
```

3. Find your tailored CV, cover letter, and metadata in:

```
jobs_csv/<CompanyName>/
```

---

## 🔧 Configuration

All path constants live in `Config.py`:

```python
MASTER_CV_PATH       = 'master_data/master_cv_context.txt '
JOB_DESCRIPTION_PATH = 'master_data/job_description.txt'
LOG                  = False
```

---

## 📦 Key Dependencies

| Library | Purpose |
|---|---|
| `groq` | LLM API for CV generation |
| `python-docx` | `.docx` file creation |
| `streamlit` | Experimental UI |
| `python-dotenv` | Environment variable management |
| `requests` / `selenium` | Job board scraping |

---

## 📁 Output Example

After running `python main.py` for a role at **DeepMind**:

```
jobs_csv/
└── DeepMind/
    ├── Chaitanya Srikanth CV - DeepMind.docx
    ├── Chaitanya Srikanth CV - DeepMind.pdf
    ├── Cover Letter - DeepMind.docx
    ├── Cover Letter - DeepMind.pdf
    └── job_metadata.json
```
