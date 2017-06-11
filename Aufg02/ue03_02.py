###################################################################
# FUNCTIONS

def removeDots(wordlist):
    """Receives a list of words. Removes dots, colons, parentheses, URLs and email addresses
        from that list and returns it."""

    #endlist = wordlist.copy()
    i = 0
    email = re.compile('.+@.+\..+')     #pattern of an email address
    dotsAndColons = re.compile('.*[,!?.;:\])}"\']\B') #any word with dots, colons,", ' or parenthesises at the end
    parenthesis = re.compile('[\[({"\'].*')    #any words with parenthesises or " ' in front
    urls = re.compile('http[s]?://.+')        #any http:// and https:// URLs

    endreached = False

    while endreached != True:

        word = wordlist[i]
        changedWord = False



        #remove parenthesises in front of words
        if parenthesis.match(word) != None:
##            print('Parenthesis found: ' + word + ' at position ' + str(i))
            word = word[1:]
            removedWord = wordlist.pop(i)
##            print('Removed: ' + removedWord)
            wordlist.insert(i, word)
##            print('Replaced with ' + word)
            changedWord = True                  # decrease i to double check words

        #remove dots, colons and parenthesises at the end
        if dotsAndColons.match(word) != None:
##           print('Dot or colon found: ' + word + ' at position ' + str(i))
           word = word[:-1]
           removedWord = wordlist.pop(i)
##           print('Removed: ' + removedWord)
           wordlist.insert(i, word)
##           print('Replaced with ' + word )
           changedWord = True                   # decrease i to double check words (e.g. 'end).' )


        #remove URLs and email addresses from wordlist
        if email.match(word) != None or urls.match(word) != None:
##            print('Email/URL found: ' + word + ' at position ' + str(i))
            wordlist.pop(i)
##            print('Removed!')
            i -= 1                  # decrease i, as wordlist has just become shorter

        #remove empty words
        if word == '':
            wordlist.pop(i)


        #if a word was changed, decrease i to double check it for another unwanted character
        if changedWord:
            i -= 1

        i += 1

        #step out of loop if end is reached
        if i == len(wordlist) :
            endreached = True

    return wordlist


#---------------------------------------------------------
# KICK STOPWORDS

def kickStopwords(wordlist):
    """receives a list of words and removes all stopwords that appear in an internal list.
        Returns that cleaned up list."""
    stopwords = open('stopwords_eng.txt').read().lower().split()

    i = 0
    endreached = False

    while endreached != True:
        word = wordlist[i]

        for stopword in stopwords:
            if word == stopword:
                #delete it
##                print('Remove ' + wordlist[i])
                wordlist.pop(i)
                i -= 1

        i += 1
        if i == len(wordlist) :
            endreached = True

    return wordlist


#---------------------------------------------------------
# STEMMING
import porterstemmer
import nltk.stem.lancaster

def stemWords(wordlist):
    """ receives a list of words and returns the list with stemmed words"""

    #using Porter Stemmer for a start
    # lancStemmer = nltk.stem.lancaster.LancasterStemmer()
    porterStemmer = porterstemmer.PorterStemmer()

    i = 0
    endreached = False

    while endreached != True:
        #stem word at position i
        wordlist[i] = porterStemmer.stem(wordlist[i], 0, len(wordlist[i]) - 1)

        i += 1
        if i == len(wordlist) :
            endreached = True

    return wordlist


#---------------------------------------------------------
# GENERATING TF-IDF-VECTOR

# Counting term frequency
def termFrequency(wordlist):
    """Receives a list of words and return a dictionary with (word: frequency) pairs"""
    wordDict = {}

    for word in wordlist:
        if wordDict.get(word) == None:
            #word not in dictionary yet, insert
            wordDict.setdefault(word, 1)
        else:
            #word in dictionary, update value
            wordDict.update({word: wordDict.get(word) + 1})

    return wordDict

#get maximum term frequency
def getMaxTermFrequency(wordDict):
    """Receives a dict with (word: frequency) pairs and return the highest frequency value"""
    maxtf = 0
    for word in wordDict:
        tf = wordDict.get(word, -1)
        if tf > maxtf:
            maxtf = tf

    return maxtf




def normTF(wordDict):
    """Receives a dictionary with (word: frequency) pairs and replaces the frequency value
        with the normalized term frequency value"""
    maxtf = getMaxTermFrequency(wordDict)

    
    for word in wordDict:
        wordDict.update({word: wordDict.get(word)/maxtf})

    return wordDict


def invDocFreq(wordDict, totalDocuments):
    """Receives a dictionary with amounts of documents that a word appears in and
        the number of total documents. Replaces the value with the the inverse
        document frequency (log(totalDocuments/amount) ) and returns the dictionary."""

    for word in wordDict:
        wordDict.update({word: math.log10(totalDocuments/wordDict.get(word))})

    return wordDict


def getMostNWords(dictList, n):
    """Receives a list of dictionaries with (word: absolute frequency) pairs and adds up the
        frequencies for every word. Then returns a dict with (word: total frequency) pairs
        for the most n words."""

    temp = {}

    for wordDict in dictList:
        for word in wordDict:
            if temp.get(word) == None:
                #word not in temp dictionary yet
                temp.setdefault(word, wordDict.get(word))
            else:
                #word already in temp dictionary. Update value
                temp.update({word: temp.get(word) + wordDict.get(word)})

    # create a sorted list from elements in dictionary
    result = sorted(temp.items(), key=lambda x: x[1], reverse=True)


    #return only most n ones
    return result[:n]

