# IMDb Top 250 Movies Scraper

This project is a Scrapy-based spider that scrapes the IMDb Top 250 movies and their cast information. The scraped data is stored in Google Sheets.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later installed on your system.
- `pip` (Python package installer) installed.
- Google Cloud project with API access to Google Sheets enabled.
- Service account credentials file (`service_account.json`) from Google Cloud.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MykytaKuzmytskyi/movies_parse.git
   cd movies_parse

2. **Install modules and dependencies:**

   ```bash
   python -m venv venv
   venv\Scripts\activate (on Windows)
   source venv/bin/activate (on macOS)
   pip install -r requirements.txt
   ```
3. `.env_sample`
   This is a sample .env file for use in local development.
   Duplicate this file as .env in the root of the project
   and update the environment variables to match your
   desired config.

4. **Creating and Using Google Sheets**

 *Create a Google Sheet:*

   - Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet.
   - Name the spreadsheet as desired.

*Obtain the Spreadsheet ID:*

   - Open the created spreadsheet.
   - The Spreadsheet ID is the part of the URL between `/d/` and `/edit`. For example, in the URL `https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0jklmnopqrstu/edit`, the Spreadsheet ID is `1a2b3c4d5e6f7g8h9i0jklmnopqrstu`.

*Share the Spreadsheet:*

   - Click the "Share" button in the upper right corner of the Google Sheet.
   - Share it with the email address associated with your Google Cloud service account (you can find this email in your `service_account.json` file).

*Update Environment Variables:*

   - Replace `<YOURS_SPREADSHEET_ID>` in your `.env` file with the actual Spreadsheet ID you obtained.
   - Define the following range names in your `.env` file:
     - `ACTORS_RANGE_NAME='Actors!A1'`: The range where actor data will be stored.
     - `MOVIES_RANGE_NAME='Movies!A1'`: The range where movie data will be stored.

5. **Run the Scrapy spider**
   ```bash
   scrapy crawl top_250_movies
   ```

The spider will scrape the IMDb Top 250 movies page.
It will extract details for each movie, including the title, rating, and cast information.
The extracted data will be sent to Google Sheets.