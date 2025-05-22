import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from tqdm import tqdm
from utils import replace_puzzle_images, save_puzzle_data
import os
from utils import DATA_DIR_JS

BASE_URL = "https://www.janestreet.com"
BASE_PUZZLE_URL = "https://www.janestreet.com/puzzles/archive/page{page_num}/index.html"

def scrape_puzzle_links(page_num):
    url = BASE_PUZZLE_URL.format(page_num=page_num)
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    puzzle_links = []
    solution_links = []
    
    # Find all links on the page
    links = soup.find_all('a')
    
    for link in links:
        href = link.get('href')
        text = link.get_text().strip()
        
        if text.lower() == "puzzle":
            puzzle_links.append(href)
        elif text.lower() == "solution":
            solution_links.append(href)
            
    return puzzle_links, solution_links

def download_images(soup, BASE_URL, output_dir):
    images = soup.find_all('img')
    downloaded = []
    
    for i, img in enumerate(images):
        src = img.get('src')
        if src:
            if not src.startswith(('http://', 'https://')):
                src = BASE_URL + src
                
            # Use sequential numbering for filename
            ext = os.path.splitext(src)[1]
            filename = f"{i}{ext}"
            
            # Download image
            img_response = requests.get(src)
            if img_response.status_code == 200:
                img_path = os.path.join(output_dir, filename)
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                downloaded.append(filename)
                
                # Update image src in markdown to use sequential numbering
                img['src'] = f'/puzzles/{i}{ext}'
                
    return downloaded


def scrape_puzzle_data(puzzle_links, solution_links):
    puzzle_data = []

    for puzzle_link, solution_link in tqdm(zip(puzzle_links, solution_links), total=len(puzzle_links), desc='Pulling puzzles'):
        puzzle_url = BASE_URL + puzzle_link
        solution_url = BASE_URL + solution_link
        
        # Get content
        puzzle_response = requests.get(puzzle_url)
        puzzle_response.encoding = 'utf-8'
        puzzle_soup = BeautifulSoup(puzzle_response.text, 'html.parser')
        
        solution_response = requests.get(solution_url)
        solution_response.encoding = 'utf-8'
        solution_soup = BeautifulSoup(solution_response.text, 'html.parser')

        # Extract content
        puzzle_container = puzzle_soup.find('div', class_='container')
        if puzzle_container:
            puzzle_header = puzzle_container.find('div', class_='puzzle-header')
            if puzzle_header:
                puzzle_header.decompose()
            puzzle_content = puzzle_container.decode_contents()
        else:
            puzzle_content = ""

        solution_container = solution_soup.find('div', class_='container')
        if solution_container:
            solution_header = solution_container.find('div', class_='puzzle-header')
            if solution_header:
                solution_header.decompose()
            solution_content = solution_container.decode_contents()
        else:
            solution_content = ""

        puzzle_name = puzzle_url.split('/')[-2]

        puzzle_img_dir = os.path.join(DATA_DIR_JS, 'problem', 'images', puzzle_name)
        solution_img_dir = os.path.join(DATA_DIR_JS, 'solution', 'images', puzzle_name)
        os.makedirs(puzzle_img_dir, exist_ok=True)
        os.makedirs(solution_img_dir, exist_ok=True)

        puzzle_images = download_images(puzzle_container, BASE_URL, puzzle_img_dir) if puzzle_container else []
        solution_images = download_images(solution_container, BASE_URL, solution_img_dir) if solution_container else []

        puzzle_content = md(puzzle_content, newline_style='backslash')
        solution_content = md(solution_content, newline_style='backslash')

        puzzle_content = puzzle_content.replace('\\*', '*')
        solution_content = solution_content.replace('\\*', '*')

        puzzle = {
            'puzzle_name': puzzle_name,
            'puzzle_url': puzzle_url,
            'solution_url': solution_url,
            'puzzle_content': puzzle_content,
            'solution_content': solution_content,
            'puzzle_images': puzzle_images,
            'solution_images': solution_images
        }

        puzzle = replace_puzzle_images(puzzle)

        puzzle_data.append(puzzle)

    return puzzle_data


if __name__ == '__main__':
    puzzle_links = []
    solution_links = []
    for i in range(2, 14):
        p_links, s_links = scrape_puzzle_links(i)
        puzzle_links.extend(p_links)
        solution_links.extend(s_links)

    # puzzle_links, solution_links = (['/puzzles/sum-one-somewhere-index/', '/puzzles/altered-states-2-index/'], ['/puzzles/sum-one-somewhere-solution', '/puzzles/altered-states-2-solution'])

    puzzle_data = scrape_puzzle_data(puzzle_links, solution_links)
    print(f"Scraped {len(puzzle_data)} puzzle/solution pairs")
    save_puzzle_data(puzzle_data, DATA_DIR_JS)