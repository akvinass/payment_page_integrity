from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import hashlib
import difflib

#setting headless browser
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

#page URL
url = "https://yourpaymentpage.com"

#loading the page
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract all inline or external script URLs
scripts = [tag.get('src', '') + tag.get_text() for tag in soup.find_all('script')]

# Extract the form and action URL (e.g., the checkout/payment form)
forms = [tag.get('action', '') for tag in soup.find_all('form')]

#computing hash
critical_content = "".join(scripts + forms)
page_hash = hashlib.sha256(critical_content.encode("utf-8")).hexdigest()
print("Page SHA-256:", page_hash)

#loading baseline hash from file
with open("baseline_hash.txt", "r") as f:
    baseline_hash = f.read().strip()

#comparing hashes
if page_hash != baseline_hash:
    with open("debug_current.txt", "w") as f:
        f.write(critical_content)
    print("⚠️ Page has changed!")
    with open("baseline_debug.txt", "r") as f1, open("debug_current.txt", "r") as f2:
        baseline = f1.readlines()
        current = f2.readlines()

    diff = difflib.unified_diff(
        baseline,
        current,
        fromfile='baseline_debug.txt',
        tofile='debug_current.txt',
        lineterm=''
    )

    '''for line in diff:
        print(line)'''

    with open("page_diff.txt", "w") as diff_out:
        diff_out.writelines(diff)

    from email_alerts import send_email
    send_email(
        subject="⚠️ Payment Page Changed!",
        body=f"Hash mismatch detected on {url}. Possible unauthorized modification."
    )
else:
    print("✅ Page content unchanged.")

driver.quit()