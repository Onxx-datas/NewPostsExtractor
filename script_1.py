import gspread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime, timedelta

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('access-to-sheets-449017-376cfa18b986.json', scope)
client = gspread.authorize(creds)

sheet_url = "https://docs.google.com/spreadsheets/d/1QCL-vqfLsLafS2VYg8cPjj31PiQk-IwuQHistOaTXDk/edit"
sheet = client.open_by_url(sheet_url)
worksheet = sheet.worksheet("testing")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrape_title(url):
    driver.get(url)
    time.sleep(5) 

    try:
        title_tag = driver.find_element(By.XPATH, "//div[@x-text='incident.title']")
        title = title_tag.text.strip() if title_tag else ""
    except Exception as e:
        title = f"Error: {str(e)}"
    return title

def scrape_date(url):
    driver.get(url)
    time.sleep(5)

    try:
        date_tag = driver.find_element(By.XPATH, "//div[@x-text='incident.date']")
        date_text = date_tag.text.strip() if date_tag else ""

        if "dege siden" in date_text:
            days_ago, exact_date = date_text.split(" - ")
            days_ago = int(days_ago.split()[0])
            parsed_date = datetime.strptime(exact_date, "%d.%m.%Y %H:%M")
            calculated_date = parsed_date - timedelta(days=days_ago)
            return calculated_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return f"{date_text}"
    except Exception as e:
        return f"Error: {str(e)}"
    
def scrape_description(url):
    driver.get(url)
    time.sleep(5)

    try:
        description_tag = driver.find_element(By.XPATH, "//div[@x-html='formatText(incident.body)']")
        description = description_tag.text.strip() if description_tag else ""
    except Exception as e:
        description = f"Error: {str(e)}"
    return description
def scrape_area(url):
    driver.get(url)
    time.sleep(5)

    try:
        area_tag = driver.find_element(By.XPATH, "//span[@x-text='area.area']")
        area = area_tag.text.strip() if area_tag else ""
    except Exception as e:
        area = f"Error: {str(e)}"
    return area

def scrape_impact(url):
    driver.get(url)
    time.sleep(5)

    try:
        impact_tag = driver.find_element(By.XPATH, "//div[@x-text='incident.incident.impact']")
        impact = impact_tag.text.strip() if impact_tag else ""
    except Exception as e:
        impact = f"Error: {str(e)}"
    return impact

def get_next_order_number():
    rows = worksheet.get_all_values()
    if len(rows) > 1:
        last_order_number = int(rows[-1][0])
        return last_order_number + 1
    return 1

url = "https://www.tusass.gl/da/kundeservice/driftsinformation/"
title = scrape_title(url)
date = scrape_date(url)
description = scrape_description(url)
area = scrape_area(url)
impact = scrape_impact(url)

scraping_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

web_scraper_order = get_next_order_number()

new_data = [
    web_scraper_order, 
    url,
    title,
    date,
    description,
    area,
    impact,
    scraping_time
]

next_row = len(worksheet.get_all_values()) + 1
worksheet.insert_row(new_data, next_row)

print("New data added!")
driver.quit()