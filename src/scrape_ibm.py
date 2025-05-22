import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from tqdm import tqdm
import os
from datetime import datetime, timedelta
from utils import DATA_DIR_IBM, save_puzzle_data

BASE_URL = "https://research.ibm.com/haifa/ponderthis"
PUZZLE_URL = BASE_URL + "/challenges/{month}{year}.html"
SOLUTION_URL = BASE_URL + "/solutions/{month}{year}.html"

def get_date_range():
    start_date = datetime(1998, 5, 1)  # May 1998
    end_date = datetime(2025, 5, 1)    # May 2025
    
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=32) # Move to next month
        current_date = current_date.replace(day=1)
    
    return dates


def scrape_puzzle_data(dates):
    puzzle_data = []

    for date in tqdm(dates, desc='Pulling puzzles'):
        month = date.strftime("%B")
        year = date.strftime("%Y")
        
        # Get puzzle content
        puzzle_url = PUZZLE_URL.format(month=month, year=year)
        puzzle_response = requests.get(puzzle_url)
        if puzzle_response.status_code != 200:
            continue
            
        puzzle_response.encoding = 'utf-8'
        puzzle_soup = BeautifulSoup(puzzle_response.text, 'html.parser')
        
        # Get solution content
        solution_url = SOLUTION_URL.format(month=month, year=year)
        solution_response = requests.get(solution_url)
        if solution_response.status_code != 200:
            continue
            
        solution_response.encoding = 'utf-8'
        solution_soup = BeautifulSoup(solution_response.text, 'html.parser')

        # Extract main content
        puzzle_content = puzzle_soup.find('body')
        solution_content = solution_soup.find('body')

        if not puzzle_content or not solution_content:
            continue

        # Convert to markdown
        puzzle_md = md(str(puzzle_content))
        solution_md = md(str(solution_content))

        puzzle = {
            'puzzle_name': f"{month}-{year}",
            'puzzle_url': puzzle_url,
            'solution_url': solution_url,
            'puzzle_content': puzzle_md,
            'solution_content': solution_md
        }

        puzzle_data.append(puzzle)

    return puzzle_data


if __name__ == '__main__':
    dates = get_date_range()
    puzzle_data = scrape_puzzle_data(dates)
    print(f"Scraped {len(puzzle_data)} puzzle/solution pairs")
    save_puzzle_data(puzzle_data, DATA_DIR_IBM)