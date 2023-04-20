import datetime
import pytz
import time
from bs4 import BeautifulSoup
from difflib import ndiff
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import requests

url = "YOUR_WEBSITE_URL"
url_discord = "WEBHOOK_URL"
tz = pytz.timezone('Europe/Paris')

# Configure Selenium
options = webdriver.ChromeOptions()
options.add_argument('headless')  # Run Chrome in headless mode
chrome_path = '/usr/lib/chromium-browser/chromedriver'  # Path to the Chrome driver executable
driver = webdriver.Chrome(chrome_path, options=options)
last_content = []
nb_request = 0


# Create a function to check for changes in the page
def check_for_changes():
    global actual_time, last_content, nb_request
    # Load the page and get its source code
    try:
        driver.set_page_load_timeout(60) # set a timeout of 60 seconds
        driver.get(url)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_div_elements = soup.select('YOUR_DIV_SELECTOR')
    new_content = [element.text.strip() for element in all_div_elements]
    nb_request += 1
    with open('last_request_time.txt', 'w', encoding='utf-8') as f:
        f.write(str(datetime.datetime.now(tz)))
    with open('nb_request.txt', 'w', encoding='utf-8') as f:
        f.write(str(nb_request))
    # Check if the data has changed
    if new_content != last_content:
        old_str = '\n'.join(map(str, last_content))
        new_str = '\n'.join(map(str, new_content))
        # Trouver les différences entre les deux chaînes de caractères
        diff = ndiff(old_str.split(), new_str.split())
        # Ouvrir le fichier pour enregistrer les changements
        changes = []
        for line in diff:
            # Enregistrer les nouveaux mots dans le fichier
            if line.startswith('+'):
                changes.append(line[2:])
            # Enregistrer les anciens mots remplacés par les nouveaux dans un autre fichier
            elif line.startswith('-'):
                changes.append(line[2:])
        if len(changes) > 0:
            # Remplacer tous les 'à' par une flèche, sauf pour le premier
            changes_str = ' -> '.join([changes[0]] + [x.replace('à', ' -> ') for x in changes[1:]])
            payload = {
                "content": "YOUR_DISCORD_USER_ID",
                "embeds": [
                    {
                        "title": "❗ Changement de la page détecté !!! ❗",
                        "description": f"⚠️ Un changement a été détecté sur la page de la billetterie ⚠️\n\n 👉 Les caractères modifiés sont les suivants : ```{changes_str}``` 👈 \n\n🕐 Changement détecté le {datetime.datetime.now()} ",
                        "color": 5814783
                    }
                ],
            }
            requests.post(url_discord, json=payload)
        last_content = new_content


# Check for changes every 10 seconds
while True:
    check_for_changes()
    time.sleep(10)