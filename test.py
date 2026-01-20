# from job_search import ireland_jobs 
# from utils import csv_creater 

# results = ireland_jobs.main()
# csv_creater.create_day_csv(results)

# from job_search.resume_customise import job_description_scrape
# import pandas as pd 


# df = pd.read_csv('jobs_csv/jobs_2026-01-16.csv')
# job_description_scrape(df)

from llm_call import groq_api
import Config 
import time 

# groq_api.groq_api_call('Hello Groq')

'''
Docstring for test
Finish Scraping for Trackr, Ireland jobs, and create CSVs for them. 
Post that, use groq api to test the RPM and adjust the code with timeouts.
Create .txt files for each job role 



'''

from scraper_utils.crawler import start_async_crawl, start_job_crawl
job_links = start_async_crawl('https://www.irishjobs.ie/jobs/data-scientist?searchOrigin=membersarea&q=data%20scientist%20')







with open(Config.MASTER_CV_PATH, 'r') as file:
    master_cv_content = file.read()
print(master_cv_content)

def create_prompt(job_description, master_cv_content):

    main_prompt = f'''
    You are an expert job application assistant. Based on the following job description,
    Job Description : {job_description}, create a tailored CV for the applicant. The applicant's master CV contains the following information: {master_cv_content}.
    Please ensure the CV highlights relevant skills and experiences that align with the job requirements. 
    The applicant follows the structure of work done and the achievements in a quantitve manner. (e.g., "Increased sales by 20%" rather than just "Responsible for sales").
    Provide the final CV text output. Ensure to have the same CV structure and don't add extra textual headings. Just edit the Job experience contents points only.
    '''
    return main_prompt

for jl in job_links:
    output = start_job_crawl(jl)
    #### These jobs were popular with other job seekers
    job_description = output.split('#### These jobs were popular with other job seekers')[0]
    prompt = create_prompt(job_description, master_cv_content)
    output = groq_api.groq_api_call(prompt = prompt)
    print(output)
    print(f'--- ' * 30)
    time.sleep(10)
    break 
# print(job_links)