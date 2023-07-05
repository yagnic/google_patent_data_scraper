import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time

# Set up Streamlit app layout
st.title("Patent Data Scraper")
substance = st.text_input("Enter the substance:", "(substance)")
num_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, step=1, value=1)
start_button = st.button("Start Scraping")

if start_button:
    # Enable headless mode for Chrome
    options = Options()
    options.add_argument('--headless')

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=options)

    # Scraping logic
    url = f"https://patents.google.com/?q={substance}&oq={substance}"
    driver.get(url)
    patents = []


    with st.spinner("Scraping in progress..."):
        for i in tqdm(range(0, 0 + num_pages)):

            time.sleep(2)
            elements = driver.find_elements_by_xpath('//span[@data-proto="OPEN_PATENT_PDF"]')
            for element in elements:
                patent_id = element.text
                if "JP" in patent_id:
                    continue
                patents.append(patent_id)
            driver.get(f"https://patents.google.com/?q={substance}&page={i}")

    st.write(f"There are in total {len(patents)} patents being scraped")
    exceptions_new = []
    titles = []
    abstracts = []
    with st.spinner("Extracting data..."):
        for patent in tqdm(patents):

            try:
                driver.get(f"https://patents.google.com/patent/{patent}/en?q={substance}")
                time.sleep(2)
                title_element = driver.find_element_by_xpath('//h1[@id="title"]')
                abstract_element = driver.find_element_by_xpath('//div[@class="abstract style-scope patent-text"]')

                title = title_element.text
                abstract = abstract_element.text

#                 # Display the extracted data in a blog-like format inside a scrollable expander
#                 with st.expander(f"Patent: {patent}"):
#                     st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
#                     st.write(f"Abstract: {abstract}")
#                     st.markdown("---")

                titles.append(title)
                abstracts.append(abstract)
            except Exception as e:
                exceptions_new.append(e)

    # Create a DataFrame with the extracted data
    train_data = pd.DataFrame({"title": titles, "abstract": abstracts})

    # Save the DataFrame as a CSV file
    train_data.to_csv("./scraped_test_data.csv",index=False)
    st.write(train_data)
    # Close the Chrome driver
    driver.quit()
    st.success("Scraping complete!")
