from bs4 import BeautifulSoup
import re

#import file testdata.html for simplicity
#switch to data collection lateron
data = open('testdata.html', 'r', encoding='utf-8')
soup = BeautifulSoup(data, 'html.parser')
wordlist = soup.get_text().lower().split()

print(wordlist)
print(len(wordlist))
print('---------------------------------------------------')

#endlist = wordlist.copy()
i = 0
email = re.compile('.+@.+\..+')     #pattern of an email address
dotsAndColons = re.compile('[a-z-]+[\.:]') #any word with dots, colons or parenthesises at the end

# TODO: parenthesises

for word in wordlist:

    #remove dots and colons
    if dotsAndColons.match(word) != None:
       print('Dot or colon found: ' + word + ' at position ' + str(i))
       word = word[:-1]
       print('popped: ' + wordlist.pop(i))
       wordlist.insert(i, word)
       print('Changed to: ' + word + ' between ' + wordlist[i-1] + ' and ' + wordlist[i+1])


    #remove email addresses from wordlist
    if email.match(word) != None:
        print('Email found: ' + word + ' at position ' + str(i))
        wordlist.pop(i)
        print('Removed!')
                

    
    
    i += 1

print('---------------------------------------------------')
print(wordlist)
print(len(wordlist))
    

    
##    charlist = list(word)
##    for 

##for char in charlist:
##    if char = 
