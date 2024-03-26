Use merge_data.py for scraped data and capacity data

# GP Data Scraper

## Overview
The GP Data Scraper is a Python-based tool designed to automate the scraping of local GP provision information from the NHS website. This tool takes a UK postcode as input and outputs the corresponding GP data.

## Features
- **Input:** UK postcode 
- **Output:** An excel spreadsheet containing the relevant data (including practice name, distance from postcode, if its currently accepting new patients, patient to GP ratio etc)
- **Interface:** The tool is used via a simple CLI
- **Source:** Data is scraped directly from https://www.nhs.uk/service-search/find-a-gp/results and https://files.digital.nhs.uk/09/36F385/GPWPracticeCSV.092023.zip.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python 3.8 or higher
- Pip (Python package installer)
- Scrapy 


## Usage 

To scrape data from both sources and merge them into one locally saved file:
1. Ensure that all prerequisites are installed. 
2. Navigate to the parent 'MergedataGUI' directory 
3. Enter 'python merge_data.py postcode=input_postcode', replacing 'input_postcode' 

## Notes
- This project also contains files to create a GUI interface and to host a website locally (using the Flask framework)


