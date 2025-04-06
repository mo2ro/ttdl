import json
import sys
import urllib.request
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('config.json', 'r') as file:
    config = json.load(file)

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.binary_location = config['chrome_path']
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


if __name__ == "__main__":
    driver = webdriver.Chrome(options=set_chrome_options())
    args = sys.argv[1:]
    if len(args) < 1:
        print("Error: Invalid arguments");
        exit(1);

    if not "tiktok.com/" in args[0] and not "video" in args[0]:
        print("Error: Invalid arguments");
        exit(1);
    video = {}
    video['id'] = args[0].split('/video/')[1].split('?')[0]
    video['username'] = args[0].split('/video/')[0].split('tiktok.com/')[1]
    print("Posted by: "+video['username'])
    print("Video id: "+video['id'])
    print("Fetching video...")
    driver.get(f'https://www.tiktok.com/player/v1/{video["id"]}?utm_source=discord.gg')
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
    src = element.get_attribute("src")
    video['type'] = src.split('mime_type')[1].split('&')[0].split('_')[1]
    print("Response type:", video['type'])
    video_path = f"{video['id']}.{video['type']}"
    print("Saving video...")
    if not os.path.exists(config['save_path']):
        os.makedirs(config['save_path'])
    urllib.request.urlretrieve(src, config['save_path'] + video_path)
    print("Video saved to", video_path)
    driver.quit()
    
