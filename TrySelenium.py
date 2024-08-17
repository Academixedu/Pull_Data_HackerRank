from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
driver_service = Service('/path/to/chromedriver')  # Adjust this path

def scrape_hackerrank():
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        
        problem_data = []
        question_number = 1
        page_number = 1
        
        while True:
            # Construct the URL for the current page
            url = f'https://www.hackerrank.com/domains/data-structures?page={page_number}'
            print(f'Fetching URL: {url}')
            driver.get(url)
            time.sleep(2)  # Wait for the page to load
            
            # Find the relevant elements that contain problem titles and URLs
            problems = driver.find_elements(By.CLASS_NAME, 'js-track-click')
            print(f'Found {len(problems)} problems on page {page_number}.')
            
            # Break if there are no problems found on the current page
            if not problems:
                print(f'No more problems found on page {page_number}. Exiting...')
                break
            
            for problem in problems:
                title = problem.text
                link = problem.get_attribute('href')
                
                # Print the question number, page number, and title
                print(f'Fetching Question {question_number} from Page {page_number}: {title}')

                # Fetch the problem description by navigating to the problem's page
                driver.get(link)
                time.sleep(2)  # Wait for the problem page to load
                description = driver.find_element(By.CLASS_NAME, 'challenge-text').text
                
                # Append the data to the list
                problem_data.append({'Title': title, 'URL': link, 'Description': description})

                question_number += 1
            
            # Move to the next page
            page_number += 1

        # Convert the data to a DataFrame
        df = pd.DataFrame(problem_data)

        # Ensure a different file name to avoid conflicts
        output_file = 'D:/GitTest/hackerrank_problems_with_description.csv'

        # Check if the file exists and if not, create it
        if os.path.exists(output_file):
            os.remove(output_file)  # Remove the existing file to avoid conflicts

        # Save the data to a CSV file
        df.to_csv(output_file, index=False)

        print(f'Data has been scraped and saved to {output_file}')
        
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        driver.quit()  # Close the WebDriver

# Run the scraping function
scrape_hackerrank()
