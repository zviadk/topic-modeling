#Scraping of daily news from agenda.ge in text format and storing them in csv file news_data

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import csv
import os


def scraping_agenda (year, month, day):

    url = 'https://agenda.ge'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    pause_loading = 5
    keyword = 'news/news'
    link_to_follow = None

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and keyword in href:
            link_to_follow = href
            break
     
    if link_to_follow:
        link_to_follow = urljoin(url, link_to_follow)
        driver = webdriver.Edge(service = Service(EdgeChromiumDriverManager().install()))


        try:
            driver.get(link_to_follow)
            time.sleep(pause_loading)

            year_dropdown_trigger = driver.find_element(By.ID, "select-year")
            year_dropdown_trigger.click()
            time.sleep(pause_loading)
            year_option = driver.find_element(By.XPATH, f"//a[text()= '{year}']")
            year_option.click()
            time.sleep(pause_loading) 
                       
            month_dropdown_trigger = driver.find_element(By.ID, "select-month")
            month_dropdown_trigger.click()
            time.sleep(pause_loading) 
            month_option = driver.find_element(By.XPATH, f"//a[text()= '{month}']")
            month_option.click()
            time.sleep(pause_loading)

            day_dropdown_trigger = driver.find_element(By.ID, "select-day")
            day_dropdown_trigger.click()
            time.sleep(pause_loading)
            day_option = driver.find_element(By.XPATH, f"//a[text()= '{day}']")
            day_option.click()
            time.sleep(pause_loading)  

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            news_items = soup.find_all('div', class_='card')

            news_data = []
            existing_urls = set()

            if os.path.exists('news_data.csv'):
                with open('news_data.csv', 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    for row in reader:
                        existing_urls.add(row[1])  # Assuming URL is the second column




            
            for item in news_items:
                try:
                    title = item.find('a').text.strip()
                    read_more_link = urljoin(url, item.find('a')['href'])

                    if read_more_link not in existing_urls:
                        news_page = requests.get(read_more_link)
                        news_soup = BeautifulSoup(news_page.text, 'html.parser')

                        # Extract only the textual content, excluding links and ads
                        full_text = ' '.join([p.text.strip() for p in news_soup.find_all('p')])
                        
                        news_data.append([title, full_text])
                        existing_urls.add(read_more_link)
                except Exception as e:
                    print(f"An error occurred while processing an item: {e}")
                
            if news_data:
                with open('news_data_2024_January.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if os.stat('news_data.csv').st_size == 0:
                        writer.writerow(['Title', 'Full Text'])
                    writer.writerows(news_data)

                print("Data has been written to news_data.csv")



        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
        # Close the driver
            driver.quit()
    
    else:
        print('Link not found')
        print ('extracted daily news for: {year}, {month}, {day}')   

for day_of_month in range(1,31):
    scraping_agenda(2024,'January',day_of_month)
