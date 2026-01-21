import json 
from utils.doc_create import create_cv_docx

output  = '''
{
  "full_time_experience_points": [
    "Designed and deployed an AI‑driven medical product scanning solution, cutting documentation time by up to 85% (from 20 s to 3 s) and boosting operating‑room efficiency",
    "Built scalable Python data pipelines for image ingestion, cleaning and transformation; automated reporting dashboards that reduced cloud API costs by 65% while delivering real‑time accuracy metrics",
    "Implemented object‑detection and OCR models reaching 92% extraction accuracy and integrated them via FastAPI, supporting >10 k daily scans with high reliability",
    "Led cross‑functional delivery by coordinating client requirements, DevOps, backend and frontend teams, ensuring on‑time launch and maintaining data quality and performance"
  ],
  "internship_experience_points": [
    "Engineered a product onboarding pipeline that accelerated computer‑vision model training from several hours to 10‑15 minutes while preserving ~80% accuracy through ensemble and few‑shot learning techniques",
    "Developed a real‑time inventory visibility system using Python/Flask; decreased stock‑out incidents by 45% by providing up‑to‑the‑minute stock dashboards for managers",
    "Automated data extraction, preprocessing and model orchestration, cutting manual data‑preparation effort by 70% and enabling rapid model iteration",
    "Collaborated with data‑engineering and analytics teams to create monitoring dashboards that highlighted model drift and usage trends, informing continuous improvement"
  ]
}'''
print(output)
llm_json_output = json.loads(output)
create_cv_docx(llm_json_output,  file_name = f"wtf.docx")