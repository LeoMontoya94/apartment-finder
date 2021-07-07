from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import requests
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = r'C:\Users\leoof\chromedriver_win32\chromedriver.exe'
FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLScu5KwPS6siSW0YusUcoKTkUdVJcth3wgD_hO1UmmF-1lFR0A/viewform?usp=sf_link'
FORM_CONTROL = 'https://docs.google.com/forms/d/1q_f39dw0Kpd0f6RGzaUjbWrWDiGiUHNU79R1g-b44g0/edit#responses'
ZILLOW_URL = 'https://www.zillow.com/provo-ut/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Provo%2C%20UT%22%2C%22mapBounds%22%3A%7B%22west%22%3A-112.41623288964846%2C%22east%22%3A-110.8094824013672%2C%22south%22%3A40.017649995283115%2C%22north%22%3A40.82994327643148%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20071%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D'
REQ_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
EMAIL = 'pythontest12320@gmail.com'
PASSWORD = 'Boombox1'


class ZillowDataScraper:

    def __init__(self):
        self.response = requests.get(ZILLOW_URL, headers=REQ_HEADERS)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.links_list_final = []
        self.price_list = []
        self.address_list = []
        self.iterative = 0
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    def get_info_lists(self):
        links_div_list = self.soup.find_all('div', class_='list-card-info')
        links_element_list = [div.find_all('a', class_='list-card-link')[0] for div in links_div_list]
        links_list = [link['href'] for link in links_element_list]
        for link in links_list:
            if 'zillow' not in link:
                link = 'https://www.zillow.com' + link
            self.links_list_final.append(link)

        price_element_list = self.soup.find_all('div', class_='list-card-price')
        self.price_list = [price.getText()[:6] for price in price_element_list]

        address_element_list = self.soup.find_all('address', class_='list-card-addr')
        self.address_list = [address.getText() for address in address_element_list]

        self.iterative = len(self.links_list_final)

    def fill_out_form(self):
        for n in range(self.iterative):
            self.driver.get(FORM_URL)
            self.driver.maximize_window()
            sleep(1)
            address_entry = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address_entry.send_keys(self.address_list[n])
            price_entry = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_entry.send_keys(self.price_list[n])
            link_entry = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_entry.send_keys(self.links_list_final[n])
            submit_button = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
            submit_button.click()
            sleep(1)


bot = ZillowDataScraper()
bot.get_info_lists()
bot.fill_out_form()

