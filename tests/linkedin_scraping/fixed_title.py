from concurrent.futures import ThreadPoolExecutor
import json
import re
import requests
from bs4 import BeautifulSoup
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

def load_json_data(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading JSON file: {e}")
        return None

def get_title_name(query):
    """Get title and workplace name from LinkedIn profile using Bing search."""
    result = re.search(r"/in/([^/?]+)", query)
    if not result:
        return "Not found", None

    query = result.group(1) + ' linkedin'
    try:
        response = requests.get('https://www.bing.com/search', params={'q': query})
        response.raise_for_status()
        return parse_html(response.text)
    except Exception as e:
        logging.error(f"Error in get_title_name: {e}")
        return None, None

def parse_html(html_content):
    """Parse HTML content to extract information."""
    soup = BeautifulSoup(html_content, 'html.parser')
    works_for, title = extract_works_for(soup), extract_title(soup)
    return title, works_for

def extract_works_for(soup):
    """Extract 'Works For' information."""
    try:
        works_for = None
        works_for_span = soup.find('span', title=lambda x: x and x.startswith('Works For:'))
        if works_for_span:
            works_for = works_for_span['title'].replace('Works For:', '').strip()

        # Method 2
        if not works_for:
            works_for_div = soup.find('strong', text='Works For:').parent
            if works_for_div:
                works_for = works_for_div.get_text(strip=True).replace('Works For:', '').strip()

        return works_for
    except Exception as e:
        logging.error(f"Error in extract_works_for: {e}")
        return None

def extract_title(soup):
    """Extract 'Title' information."""
    try:
        title = None
        # Try to find "Title"
        title_div = soup.find('strong', text='Title:')
        if title_div:
            title = title_div.get_text(strip=True).replace('Title:', '').strip()

        # Try to find "Job Title" if "Title" is not found
        if not title:
            job_title_span = soup.find('strong', text=lambda text: text and 'Job Title' in text)
            if job_title_span:
                job_title_container = job_title_span.parent
                if job_title_container:
                    job_title_text = job_title_container.get_text(strip=True)
                    if ':' in job_title_text:
                        title = job_title_text.split(':', 1)[1].strip()

        if not title:
            # Extract "Job Title"
            job_title_div = soup.find('strong', text='Occupation:')
            # print(job_title_div)
            if job_title_div:
                title = job_title_div.find_next_sibling(text=True).strip()

        return title
    except Exception as e:
        logging.error(f"Error in extract_title: {e}")
        return None

def update_json_data(item):
    """Update JSON data with scraped information."""
    title, works_for = get_title_name(item["ActualLinkedIn"])
    if title or works_for:
        item["LinkedIn Title"] = title
        item["working for"] = works_for
    return item

def main():
    """Main function to update JSON data with LinkedIn information."""
    file_path = 'tests/linkedin_scraping/title_working_for.json'
    json_data = load_json_data(file_path)
    if json_data:
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(update_json_data, json_data))

        updated_json_data_with_actual_linkedin = json.dumps(results, indent=4)
        try:
            with open('title_worksfor.json', 'w') as file:
                file.write(updated_json_data_with_actual_linkedin)
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

        logging.info('Finished updating JSON data with LinkedIn links.')

if __name__ == "__main__":
    main()
