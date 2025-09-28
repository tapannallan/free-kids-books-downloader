# Free PDF Book Downloader

This project is a Python script that downloads free PDF books from [freekidsbooks.org](https://freekidsbooks.org).

## Description

The script scrapes book URLs from the "Stories for Age 2-5 Years" category on `freekidsbooks.org` and downloads the PDF files to a local directory.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/free-pdf-book-downloader.git
    cd free-pdf-book-downloader
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the script:**
    ```bash
    python downloader.py
    ```

The downloaded books will be saved in the `~/Documents/Kids Books` directory.

## Dependencies

The script requires the following Python libraries:

*   [requests](https://pypi.org/project/requests/)
*   [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

These can be installed using the `requirements.txt` file as described above.
