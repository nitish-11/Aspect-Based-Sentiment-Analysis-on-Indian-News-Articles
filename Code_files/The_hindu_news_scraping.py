import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Initialize Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

page = 1
all_links = []

try:
    while True:
        url = f"https://www.thehindu.com/latest-news/?page={page}"
        print(f"\nScraping Page {page}: {url}")

        try:
            driver.get(url)
        except Exception as e:
            print(f"Failed to load {url}: {e}")
            break

        time.sleep(2)

        # Extract article links
        for i in range(1, 15):
            try:
                xpath = f"/html/body/section[2]/div/div[2]/div[2]/ul/li[{i}]/div/div/h3/a"
                article = driver.find_element(By.XPATH, xpath)
                article_link = article.get_attribute("href")
                print(f"{i}. {article_link}")
                all_links.append({"Page": page, "Index": i, "URL": article_link})
            except NoSuchElementException:
                break

        # Check if next button exists
        try:
            next_button_xpath = "/html/body/section[2]/div/div[2]/div[2]/nav/ul/li[11]"
            next_button = driver.find_element(By.XPATH, next_button_xpath)
            if 'disabled' in next_button.get_attribute("class"):
                print("No more pages.")
                break
        except NoSuchElementException:
            print("Next button not found. Stopping.")
            break

        page += 1
        time.sleep(2)

except Exception as main_error:
    print(f"\n‼Unexpected error: {main_error}")

finally:
    # Always close browser
    driver.quit()
    print("\n🧹 Browser closed.")

    # Save to Excel
    if all_links:
        df = pd.DataFrame(all_links)
        excel_path = "thehindu_article_links.xlsx"
        df.to_excel(excel_path, index=False)
        print(f"Saved {len(all_links)} articles to {excel_path}")
