# SEO Content Analyzer

A Streamlit-based web application that analyzes search results and provides content insights including word count analysis.

## Features

- Search for any query and analyze top 10 Google search results
- Extract and analyze main content from web pages (excluding navigation, sidebars, etc.)
- Calculate average word count across all analyzed pages
- View detailed statistics for each page including:
  - Page title
  - URL
  - Word count
- Export results to CSV
- Progress tracking during analysis
- Error handling and timeout protection

## Installation

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Enter your search query in the text input field
3. Click "Analyze" to start the analysis
4. View the results:
   - Average word count across all pages
   - Detailed table with information for each page
5. Download results as CSV if needed

## Requirements

- Python 3.7+
- See requirements.txt for package dependencies

## Notes

- The analysis focuses on the main content of web pages, excluding navigation menus, sidebars, and other non-content elements
- Processing time may vary depending on the number of pages and their size
- Some websites may block automated access, which could affect the results
