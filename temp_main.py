from llm_call import groq_api
import Config 
import json 
from utils.cv_save import save_cv




def create_prompt(job_description, master_cv_content):

    main_prompt  = f'''
        You are an expert job application assistant. Based on the following job description,
        Job Description: {job_description}, create a tailored CV for the applicant. The applicant's master CV contains the following information: {master_cv_content}

        Use UK English to fill the CV contents. 

        Create the CV in a style optimized for ATS, following VMock recommendations. Focus only on editing the job experience content points. Do not add extra textual headings or sections

        Guidelines:

        1. Experience Points:
        - Each point should be action-oriented, demonstrating analytical ability, communication, leadership, teamwork, and initiative
        - Highlight measurable impact wherever possible (e.g., "Increased sales by 20%" instead of "Responsible for sales")
        - Avoid passive language, personal pronouns, filler words, and repetitive verbs
        - No full-stops at the end of each point
        - Use diverse strong verbs to convey ownership, achievement, and results
        - Align experience points closely with the job description to maximize selectability
        - Full-time experience: max 4-5 points
        - Internship experience: max 3-4 points
        - Mentoring experience: 1 point

        2. Skills:
        - Keep the three sections as is: Skills, Databases, Cloud
        - Include only relevant skills mentioned in the experience points
        - Rearrange skills in priority order based on the job description
        - Remove any skill not applicable to the job role

        3. Achievements:
        - Include only relevant achievements for the job role
        - Highlight quantifiable or high-impact achievements
        - Do not mention my Google ML certification
        - Do not mention about any merit scholarships

        4. Job Seniority Level:
        - If job requires >2 years experience → "Experienced"
        - If job requires 1-2 years experience → "Graduate Scheme"
        - If job requires <1 year experience → "Entry Level" or "Internship" as appropriate

        5. Cover Letter:
        - Create a tailored cover letter for the same job role
        - Ensure proper formatting in a single textual format suitable for JSON output

        6. Output Format (as a dictionary with following keys):
        
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
            "skills": [
                "Skill 1",
                "Skill 2",
                ...
            ],
            "databases": [
                "Database 1",
                "Database 2",
                ...
            ],
            "cloud": [
                "Cloud 1",
                "Cloud 2",
                ...
            ],
            "mentoring_experience": [
                "Point 1"
            ],
            "achievements": [
                "Achievement 1",
                "Achievement 2"
            ],
            "cover_letter": "<Created Cover Letter for the Job Role>",
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

 