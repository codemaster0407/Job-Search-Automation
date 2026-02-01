from llm_call import groq_api
import Config 
import json 
from utils.cv_save import save_cv




def create_prompt(job_description, master_cv_content):

    main_prompt = f'''
    You are an expert job application assistant. Based on the following job description,
    Job Description : {job_description}, create a tailored CV for the applicant. The applicant's master CV contains the following information: {master_cv_content}.
    Please ensure the CV highlights relevant skills and experiences that align with the job requirements. 
    The applicant follows the structure of work done and the achievements in a quantitve manner. 
    (e.g., "Increased sales by 20%" rather than just "Responsible for sales").
    Provide the final CV text output. Ensure to have the same CV structure and don't add extra textual headings.
    Just edit the Job experience contents points only.

    Try to align the job experience points to the job description provided to maximise my selectability for the job role using my full experience and select only relevant experience for the job role.
    Moreover, ensure the CV is concise and don't add tech stack or skills section if I don't possess those skills.
    Try to maximise the alignment of the CV to the job description provided without adding skills or experiences I don't have.
    Ensure to keep the maximum number of points in the experience sections as 4 points for full time and 3 points for internship experience. 1 point for mentorship experience.
    I have divided the skills into three sections : Skills, Databases, Cloud. 
    Make sure to keep those sections as it is without adding any extra skills I don't have and rearrange them in the priority based on the job description. If the skill is not required for the job role, make sure to remove it from the output.
    I'm a recent graduate so ensure to fill the job_seniority_level as "Entry Level" , "Graduate Scheme" , "Experienced" or "Internship".
    If the job requires more than 2 years of experience, mark it as "Experienced", if it requires 1-2 years of experience, mark it as "Graduate Scheme",
    if it requires less than 1 year of experience, mark it as "Entry Level".


    For the same Job role , create a customised Cover letter with proper formatting in a single textual format which I can access in the JSON object with proper formatting

    Even for the achievements, only choose the relevant achievements for the job role
    Return the output in the following format as a JSON Object 
        "full_time_experience_points": [
            "Point 1",
            "Point 2",
            ...
        ],
        "internship_experience_points": [
            "Point 1",
            "Point 2",
            ...
        ], 
        "skills" : [
            "Skill 1",
            "Skill 2",
            ...
        ],
        "databases" : [
            "Database 1",
            "Database 2",
            ...
        ], 
        "mentoring_experience" : [
        "point 1"
        ], 
        "achievements" : [
        "achievement 1", 
        "achievement 2"
        ]

        "cover_letter" : "<Created Cover Letter for the Job Role>",
        "job_title": "<Extracted Job Role Title from the job description>", 
        "company_name": "<Extracted Company Name from the job description>",
        "job_seniority_level": "<Extracted Seniority Level from the job description>"
    '''
    return main_prompt

# for jl in job_links:
#     output = start_job_crawl(jl)
#     #### These jobs were popular with other job seekers
# job_description = output.split('#### These jobs were popular with other job seekers')[0]

# Copy paste Job Description Here....

with open(Config.JOB_DESCRIPTION_PATH, 'r') as file:
    job_description = file.read()


with open(Config.MASTER_CV_PATH, 'r') as file:
    master_cv_content = file.read()



prompt = create_prompt(job_description, master_cv_content)
output = groq_api.groq_api_call(prompt = prompt)

print(output)
llm_json_output = json.loads(output)
# print(llm_json_output)
save_cv(llm_json_output)

 