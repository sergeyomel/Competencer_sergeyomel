import random
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

class Parser:
    def __init__(self):
        self.start = 0
        self.step = 25

    def get_data(self, url):
        html_elements = []
        for i in range(0, 39):
            try:
                links = []
                try:
                    driver.get(url + str(self.start))
                except Exception as error:
                    print('URL error')
                    print(error)

                elements = driver.find_elements(By.TAG_NAME, 'a')
                if len(elements) == 0:
                    break

                try:
                    for element in elements:
                        href = element.get_attribute('href')
                        if href[0:35] == 'https://www.linkedin.com/jobs/view/':
                            links.append(href)
                except Exception as error:
                    print('Cannot find @href')
                    print(error)

                for link in links:
                    driver.get(link)
                    desc = []
                    try:
                        description = driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div')
                        for d in description:
                            if d != []:
                                desc.append(d.text)
                        html_elements.append(
                            {
                            '1': driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1')[0].text,
                            '2': driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a')[0].text,
                            '3': driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]')[0].text,
                            '4': driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[1]')[0].text,
                            '5': driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]')[0].text,
                            '6': desc
                            }
                        )
                    except Exception as error:
                        print(error)
                self.start += self.step
                time.sleep(random.randint(2, 4))
            except Exception as error:
                print(error)

        return html_elements

def main():
    url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?trk=guest_homepage-basic_guest_nav_menu_jobs&start='
    P = Parser()
    data = P.get_data(url)
    with open("data.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
