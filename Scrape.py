import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Define the URL of the HackerRank page to scrape
url = 'https://www.hackerrank.com/domains/data-structures'

# Set up headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Send a GET request to the webpage with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize a list to store the scraped data
        problem_data = []

        # Find the relevant elements that contain problem titles and URLs
        problems = soup.find_all('a', class_='js-track-click challenge-list-item')

        # Loop through each problem element and extract the title, link, and description
        for problem in problems:
            title = problem.get_text(strip=True)
            link = problem['href']
            problem_url = f"https://www.hackerrank.com{link}"

            # Make a request to the individual problem page to get the description
            problem_response = requests.get(problem_url, headers=headers)
            if problem_response.status_code == 200:
                problem_soup = BeautifulSoup(problem_response.content, 'html.parser')
                description_tag = problem_soup.find('div', class_='challenge-text')
                description = description_tag.get_text(strip=True) if description_tag else "No description found"
            else:
                description = "Failed to retrieve description"

            # Append the data to the list
            problem_data.append({'Title': title, 'URL': problem_url, 'Description': description})

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
    else:
        print('Failed to retrieve the webpage. Status code:', response.status_code)
except PermissionError:
    print(f"PermissionError: You don't have permission to write to the specified location: {output_file}")
except Exception as e:
    print(f'An error occurred: {e}')
