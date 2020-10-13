import requests
from bs4 import BeautifulSoup
checks = ['(', ')', '[', ']', ':', ',', '-']
intro = 'Welcome to Python Dictionary\n----------Have Fun----------\n\n(To quit enter "quit" and include a "-")\n\n'
clear = ''.join(['\n']*39)
print(clear, intro, end = '')
while True:
    words = ''
    word = ''
    try:
        word = str(input('Enter a word: ')).lower().strip()
        if '-' in word:
            word = word.replace('-', '').strip()
            if 'quit' in word:                    
                print('\nThanks!\nGoodbye\n')
                break
        URL = f"https://www.merriam-webster.com/dictionary/{word}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        words = str(soup.find(class_ = 'dtText').text)
        definition = ''
        counter = 0 
        for i in words:
            if not i.isalpha() and i not in checks: counter += 1
            else: counter = 0
            if counter > 1: break
            definition += i
        print(clear, intro, word.capitalize() + definition, '\n')
    except Exception as e:
        print(clear, intro, 'Word is not found:',  word, '\n')
        pass
