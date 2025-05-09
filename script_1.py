import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta
import os








excel_file = "Skrapede_data.xlsx"






driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))






def scrape_title(url):
    driver.get(url)
    time.sleep(5)
    try:
        title_tag = driver.find_element(By.XPATH, "//div[@x-text='incident.title']")
        return title_tag.text.strip() if title_tag else ""
    except Exception as e:
        return f"Error: {str(e)}"






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
            return date_text
    except Exception as e:
        return f"Error: {str(e)}"






def scrape_description(url):
    driver.get(url)
    time.sleep(5)
    try:
        description_tag = driver.find_element(By.XPATH, "//div[@x-html='formatText(incident.body)']")
        return description_tag.text.strip() if description_tag else ""
    except Exception as e:
        return f"Error: {str(e)}"






def scrape_area(url):
    driver.get(url)
    time.sleep(5)
    try:
        area_tag = driver.find_element(By.XPATH, "//span[@x-text='area.area']")
        return area_tag.text.strip() if area_tag else ""
    except Exception as e:
        return f"Error: {str(e)}"
    





def scrape_impact(url):
    driver.get(url)
    time.sleep(5)
    try:
        impact_tag = driver.find_element(By.XPATH, "//div[@x-text='incident.incident.impact']")
        return impact_tag.text.strip() if impact_tag else ""
    except Exception as e:
        return f"Error: {str(e)}"






url = "https://www.tusass.gl/da/kundeservice/driftsinformation/"
title = scrape_title(url)
date = scrape_date(url)
description = scrape_description(url)
area = scrape_area(url)
impact = scrape_impact(url)
scraping_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")






if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
    next_order = df["Order"].max() + 1
else:
    df = pd.DataFrame(columns=["Order", "URL", "Title", "Date", "Description", "Area", "Impact", "Scraped At"])
    next_order = 1
new_row = {
    "Order": next_order,
    "URL": url,
    "Title": title,
    "Date": date,
    "Description": description,
    "Area": area,
    "Impact": impact,
    "Scraped At": scraping_time
}






df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)






df.to_excel(excel_file, index=False)
print("Nye data gemt i Excel!")
driver.quit()