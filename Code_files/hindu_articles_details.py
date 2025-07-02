import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Load the Excel with links
input_file = "new_papers_scraping/thehindu_article_links.xlsx"
df = pd.read_excel(input_file)

# Output list to store results
articles_data = []

# Initialize browser
driver = webdriver.Chrome()
driver.maximize_window()

for idx, row in df.iterrows():
    url = row["URL"]
    print(f"\n[{idx + 1}/{len(df)}] Fetching: {url}")
    
    try:
        driver.get(url)
        time.sleep(2)

        # Extract Title
        try:
            title = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/div[1]/h1").text
        except NoSuchElementException:
            title = ""

        # Extract Publication Timestamp
        try:
            # publication = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/div[1]/div[1]/p/span").text
            publication = driver.find_element(By.XPATH, '//meta[@itemprop="datePublished"]').get_attribute("content")
        except NoSuchElementException:
            publication = ""

        # Extract Full Content
        try:
            content = driver.find_element(By.XPATH, '//*[@id="schemaDiv"]').text
        except NoSuchElementException:
            content = ""

        # Append data
        articles_data.append({
            "Title": title,
            "Publication": publication,
            "Content": content,
            "URL": url
        })

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        articles_data.append({
            "Title": "",
            "Publication": "",
            "Content": "",
            "URL": url
        })

    # Optional delay to avoid being blocked
    time.sleep(2)

# Close the browser
driver.quit()
print("\n🧹 Browser closed.")

# Save to Excel
output_df = pd.DataFrame(articles_data)
output_file = "thehindu_article_details.xlsx"
output_df.to_excel(output_file, index=False)
print(f"\nArticle data saved to {output_file}")
