import pandas as pd
from datetime import datetime
import os


def create_day_csv(job_search_results, output_dir='jobs_csv'):
    """
    Create a CSV file with job search results for the current day.
    
    Args:
        job_search_results (list): List of dictionaries containing job information
        output_dir (str): Directory to save the CSV file (default: 'job_results')
    
    Returns:
        str: Path to the created CSV file
    """
    # Get current date for filename
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Define the columns we want in the CSV
    columns = ['uuid', 'title', 'description', 'application_link', 'company', 'location']
    
    # Create an empty dataframe with the specified columns
    df = pd.DataFrame(columns=columns)
    
    # Iterate through job search results and add to dataframe
    for job in job_search_results:
        # Extract only the columns we need
        row_data = {
            'uuid': job.get('uuid', None),
            'title': job.get('title', None),
            'description': job.get('description', None),
            'application_link': job.get('application_link', None),
            'company': job.get('company', None),
            'location': job.get('location', None)
        }
        
        # Add the row to the dataframe using pd.concat (recommended over append)
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create the CSV filename with current date
    csv_filename = f"{output_dir}/jobs_{current_date}.csv"
    
    # Save to CSV
    df.to_csv(csv_filename, index=False)
    
    print(f"✅ CSV created successfully: {csv_filename}")
    print(f"📊 Total jobs saved: {len(df)}")
    
    return csv_filename
