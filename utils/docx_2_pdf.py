import subprocess
from pathlib import Path

def docx_to_pdf(docx_path, output_dir=None):
    docx_path = Path(docx_path).resolve()

    if output_dir is None:
        output_dir = docx_path.parent
    else:
        output_dir = Path(output_dir).resolve()

    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(docx_path)
    ], check=True)

# Usage
docx_to_pdf("Chaitanya_Srikanth_CV.docx")