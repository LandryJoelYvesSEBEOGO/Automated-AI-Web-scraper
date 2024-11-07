import streamlit as st
from workflow_dict import workflow_dict
import pandas as pd
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama,read_websites_from_file

# List of example websites
# Read websites from the text file
file_path = r"website.txt"
example_websites = read_websites_from_file(file_path)

# Initialize session state for URL if not set
if 'url_input' not in st.session_state:
    st.session_state['url_input'] = ""

# Streamlit UI
st.title("AI Web Scraper 🐙")

# Create a two-column layout: one for the input bar, one for the dropdown widget
col1, col2 = st.columns([8, 3])  # Adjust the ratio as needed for proper alignment

with col2:
    # Dropdown widget (acts as the arrow-like button)
    selected_website = st.selectbox(
        "Select website",
        options=["Select a website"] + example_websites,
    )

# If a website is selected from the dropdown, update the URL input field directly
if selected_website != "Select a website":
    # Update the session state for the URL input field
    st.session_state['url_input'] = selected_website
    

# Now create the text input field after ensuring the session state is set
with col1:
    # Text input for the URL (Principal Input Bar)
    url = st.text_input("Enter Website URL", value=st.session_state['url_input'], key='url_input')
        
        
# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write(f"Scraping the website {url}...")

        try:
            # Scrape the website
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            parse_description = "Put all car details, price per day and location in the same table."
            st.write("Parsing the content...")

            try:
                # Parse the content with Gemini
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                st.write(parsed_result)

                # Store the parsed result in Streamlit session state
                st.session_state.parsed_result = parsed_result
                #st.write(st.session_state.parsed_result)
            except Exception as e:
                st.error(f"An error occurred while parsing the content: {e}")
                
        except Exception as e:
            st.error(f"An error occurred while scraping the website: {e}")
     
            
if st.button("Rescrape"):
    parse_description = "Put all the car details and price per day in the same table."
    st.write("Parsing the content...")
    try:
                # Parse the content with Gemini
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                
                # Store the parsed result in Streamlit session state
                st.session_state.parsed_result = parsed_result
                st.write(st.session_state.parsed_result)
    except Exception as e:
                st.error(f"An error occurred while parsing the content: {e}")
    

# Step 3: Download Parsed Result as CSV
if "parsed_result" in st.session_state:
        try:
            # Convert the parsed result to a DataFrame
            parsed_data = {"Parsed Result": st.session_state.parsed_result.split('\n')}
            df = pd.DataFrame(parsed_data)

            # Convert the DataFrame to CSV
            csv = df.to_csv(index=False)

            # Make the CSV file downloadable
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="parsed_result.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"An error occurred while preparing the CSV: {e}")
