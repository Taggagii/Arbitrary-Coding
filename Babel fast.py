from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

shelf = 2
volume = 1
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://libraryofbabel.info/book.cgi?0-w1-s1-v01:0")
open('urls.txt', 'w')
while True:
    try:
        text = driver.find_element_by_id('textblock').text
        if 'jack' in text:
            open("urls.txt", 'a').write(driver.current_url + '\n')
        driver.find_element_by_xpath('''/html/body/div/div[3]/span[2]/a[1]''').click()
    except Exception as e:
        if ' '.join(str(e).split()[1:4])[:-1] == 'no such element':
            volume = int(volume)
            if volume < 10: volume = '0' + str(volume + 1)
            else:
                volume += 1
                if volume > 32:
                    shelf += 1
                    if shelf >= 6: break
            driver.get(f"https://libraryofbabel.info/book.cgi?0-w1-s{shelf}-v{volume}:0")
            print(int(volume) - 1)
            pass
driver.close()
values.close()
