from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
import csv
import json

s = Service('chromedriver')
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options=chrome_options)

def get_avg_temp_for_month_year(month, year):
    try:
        dropdown = driver.find_element(By.XPATH, "/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[1]")
        month_select = Select(dropdown)
        month_select.select_by_index(month)
        time.sleep(.5)

        year_dropdown = driver.find_element(By.XPATH, '//*[@id="yearSelection"]')
        year_select = Select(year_dropdown)
        year_select.select_by_visible_text(str(year))
        time.sleep(1)

        submit_button = driver.find_element(By.ID, "dateSubmit")
        submit_button.click()
        time.sleep(7)
        avgtemp = driver.find_element(By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table/tbody[1]/tr[2]/td[2]')
        return avgtemp.text
    except Exception as e:
        print(f"Error for month {month} year {year}: ", e)
        return None

driver.get('https://www.wunderground.com/history/monthly/kr/seoul/RKSS')
time.sleep(8)

time_series_data = []  

for year in range(1997, 2024):  
    for month in range(1, 13):  # for all 12 months
        temp = get_avg_temp_for_month_year(month, year)
        if temp:
            time_series_data.append({"year": year, "month": month, "temp": temp})
            print(f"{year}-{month}: {temp}")

with open("time_series_results.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["year", "month", "temp"])
    writer.writeheader()
    for data_point in time_series_data:
        writer.writerow(data_point)

driver.quit()
