# # app.py
# from flask import Flask, render_template, request, send_file
# import sys
# import os
# from datetime import datetime

# # Get the current date
# current_date = datetime.now()

# # Format the date as "dd_mm_yy"
# formatted_date = current_date.strftime("%d_%m_%y")

# # Determine the path to the GPscraper project directory
# path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper\MergedataGUI")

# # Add the GPscraper project directory to the Python path
# sys.path.append(path)
# from merge_data_flask import run_crawl_spider, main_flask



# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     postcode = request.form['postcode']
#     run_crawl_spider(postcode, formatted_date="")
#     return "Scraping initiated. Check logs for progress."

# @app.route('/process', methods=['POST'])
# def process():
#     postcode = request.form['postcode']
#     main_flask(postcode)
#     return "Data extraction and merging complete."

# if __name__ == '__main__':
#     app.run(debug=True)



# @app.route('/process', methods=['POST'])
# def process():
#     postcode = request.form['postcode']
#     main_flask(postcode)

#     # Instead of starting a download immediately, provide a link to trigger the download
#     download_link = f"/download/{postcode}"

#     return f"Data extraction and merging complete. Download your file <a href='{download_link}'>here</a>."

# @app.route('/download/<postcode>', methods=['GET'])
# def download(postcode):
#     # Form the filename based on the provided postcode
#     filename = f"gp_data_{postcode}_{formatted_date}.csv"
#     filepath = os.path.join(os.getcwd(), filename)

#     # Send the file as a response for the user to download
#     return send_file(filepath, as_attachment=True)

















# # app.py
# from flask import Flask, render_template, request, send_file
# import sys
# import os
# from datetime import datetime


# app = Flask(__name__)

# # Get the current date
# current_date = datetime.now()

# # Format the date as "dd_mm_yy"
# formatted_date = current_date.strftime("%d_%m_%y")

# # Determine the path to the GPscraper project directory
# path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper\MergedataGUI")

# # Add the GPscraper project directory to the Python path
# sys.path.append(path)

# from merge_data_flask import run_crawl_spider, main_flask

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     postcode = request.form['postcode']
#     run_crawl_spider(postcode, formatted_date="")
#     return "Scraping initiated. Check logs for progress."

# @app.route('/process', methods=['POST'])
# def process():
#     postcode = request.form['postcode']
#     main_flask(postcode)

#     # Instead of starting a download immediately, provide a link to trigger the download
#     download_link = f"/download/{postcode}"

#     return f"Data extraction and merging complete. Download your file <a href='{download_link}'>here</a>."

# @app.route('/download/<postcode>', methods=['GET'])
# def download(postcode):
#     # Form the filename based on the provided postcode
#     filename = f"gp_data_{postcode}_{formatted_date}.csv"
#     filepath = os.path.join(os.getcwd(), filename)

#     # Send the file as a response for the user to download
#     return send_file(filepath, as_attachment=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)















from flask import Flask, render_template, request, send_file
import sys
import os
from datetime import datetime

app = Flask(__name__)

# Get the current date
current_date = datetime.now()
# Format the date as "dd_mm_yy"
formatted_date = current_date.strftime("%d_%m_%y")

# Determine the path to the GPscraper project directory
path = os.path.abspath(r"C:\Users\oharris\Repos\GP_Data_Scraper\MergedataGUI")
# Add the GPscraper project directory to the Python path
sys.path.append(path)
from merge_data_flask import run_crawl_spider, main_flask

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    postcode = request.form['postcode']
    run_crawl_spider(postcode, formatted_date="")
    return "Scraping initiated. Check logs for progress."

@app.route('/process', methods=['POST'])
def process():
    postcode = request.form['postcode']
    main_flask(postcode)

    # Instead of starting a download immediately, provide a link to trigger the download
    download_link = f"/download/{postcode}"

    return f"Data extraction and merging complete. Download your file <a href='{download_link}'>here</a>."

@app.route('/download/<postcode>', methods=['GET'])
def download(postcode):
    # Form the filename based on the provided postcode
    filename = f"gp_data_{postcode}_{formatted_date}.csv"
    filepath = os.path.join(os.getcwd(), filename)

    # Send the file as a response for the user to download
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
