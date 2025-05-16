'''this part is used for creating a baseline hash of the html contents of your payment page.
"payment_page_analyzer" will then check the current contents against it'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import hashlib

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://yourpaymentpage.com"

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract all inline or external script URLs
scripts = [tag.get('src', '') + tag.get_text() for tag in soup.find_all('script')]

# Extract the form and action URL (e.g., the checkout/payment form)
forms = [tag.get('action', '') for tag in soup.find_all('form')]

# Combine and hash
critical_content = "".join(scripts + forms)
page_hash = hashlib.sha256(critical_content.encode("utf-8")).hexdigest()
print("Page SHA-256:", page_hash)

with open("baseline_hash.txt", "w") as f:
    f.write(page_hash)

#creating a debug file of baseline content
with open("baseline_debug.txt", "w") as f:
    f.write(critical_content)

driver.quit()