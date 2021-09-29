'''
Joke code about how pointless it would be to make something that's just a crappy version of google translate. Anyway, at some point in the past 3 months this code broke.
I don't really care enough about it to fix it so I'm just going to post it here incase I need a reminder of selenium stuff
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from chromedriver_downloader import download_chrome_driver

def find_el(value, by = By.XPATH, max_time = 10):
    try:
        output = WebDriverWait(driver, max_time).until(
            EC.presence_of_element_located((by, value))
        )
        return output
    except:
        return "things didn't work"

def find_els(value, by = By.XPATH, max_time = 10):
    try:
        output = WebDriverWait(driver, max_time).until(
            EC.presence_of_all_elements_located((by, value))
        )
        return output
    except:
        return "things didn't work"



viable_languages = {i.split()[0].lower() : i.split()[1] for i in open("translateable_languages.txt", "r").read().split("\n")}

while True:
    first_language = input("Enter the input language: ").lower()

    if "languages" in first_language:
        print("The viable languages are ", "\n".join(viable_languages.keys()))
        continue
    if first_language not in viable_languages.keys():
        print("That language is not recognized. To view viable languages print \"languages\"")
        continue

    break

while True:
    second_language = input("Enter the second language: ").lower()

    if "languages" in second_language:
        print("The viable languages are ", "\t".join(viable_languages.keys()))
        continue
    if second_language not in viable_languages.keys():
        print("That language is not recognized. To view viable languages print \"languages\"")
        continue

    break


text = input("Enter the text to be translated: ")

options = webdriver.ChromeOptions()
options.add_argument("headless")



try:
    driver = webdriver.Chrome("chromedriver.exe", options = options)
except:
    download_chrome_driver()
    driver = webdriver.Chrome("chromedriver.exe", options=options)

driver.get(f"https://translate.google.ca/?sl={viable_languages[first_language]}&tl={viable_languages[second_language]}&text={text}")
output = find_el("VIiyi", By.CLASS_NAME)
print()
print(output.text)
driver.close()

# print(f"https://translate.google.ca/?sl={first_language}&tl={second_language}&text={text}")


