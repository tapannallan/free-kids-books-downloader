import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_book(url, folder):
    """Downloads a book from the given URL to the specified folder."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def main():
    """Main function to scrape and download books."""
    base_url = "https://freekidsbooks.org/age-group/stories-age-2-5-years/page/"
    download_folder = os.path.expanduser("~/Documents/Kids Books")

    for page_num in range(3, 50):
        page_url = f"{base_url}{page_num}/"
        print(f"Scraping page: {page_url}")
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            download_links = soup.find_all('a', class_='download-book my-post-like')
            for link in download_links:
                book_url = link.get('href')
                if book_url:
                    # The href is a relative URL, so we need to join it with the base URL
                    absolute_book_url = urljoin("https://freekidsbooks.org", book_url)
                    download_book(absolute_book_url, download_folder)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_url}: {e}")

if __name__ == "__main__":
    main()
