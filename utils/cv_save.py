import os 
from utils.doc_create import create_cv_docx
import json 
    
def save_cv(json_output):
    # Create new directory for the job if it doesn't exist
    company_name = json_output.get("company_name", "Unnamed_Job").replace(" ", "_").replace("/", "_")
    job_dir = os.path.join('jobs_csv', company_name)


    if not os.path.exists(job_dir):
        os.mkdir(job_dir)

    file_name = f"Chaitanya Srikant CV - {company_name}"
    file_name = os.path.join(job_dir, f"{file_name}.docx")

    create_cv_docx(json_output, file_name)
    print(f"✅ CV saved to {file_name}")

    with open(os.path.join(job_dir, 'job_metadata.json'), 'w') as f:
        json.dump(json_output, f, indent=4)
    
    print(f'JSON Dumped to {os.path.join(job_dir, "job_metadata.json")}')


    return file_name 