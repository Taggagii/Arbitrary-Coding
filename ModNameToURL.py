from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import time
import json
from multiprocessing import Pool
import math

minecraft_version = "1.18.2"

mod_names = []

with open("mods.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        mod_names.append(row[0])

def getLinks(mod_names):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless=new")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    links = []

    try:
        for mod_name in mod_names:
            mod_name_transformed = mod_name.replace(" ", "+")
            driver.get(f"https://www.curseforge.com/minecraft/search?page=1&pageSize=20&sortType=1&search={mod_name_transformed}&gameVersion=1.18.2")
            results = driver.find_element(By.CLASS_NAME, "results-container")
            mod_options = results.find_elements(By.TAG_NAME, "a")
            link = mod_options[0].get_attribute("href")
            print(mod_name, link, sep="|")
            links.append({
                "name": mod_name,
                "link": link
            })
    except:
        print("Failure!")
        pass

    driver.close()

    return links


if __name__ == "__main__":
    group_count = 8
    group_size = math.ceil(len(mod_names) / group_count)

    print(f"Group count: {group_count} | Group Size: {group_size}")

    list_of_groups = []
    for i in range(0, len(mod_names), group_size):
        list_of_groups.append(mod_names[i:i + group_size])

    with Pool(group_count) as p:
        links = p.map(getLinks, list_of_groups)
        print("Finished Finding Links, exporting to JSON")
        with open("mods.json", "w") as f:
            json.dump(links, f)

        print("Finished")
