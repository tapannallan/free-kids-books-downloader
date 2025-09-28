import os
import requests
import subprocess
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pypdf import PdfReader, PdfWriter

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

def download_files():
    """Scrapes and downloads books."""
    base_url = "https://freekidsbooks.org/age-group/stories-age-2-5-years/page/"
    download_folder = os.path.expanduser("~/Documents/Kids Books")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

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
                    absolute_book_url = urljoin("https://freekidsbooks.org", book_url)
                    download_book(absolute_book_url, download_folder)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_url}: {e}")

def process_files():
    """Processes downloaded PDF files."""
    download_folder = os.path.expanduser("~/Documents/Kids Books")
    edited_folder = os.path.join(download_folder, "edited")

    if not os.path.exists(edited_folder):
        os.makedirs(edited_folder)

    for filename in os.listdir(download_folder):
        if filename.endswith(".pdf") and not filename.endswith("_processed.pdf") and not filename.endswith("_skipped.pdf"):
            original_filepath = os.path.join(download_folder, filename)
            
            # Open the PDF
            try:
                if sys.platform == "win32":
                    os.startfile(original_filepath)
                elif sys.platform == "darwin":
                    subprocess.run(["open", original_filepath], check=True)
                else:
                    subprocess.run(["xdg-open", original_filepath], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"Error opening {original_filepath}: {e}")
                continue

            # Get user input for pages
            pages_input = input(f"Enter pages for {filename} (e.g., 1,3-5,9-12): ")

            if pages_input == '0':
                # Copy the file as is
                import shutil
                edited_filepath = os.path.join(edited_folder, filename)
                shutil.copyfile(original_filepath, edited_filepath)
                print(f"Copied original file to: {edited_filepath}")

                # Rename original file
                processed_filepath = os.path.join(download_folder, f"{os.path.splitext(filename)[0]}_processed.pdf")
                os.rename(original_filepath, processed_filepath)
                print(f"Renamed original file to: {processed_filepath}")
                continue

            if pages_input == '-1':
                # Skip the file and rename it
                skipped_filepath = os.path.join(download_folder, f"{os.path.splitext(filename)[0]}_skipped.pdf")
                os.rename(original_filepath, skipped_filepath)
                print(f"Skipped and renamed file to: {skipped_filepath}")
                continue
            
            # Create new PDF with specified pages
            try:
                reader = PdfReader(original_filepath)
                writer = PdfWriter()
                
                page_ranges = pages_input.split(',')
                pages_to_keep = set()
                for part in page_ranges:
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        for i in range(start, end + 1):
                            pages_to_keep.add(i)
                    else:
                        pages_to_keep.add(int(part))
                
                for i in sorted(list(pages_to_keep)):
                    if 0 < i <= len(reader.pages):
                        writer.add_page(reader.pages[i-1])

                edited_filepath = os.path.join(edited_folder, filename)
                with open(edited_filepath, "wb") as f:
                    writer.write(f)
                print(f"Created edited PDF: {edited_filepath}")

                # Rename original file
                processed_filepath = os.path.join(download_folder, f"{os.path.splitext(filename)[0]}_processed.pdf")
                os.rename(original_filepath, processed_filepath)
                print(f"Renamed original file to: {processed_filepath}")

            except Exception as e:
                print(f"Error processing {original_filepath}: {e}")

def display_menu():
    """Displays the main menu."""
    print("\n--- Menu ---")
    print("1. Download files")
    print("2. Process downloaded files")
    print("3. Exit")

def main():
    """Main function to run the script."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            download_files()
        elif choice == '2':
            process_files()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()