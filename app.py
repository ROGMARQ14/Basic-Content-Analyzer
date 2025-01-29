import streamlit as st
import requests
import pandas as pd
from googlesearch import search
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Remove extra whitespace and newlines from text"""
    return ' '.join(text.split())

def get_main_content(soup):
    """Extract main content from webpage, excluding navigation, header, footer, etc."""
    # Remove unwanted elements
    for unwanted in soup.find_all(['nav', 'header', 'footer', 'sidebar', 'aside']):
        unwanted.decompose()
    
    # Try to find main content container
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|post'))
    
    if main_content:
        return clean_text(main_content.get_text())
    else:
        # Fallback to body content if no main content container found
        body = soup.find('body')
        return clean_text(body.get_text()) if body else ""

def count_words(text):
    """Count words in text"""
    return len(text.split())

def parse_page_info(link):
    """
    Parse webpage to extract title, sections, and word count
    """
    try:
        page = requests.get(link, timeout=10)
        soup = BeautifulSoup(page.text, "lxml")
        
        title = soup.find("title")
        title = title.text if title else "No title found"
        
        # Get main content and word count
        main_content = get_main_content(soup)
        word_count = count_words(main_content)
        
        headers = ['h1', 'h2', 'h3', 'h4', 'h5']
        sections = []
        
        for header in headers:
            header_elements = soup.find_all(header)
            for order, section in enumerate(header_elements):
                sections.append({
                    "url": link,
                    "page_title": title,
                    "header": header,
                    "order": order,
                    "title": section.text
                })
        
        return {
            "url": link,
            "title": title,
            "word_count": word_count,
            "sections": sections
        }
    except Exception as e:
        st.error(f"Error processing {link}: {str(e)}")
        return None

def main():
    st.title("SEO Content Analyzer")
    
    query = st.text_input("Enter your search query:", "python for seo")
    
    if st.button("Analyze"):
        with st.spinner("Searching and analyzing content..."):
            try:
                # Get search results
                results_generator = search(query, num_results=10, lang="en")
                results = list(results_generator)
                
                # Analyze each page
                page_data = []
                total_words = 0
                
                progress_bar = st.progress(0)
                for i, link in enumerate(results):
                    data = parse_page_info(link)
                    if data:
                        page_data.append(data)
                        total_words += data["word_count"]
                    progress_bar.progress((i + 1) / len(results))
                
                # Calculate average word count
                avg_word_count = total_words / len(page_data) if page_data else 0
                
                # Display results
                st.subheader("Analysis Results")
                st.write(f"Average word count across {len(page_data)} pages: {int(avg_word_count)} words")
                
                # Create DataFrame for detailed view
                detailed_data = []
                for data in page_data:
                    detailed_data.append({
                        "URL": data["url"],
                        "Title": data["title"],
                        "Word Count": data["word_count"]
                    })
                
                df = pd.DataFrame(detailed_data)
                st.dataframe(df)
                
                # Option to download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download results as CSV",
                    data=csv,
                    file_name=f"seo_analysis_{query}.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
