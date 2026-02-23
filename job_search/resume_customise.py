import os
import pandas as pd 
from scraper_utils.web_scraper import scrape_url_auto
from llm_call import hugging_face_call 
import Config 

def read_master_csv_contents(txt_file_path):
    with open(txt_file_path, 'r') as file:
        file_content = file.read()
    return file_content



def job_description_scrape(dataframe):
    
    for index, row in dataframe.iterrows():
        url = row['application_link']
        master_cv_content = read_master_csv_contents(Config.MASTER_CV_PATH)
        
        print(f"\n{'='*60}")
        print(f"🔍 Processing job: {row.get('title', 'Unknown')}")
        print(f"{'='*60}")
        
        # Scrape the job description (now returns text directly)
        scraped_text = scrape_url_auto(url)
        print(scraped_text)
        if not scraped_text:
            print(f"⚠️ Failed to scrape URL: {url}")
            continue
        
        # Truncate to avoid token limits (keep first ~10,000 characters)
        # Most job descriptions are in the first part of the page
        MAX_CHARS = 10000
        truncated_text = scraped_text[:MAX_CHARS]
        
        print(f"📄 Scraped text length: {len(scraped_text)} chars")
        print(f"📝 Using first {min(len(scraped_text), MAX_CHARS)} chars for LLM")
        
        # Extract clean job description using LLM
        prompt_html_job_description = f'''
        Extract ONLY the job description from the following webpage text. 
        Focus on: job title, responsibilities, requirements, qualifications, and benefits.
        Ignore: navigation menus, footers, advertisements, and other jobs.
        
        Webpage text:
        {truncated_text}
        
        Provide a clean, structured job description.
        '''
        
        print("🤖 Extracting job description with LLM...")
        job_description_text = hugging_face_call.call_llm(prompt_html_job_description)
        print(f"✅ Job description extracted ({len(job_description_text)} chars)\n")

        prompt = f'''
        You are an expert in creating CVs for Job applications. My master CV contains the projects and the
        work experience I have. My current CV contains these contents {master_cv_content}. 
        This HTML scraped data contains the Job Role Description {job_description_text}.
        Based on the job description, make the changes in my CV contents aligned with the job role and give me the final text output. 
         
        My current CV explains my projects in a way that what work I have done and what profitted the company with numbers (65% efficient, 83% accuracy etc.)
        Follow the same format. Work -> Numbers achieved. 
        Ensure not to change the CV format content with lines. 
        
        '''
        job_description_refinement = hugging_face_call.call_llm(prompt)
        print(job_description_refinement)
        