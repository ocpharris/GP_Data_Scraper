import argparse
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

#
#
#
#
import multiprocessing
#
#
#
#





# Determine the path to the GPscraper project directory
data_scraper_path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper")

# Add the GPscraper project directory to the Python path
sys.path.append(data_scraper_path)
from GPscraper.spiders.GPspider import GpspiderSpider


def __init__(self, postcode, *args, **kwargs):
    super(GpspiderSpider, self).__init__(*args, **kwargs)
    self.postcode = postcode


def generate_url(postcode):
    return f"https://www.nhs.uk/service-search/find-a-gp/results/{postcode}"

 

# function that runs web scraper 
def crawl_spider(postcode, formatted_date):
    
# Initialize the CrawlerProcess with a complete path to the output file

    output_filename = f"{postcode}_{formatted_date}.csv"
    
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


#
#
#
# for flask
def run_crawl_spider(postcode, formatted_date):
    p = multiprocessing.Process(target=crawl_spider, args=(postcode, formatted_date))
    p.start()
    p.join()
#
#
#
#





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
def extract_and_merge_data(postcode, formatted_date):

    data_scraper_path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper\MergedataGUI\flask\gp_practice_level_sept2023.xlsx")

    output_filename = f"{postcode}_{formatted_date}.csv"

    # Read the CSV file into a Pandas DataFrame
    df1 = pd.read_csv(output_filename)
    df2 = pd.read_excel(data_scraper_path, engine='openpyxl')

    # Specify the column name you want to extract
    column_name = 'name'

    # Access the column and convert it to a Python list
    gp_name_list = df1[column_name].tolist()

    gp_name_list = [name.upper() for name in gp_name_list]
  

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

        merged_gp_data = f"gp_data_{postcode}_{formatted_date}.csv"
        df1.to_csv(merged_gp_data, index=False)



def main(postcode):

    # Get the current date
    current_date = datetime.now()

    # Format the date as "dd_mm_yy"
    formatted_date = current_date.strftime("%d_%m_%y")
    
    # Run the web scraper
    crawl_spider(postcode, formatted_date=formatted_date)

    # Extract data from the downloaded Excel file
    write_excel()
    extract_and_merge_data(postcode, formatted_date=formatted_date)



#
#
#
#
# for flask 
def start_scrapy_process(postcode, formatted_date):
    process = multiprocessing.Process(target=crawl_spider, args=(postcode,), kwargs={'formatted_date': formatted_date})
    process.start()
    process.join()

def main_flask(postcode):
    # Get the current date
    current_date = datetime.now()

    # Format the date as "dd_mm_yy"
    formatted_date = current_date.strftime("%d_%m_%y")

        # Run the web scraper in a separate process
    start_scrapy_process(postcode, formatted_date)

    # Extract data from the downloaded Excel file
    write_excel()
    extract_and_merge_data(postcode, formatted_date=formatted_date)
#
#
#
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GP Data Scraper")
    parser.add_argument("postcode", type=str, help="Specify the postcode")

    args = parser.parse_args()
    main(args.postcode)