def getMostNDocFreqWords(wordDict, n):
    """Receives a dictionary with amount of documents a word appears in and a number n.
        Transforms the dict in a list with descending order and returns the first n elements."""

    # create a sorted list from elements in dictionary
    result = sorted(wordDict.items(), key=lambda x: x[1], reverse=True)

    return result[:n]



###################################################################
# MAIN BODY

from bs4 import BeautifulSoup
import re
import glob
import math

#sample file for presentation:
#filelist = glob.glob('testdata2/*.html')

#regular training data set from Aufg01
filelist = glob.glob('../Aufg01/trainingData/*--fulltext*.html')

#counts, in how many documents a word appears with (word: absolute frequency) pairs
totalWordAppearenceDict = {}
#a list that contains for every document the dictionary with normalized term frequencies
dictList = []

#list that contains the class for every document, either course or non-course
classList = []

#list that contains the most n words appearing in training set
n = 400
mostNWords = []

#to store index of sample file in presentation
index = -1

for file in filelist:

    try:
         
        #catch index of sample file for presentation
        if file == '../Aufg01/trainingData\\train--fulltext--course--BEG--cs.washington.edu^education^courses^590D^autumn95.html':
            index = filelist.index(file)
            print('FOUND IT: ' + str(index))

    
        data = open(file, 'r', encoding='utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        wordlist = soup.get_text().lower().split()

        #course or non-course
        svmClass = file.split('--')[2]
        classList.append(svmClass)

        #wordlist = ['(((aaa:', 'https://google', 'aa:a?!', '"zzz,?!""', 'abc@xyz.de.', 'bbb)...', 'http://google.com', 'https://www.google.com/', '[ccc.)', 'ddd.', 'eee])', 'fff.', '(xyz@abc.com', 'ggg:']

        #wordlist without dots, colons, parentheses, URLs, email addresses etc.
        wordlist = removeDots(wordlist)

 
        #wordlist without stopwords and stemmed
        wordlist = kickStopwords(wordlist)
##        print('Length without stopwords: ' + str(len(wordlist)))
##        print('Unstemmed words: ')
##        print(wordlist)
        wordlist = stemWords(wordlist)
##        print('Stemmed words: ')
##        print(wordlist)

        #dictionary with (word: absolute frequency) pairs
        wordDict = termFrequency(wordlist)

        #append copy of dict with (word: abs. frequency) to mostNWords for later selection of the most n words
        mostNWords.append(wordDict.copy())


        #add words and number of documents they appear in to totalWordDict
        for word in wordDict:
            if totalWordAppearenceDict.get(word) == None:
                #word not in dictionary yet
                totalWordAppearenceDict.setdefault(word, 1)
            else:
                #word already in dictionary. Update value
                totalWordAppearenceDict.update({word: totalWordAppearenceDict.get(word) + 1})
        

        #dictionary with (word: normalized term frequency) pairs
        wordDict = normTF(wordDict)

        #list that contains the normalized dictionary for every file of the testdata
        dictList.append(wordDict)

    except: 
        print('Failed to open file ' + file)
        #filelist.remove(file)




##print('totalWordAppearenceDict:')
##print(totalWordAppearenceDict)


##print('----------------------------------------------------------')
invDocFreqDict = invDocFreq(totalWordAppearenceDict.copy(), len(filelist))
##print('INVERSE DOCUMENT FREQUENCY:')
##print(invDocFreqDict)

#contains the TF-IDF-Vector for every document
tfIdfList = []
for dictionary in dictList:
    vector = {}
    for word in dictionary:
        tf = dictionary.get(word)
        idf = invDocFreqDict.get(word)
        weight = tf * idf
        vector.update({word: weight})

    tfIdfList.append(vector)

#print tfIdfVector of presentation sample file (index-1 because
#one file in filelist could not be opened)
#print(tfIdfList[index-1])


##print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
##print('TF-IDF-LIST:')
##print(tfIdfList[:2])

#mostNWords = getMostNWords(mostNWords, n)
mostNWords = getMostNDocFreqWords(totalWordAppearenceDict.copy(), n)
print('++++++++++++++++++++++++++++++++++++++++++++')
print('The ' + str(n) + ' in most documents appearing words:')
print(mostNWords)
print(len(mostNWords))
print('++++++++++++++++++++++++++++++++++++++++++++')
#print(len(totalWordAppearenceDict))
#print(totalWordAppearenceDict)


file = open('data.txt', 'w')

print('length of filelist: ' + str(len(filelist)))
print('length of classList: ' + str(len(classList)))
print('length of tfidfList: ' + str(len(tfIdfList)))

endreached = False
i = 0
while endreached != True:
    tfIdf = tfIdfList[i]
    svmClass = classList[i]
    line = ''

    if svmClass == 'course':
        line = '+1 '
    else:
        line = '-1 '

    j = 1
    for word in mostNWords:
        #if tf-idf-Vector contains one of the mostNWords, get tf-idf-Value
        #and append to string
        if tfIdf.get(word[0]) != None:
            line = line + str(j) + ':' + str(tfIdf.get(word[0])) + ' '
        j += 1

    #output of sample file for presentation (index-1 because
    #one file in filelist could not be opened)
    if i == index-1:
        print(line)
        
    file.write(line + '\n')

    i += 1

    #go through loop for every TF-IDF-Vector in list
    if i == len(tfIdfList):
        endreached = True

file.close()

        
#Wait for user input to stop program
input("Press <ENTER> to continue")
