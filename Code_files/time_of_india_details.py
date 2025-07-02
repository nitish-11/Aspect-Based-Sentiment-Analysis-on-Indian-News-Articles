from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

url = "https://timesofindia.indiatimes.com/city/ranchi/state-records-89-8mm-in-last-24-hours-schools-to-remain-closed-for-2nd-day/articleshow/121959600.cms"
driver.get(url)

try:
    # Wait until content body loads
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-articlebody="1"]'))
    )

    # Title
    title = driver.find_element(By.XPATH, "//h1").text.strip()

    # Publication time
    publication_time = driver.find_element(By.XPATH, "//div[contains(@class,'publish_on')]//span").text.strip()

    # Article content
    paragraphs = driver.find_elements(By.XPATH, "//div[@data-articlebody='1']//p")
    content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])

    print("Title:", title)
    print("Published:", publication_time)
    print("Content:", content[:500] + "..." if content else "N/A")
    print("URL:", url)

except Exception as e:
    print("Error:", str(e))

driver.quit()
