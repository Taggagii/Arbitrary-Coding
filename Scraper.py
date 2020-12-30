#this is a webscraper which takes in words from "TestingWords.txt" and formats them into an output txt
#it utilizes multithreading to perform the downloads asynchronously which is much faster than doing it one at a time



import requests, time, concurrent.futures, re, io, multiprocessing
from bs4 import BeautifulSoup

MAX_THREADS = multiprocessing.cpu_count()

outputTxtName = "output.txt"
open(outputTxtName, "w+") #Clearing and creating output


def pushInfoToOutput(word, wordClass, entrys, didYouKnow):
    output = ""
    while True:
        if wordClass is None:
            output += (word + " ---- " + "Does not exist\n\n\n")
            break
        output += (word + " ---- " + wordClass + "\n")
        for entry in entrys:
            for defintions in entry:
                for defintion in defintions:
                    output += (defintion + "\n")
            output += "\n"
            
        if didYouKnow is None:
            break
        output += (didYouKnow)
        break
    
    with io.open(outputTxtName, "a+", encoding = "utf-8") as file:
        file.write(output.strip() + "\n\n\n")
    
         


#Specifications Are Found Here
def downloadWord(word):
    #Scraping Page
    url = "https://www.merriam-webster.com/dictionary/" + word
    page = requests.get(url)

    #Finding Specifics
    soup = BeautifulSoup(page.content, "html.parser")

    #getting the word class (eg. adj, noun, verb, etc.)
    wordClass = ""
    try:
        wordClass = soup.find(class_="important-blue-link").text
    except Exception as e:
        pushInfoToOutput(word, None, None, None)
        return;
        

    #getting the definitions
    currentEntry = 1
    baseId = "dictionary-entry-"
    entrys = []
    while True:             
        entry = soup.find(id = baseId + str(currentEntry))
        if entry is None: break
    
        definitions = []
        definitionIndex = entry.find_all(class_="sb-0")
        for defintion in definitionIndex:
            definitions.append([re.sub(" +", " ", defintion.text.replace("\n", "^")).replace("^ ^", "\n")])

        sbValue = 1
        while True:
            definitionIndex = entry.find_all(class_="sb-" + str(sbValue))
            if definitionIndex == []: break
            sbValue += 1
            counter = 0
            for definition in definitionIndex:
                definitions[counter].append(re.sub(" +", " ", definition.text).replace("\n \n", "\n"))
                counter += 1
            
                
        entrys.append(definitions)
        currentEntry += 1

    #getting the "Did You Know?"
    didYouKnow = ""
    try:
        didYouKnow = soup.find(id="note-1-anchor").find_all("p")[-1].text
    except:
        pass
           
    pushInfoToOutput(word, wordClass, entrys, didYouKnow)
    time.sleep(0.25)


def downloadWords(words):
    threads = min(MAX_THREADS, len(words)) #so we don't use more threads than there are words
    with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
        executor.map(downloadWord, words)
        


words = open("TestingWords.txt", "r").read().split("\n")
s = time.time()
downloadWords(words)
e = time.time()

print(f"It took {e - s} seconds to download {len(words)} words utilizing {min(MAX_THREADS, len(words))} workers")

