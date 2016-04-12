import database
import os

def find_word(word_set,word):
    '''
    Given a an array of words and their frequencies in the form of:
            [word1::freq1, ..., wordn::freqn]
    determine if the paramater 'word' is contained in that set and return its frequency.
    Return None otherwise
    O(log n), where n is number of words (using divide and conquer)
    '''
    first = 0

    last = len(word_set) - 1

    while(True):

        if first == last:
            word_info = word_set[first].split("::")
            if word_info[0] == word:
                return int(word_info[1])
            else:
                return 0

        mid = int((first + last)/2)

        if word_set[mid] < word:
            first = mid + 1

        elif word_set[mid] > word:

            if word_set[mid] < word:
                word_info = word_set[mid].split("::")
                if word_info[0] == word:
                    return int(word_info[1].replace(':', ''))
                else:
                    return 0
            last = mid



def find_all_files(path, all_files = None):
    '''
    Find all of the files under the given path
    Return an array of all of the file paths found
    O(num of files)
    '''
    if all_files == None:
        all_files = []

    # Look through the files and directories at the given path
    for data_file in os.listdir(path):
        # If a file containing page contents is found, add it to the list
        if data_file != "links.txt":
            if data_file.endswith('.txt'):
                all_files.append(path+'/'+data_file)
            # If a direcory is found, add all of the files in that directory to the list
            else:
                all_files = find_all_files(path+'/'+data_file, all_files)

    return all_files


def search(words, url):
    '''
    Find the page that is most relavent to the word 'word' within the 'domain'
    If the page is not found, return 'No Page Found'

    Longest function:
    O(num of files * log (num of words in file))
    '''
    page_found = ''
    highest_freq = 0
    # Get the directory of the domain that is being searched
    domain = database.getDomain(url)
    dir_path = os.getcwd()+'/data/'+domain

    # Check every file in the domain's directory for the 'word'
    for data_file in find_all_files(dir_path):
            f = open(data_file, "r")
            word_set = f.readline().replace('\n', '').split()
            freq = 0
            for word in words.split():
                try:
                    freq += find_word(word_set, word.lower())
                except:
                    freq += 0
            if highest_freq < freq:
                highest_freq = freq
                page_found = data_file
    if page_found != '' and highest_freq > 0:
        return (page_found.replace('.txt', '').split('/')[-1].replace('|', '/'))
    else:
        return 'No Page Found'
