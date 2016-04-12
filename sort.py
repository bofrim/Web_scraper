from nltk.corpus import stopwords
import string

def filter_words(words):
    '''
    Filter out the common words.
    Sort words alphabetically.
    Find and return frequency counts.
    O(number of words*log(number of words))
    '''
    # Get a list of all common english words and puncuation charachters
    cachedStopWords = stopwords.words("english")+list(string.punctuation)
    # Sort the words alphabetically
    words = sorted([word.lower() for word in words if word not in cachedStopWords])
    words.append("endstr______________")
    freq_array = []
    index = 0
    # Count the occurances of each word append representative strig to the list
    # The representative string is of the form: word::freq
    while index is not len(words)-1:
        count = 1
        if words[index] == "endstr______________":
            break
        while(words[index] == words[index+1]):
            count += 1
            index += 1
            #Add to the frequency array
        freq_array.append(words[index]+'::'+str(count))
        index += 1

    return freq_array
