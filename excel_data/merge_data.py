import pandas as pd
import requests     
import numpy as np
import zipfile
import io
import sys
import os
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from scrapy.utils.project import get_project_settings



# Determine the path to the GPscraper project directory
data_scraper_path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper")

# Add the GPscraper project directory to the Python path
sys.path.append(data_scraper_path)
from GPscraper.spiders.GPspider import GpspiderSpider



def generate_url(postcode):
    return f"https://www.nhs.uk/service-search/find-a-gp/results/{postcode}"

 

# function that runs web scraper 
def crawl_spider(postcode):
    
# Initialize the CrawlerProcess with a complete path to the output file
    
    output_path = os.path.join(os.getcwd(), output_filename)

    settings = get_project_settings()
  
    # Modify the settings as needed
    settings.set("FEED_URI", output_path)  # Update the output file path
    settings.set("FEED_FORMAT" , "csv")
    settings.set("FEED_EXPORT_FIELDS" , ['name', 'miles_away', 'accepting_patients', 'in_catchment', 'gp_website', 'phone_number','gp_address'])

    # Initialize CrawlerProcess with your Scrapy project's settings
    process = CrawlerProcess(settings=settings)
    # Pass the spider class, not an instance
    process.crawl(GpspiderSpider, postcode=postcode)
    # Start the web scraping process
    process.start()


# function that reads and writes a downloaded excel spreadsheet
def write_excel():
    # URL of the zip file to load
    zip_file_url = 'https://files.digital.nhs.uk/09/36F385/GPWPracticeCSV.092023.zip'



    try:
        # Send a GET request to the URL and download the zip file
        response = requests.get(zip_file_url)
        response.raise_for_status()  # Check for any errors in the response


        # Create a ZipFile object from the downloaded content
        with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
            # List the files within the zip file
            file_list = zip_ref.namelist()
            print(file_list)

            # Choose the spreadsheet you want to extract 
            target_spreadsheet = '1 General Practice – September 2023 Practice Level - Detailed.csv'

            if target_spreadsheet in file_list:
                # Extract the target spreadsheet
                with zip_ref.open(target_spreadsheet) as spreadsheet_file:

                    # Read the CSV content and convert it to a DataFrame
                    df = pd.read_csv(spreadsheet_file)

                    # Save the DataFrame as an Excel file
                    df.to_excel('gp_practice_level_sept2023.xlsx', index=False)
            else:
                print(f"The target spreadsheet '{target_spreadsheet}' was not found in the zip file.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the zip file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# function to extract relevent data from excel file 
def extract_and_merge_data():

    data_scraper_path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper\excel_data\gp_practice_level_sept2023.xlsx")

    # Read the CSV file into a Pandas DataFrame
    df1 = pd.read_csv(output_filename)
    df2 = pd.read_excel(data_scraper_path, engine='openpyxl')

    # Specify the column name you want to extract
    column_name = 'name'

    # Access the column and convert it to a Python list
    gp_name_list = df1[column_name].tolist()

    gp_name_list = [name.upper() for name in gp_name_list]
  
    # # add new columns 
    # new_data = {
    # 'Region': [np.nan] * len(df1['name']),
    # 'PCN': [np.nan] * len(df1['name']),
    # 'Total_Patients': [np.nan] * len(df1['name']),
    # 'Total_GP_FTE': [np.nan] * len(df1['name']),
    # }
    
    #  # Combine the initial_data DataFrame with your existing df1
    # df1 = pd.concat([df1, pd.DataFrame(new_data)], axis=1)

    df1['Region'] = np.nan
    df1['PCN'] = np.nan
    df1['Total_Patients'] = np.nan
    df1['Total_GP_FTE'] = np.nan


    for name in gp_name_list:

        df2_row = df2[df2['PRAC_NAME'] == name]
        if not df2_row.empty:
            region = df2_row['REGION_NAME'].iloc[0]
            pcn = df2_row['PCN_NAME'].iloc[0]
            total_patients = df2_row['TOTAL_PATIENTS'].iloc[0]
            total_gp_fte = df2_row['TOTAL_GP_FTE'].iloc[0]

            # Update df1 with the extracted information
            df1.loc[df1['name'].str.upper() == name, 'Region'] = region
            df1.loc[df1['name'].str.upper() == name, 'PCN'] = pcn
            df1.loc[df1['name'].str.upper() == name, 'Total_Patients'] = total_patients
            df1.loc[df1['name'].str.upper() == name, 'Total_GP_FTE'] = total_gp_fte

        else:
            df1.loc[df1['name'].str.upper() == name, 'Region'] = 'Not available'
            df1.loc[df1['name'].str.upper() == name, 'PCN'] = 'Not available'
            df1.loc[df1['name'].str.upper() == name, 'Total_Patients'] = 'Not available'
            df1.loc[df1['name'].str.upper() == name, 'Total_GP_FTE'] = 'Not available'

        df1.to_csv('output_file1.csv', index=False)


# Get the current date
current_date = datetime.now()

# Format the date as "dd_mm_yy"
formatted_date = current_date.strftime("%d_%m_%y")

# Example postcode to use in the web scraper
postcode = 'bs82aa'

output_filename = f"{postcode}_{formatted_date}.csv"

# Run the web scraper
crawl_spider(postcode)

# Extract data from the downloaded Excel file
write_excel()

extract_and_merge_data()