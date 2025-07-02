from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://timesofindia.indiatimes.com/topic/last-2-days/news")
wait = WebDriverWait(driver, 10)

article_links = set()
clicks = 0
MAX_CLICKS = 30  # click "Load More" this many times (approx 450 articles if ~30 per load)

while clicks < MAX_CLICKS:
    try:
        # Scroll near bottom (not all the way)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Scroll slightly up to make the button visible
        driver.execute_script("window.scrollBy(0, -800);")
        time.sleep(1)

        # Locate and scroll into view of the button
        load_more = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Load More Articles")]'))
        )
        # driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
        # time.sleep(1)


        # Scroll to button explicitly and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more)
        time.sleep(1)

        # Click the button
        load_more.click()
        clicks += 1
        print(f"Clicked Load More: {clicks}")
        time.sleep(4)  # wait for articles to load

    except Exception:
        print("'Load More' button not found or not clickable.")
        break




# Now extract article links
time.sleep(3)
articles = driver.find_elements(By.XPATH, '//a[contains(@href, "/articleshow/")]')
for a in articles:
    href = a.get_attribute("href")
    if href:
        article_links.add(href)

# Save to Excel
import pandas as pd
df = pd.DataFrame({"Article URL": list(article_links)})
df.to_excel("toi_article_links.xlsx", index=False)
print(f"✅ Saved {len(article_links)} article links to 'toi_article_links.xlsx'.")
