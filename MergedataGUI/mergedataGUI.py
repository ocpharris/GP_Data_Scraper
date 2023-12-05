
import tkinter as tk
from tkinter import ttk

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



# # Redirect standard output and error to a log file
# sys.stdout = open('stdout.log', 'w')
# sys.stderr = open('stderr.log', 'w')



# Determine the path to the GPscraper project directory
data_scraper_path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper")

# Add the GPscraper project directory to the Python path
sys.path.append(data_scraper_path)
# from GPscraper.spiders.GPspider import GpspiderSpider

# for running locally, uncomment line below 
# from merge_data import main

#for standalone exe, uncomment line below
from standalone_exec_gp_gui import main 





def generate_url(postcode):
    return f"https://www.nhs.uk/service-search/find-a-gp/results/{postcode}"

 

# Get the current date
current_date = datetime.now()

# Format the date as "dd_mm_yy"
formatted_date = current_date.strftime("%d_%m_%y")



def scrape_data_button():
    postcode  = postcode_entry.get()
    


    try:
        # # Perform the scraping
        # process.start()
        main(postcode=postcode)

        merged_gp_data = f"gp_data_{postcode}_{formatted_date}.csv"
        
        output_file = rf'C:\Users\oharris\Repos\GP_Data_Scraper\MergedataGUI\{merged_gp_data}'



        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Complete.")

        # Open the output file using the default program
        os.startfile(output_file)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
    result_text.config(state=tk.DISABLED)




def set_navy_blue_and_white_style():
    style.configure("TLabel", background="navy", foreground="white")
    style.configure("TButton", background="navy", foreground="white")
    style.configure("TEntry", background="white", foreground="navy")

app = tk.Tk()
app.title("Get GP Data")

style = ttk.Style()


# Set the initial style to navy blue and white
set_navy_blue_and_white_style()


# Configure the main window background
app.configure(bg="navy")

# Add a field for entering the postcode
postcode_label = ttk.Label(app, text="Enter Postcode:")
postcode_label.pack()
postcode_entry = ttk.Entry(app)
postcode_entry.pack()

# # Create input fields and labels
# url_label = tk.Label(app, text="Enter postcode (no spaces eg sw1v2le):")
# url_label.pack()
# url_entry = tk.Entry(app)
# url_entry.pack()

# Create a button to trigger scraping
scrape_button = ttk.Button(app, text="Go", command=scrape_data_button)
scrape_button.pack()

# Create a text widget to display results
result_text = tk.Text(app, wrap=tk.WORD, height=10, width=40)
result_text.pack()
result_text.config(state=tk.DISABLED)  # Set text widget to read-only

app.mainloop()
