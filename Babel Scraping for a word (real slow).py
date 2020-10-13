import requests, time
from bs4 import BeautifulSoup
def volumefix(number):
    if int(number) < 10:
        return f'0{number}'
hex, wall, shelf, volume, pageNo = 0, 1, 1, '1', 1
counter = 0
#PUT THE WORD THAT YOU WANT TO BE SEARCHING FOR WITH THIS IN THE LINE THAT FOLLOWS THIS LONG COMMENT
word_to_check = 'gibuz'
open(f"{word_to_check} Locations", 'w')
while True:
    URL = f'https://libraryofbabel.info/book.cgi?{hex}-w{wall}-s{shelf}-v{volumefix(volume)}:{pageNo}'
    page = requests.get(URL)
   # print(URL)
    if str(page) == '<Response [200]>':
        soup = BeautifulSoup(page.content, 'html.parser')
        title = str(soup.find('title')).lower()
        words = str(soup.find(id='textblock')).lower()
        if word_to_check in title:
            amount = title.count(word_to_check)
            locations = open(f"{word_to_check} Locations", "a+")
            locations.write(URL + '\t' + str(amount) + '\t' + '\ttitle\n')
            counter += 1
            print(counter)
            locations.close()
        if word_to_check in words:
            amount = words.count(word_to_check)
            locations = open(f"{word_to_check} Locations", "a+")
            locations.write(URL + '\t' + str(amount) + '\t' + '\ttextblock\n')
            counter += 1
            print(counter)
            locations.close()
    if wall == 4:
        wall = 0
        hex += 1
    if shelf == 5:
        shelf = 0
        wall += 1
    if  volume == '32':
        volume = '0'
        shelf += 1
    if pageNo == 410:
        pageNo = 0
        volume = str(int(volume) + 1)
    pageNo += 1
