import os 
from utils.doc_create import create_cv_docx , create_cover_letter_docx
import json 
from utils import docx_2_pdf
    
def save_cv(json_output):
    # Create new directory for the job if it doesn't exist
    company_name = json_output.get("company_name", "Unnamed_Job").replace(" ", "_").replace("/", "_")
    job_dir = os.path.join('jobs_csv', company_name)


    if not os.path.exists(job_dir):
        os.mkdir(job_dir)

    file_name = f"Chaitanya Srikanth CV - {company_name}"
    file_name = os.path.join(job_dir, f"{file_name}.docx")
    cv_file_name = os.path.join(job_dir, f"Cover Letter - {company_name}.docx")
    create_cv_docx(json_output, file_name)
    create_cover_letter_docx(json_output.get("cover_letter", ""), cv_file_name)

   
    docx_2_pdf.docx_to_pdf(file_name, job_dir)
    docx_2_pdf.docx_to_pdf(cv_file_name, job_dir)

    print(f"✅ CV saved to {file_name}")

    with open(os.path.join(job_dir, 'job_metadata.json'), 'w') as f:
        json.dump(json_output, f, indent=4)



    
    print(f'JSON Dumped to {os.path.join(job_dir, "job_metadata.json")}')

    os.remove(file_name)
    os.remove(cv_file_name)


    return file_name 