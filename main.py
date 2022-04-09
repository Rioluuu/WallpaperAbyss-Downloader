import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def scrapeSiteLinks(link, page_amount):
    driver = webdriver.ChromiumEdge('msedgedriver.exe')
    driver.get(link)
    driver.add_cookie({'name' : 'cookieconsent_status', 'value' : 'allow'})
    driver.get(link)
    driver.find_element(By.CLASS_NAME, 'auto-load-button-next').click()
    print(f'Page 1 done!')
    temp_links = []
    for i in range(1, page_amount):
        driver.find_element(By.ID, 'span_next_page').click()
        time.sleep(2)
        print(f'Page {i+1} done!')
        if i % 5 == 0 or i == page_amount - 1:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            image_containers = soup.find_all('div', class_='thumb-container-big')
            for container in image_containers:
                image_site_link = container.get('id').replace('thumb_', 'https://wall.alphacoders.com/big.php?i=')
                temp_links.append(image_site_link)
    links = []
    [links.append(element) for element in temp_links if element not in links]
    return links


def getFileLinks(links):
    file_links = []
    for link in links:
        image_site_content = requests.get(link).text
        soup = BeautifulSoup(image_site_content, 'lxml')
        file_link = soup.find('img', class_='main-content').get('src').replace('thumb-1920-', '')
        file_links.append(file_link)
        print(f"Wallpaper found: {file_link}")
        time.sleep(1)
    return file_links


site_links = scrapeSiteLinks(input('Enter a Link > '), int(input('Enter the amount of pages to scrape > ')))
image_links = getFileLinks(site_links)

for image_link in image_links:
    r = requests.get(image_link)
    file_name = image_link.rsplit('/', 1)[1]
    open(f'images/{file_name}', 'wb').write(r.content)
    print(f'File {file_name} saved!')
    time.sleep(1)
