import os
import shutil
from sort import*
from scrape import*


class Page:
    '''
    Class for holding the different data for a web page
    -title: holds the most important words(the title of the page)
    -heading: holds next most important words (all of the headings)
    -text: holds the majority of the pages contents (all of the paragraphs)
    '''
    def __init__ (self, title = None, heading = None, text = None):
        '''data is passed as arrays'''
        self.title = title
        self.heading = heading #heading are the data from <h#> tags (NOT <head>)
        self.text = text #data from <p> tags

    def __repr__ (self):
        return self.title + '\n' + self.heading + '\n' + self.text


def get_dir (url):
    '''
    Finds the path to the directory made for the url's domain.
    Creates the directory if it does not exist already
    -url: the url of the web page for which a path to the base domain will be found
    O(1)
    '''
    cwd = os.getcwd() # Find the user's location in their file system (should always be the same)
    domain = getDomain(url) # Retrieve the base domain for the inputted url

    # Check if there is a data folder, if not make one (this should only create one once)
    if not os.path.exists(cwd+"/data"):
        # The 'data' directory holds all for the files for all of the domains
        os.makedirs(cwd+"/data/")

    dir_path = cwd+'/data/'+domain # Path to the folder for the given domain

    # Check if there is a folder for this specific domain
    if not os.path.exists(dir_path):
        # This domain folder should contain all of the imformation for that specific domain
        os.makedirs(dir_path)

    # Check if the domain's folder has a links file
    if not os.path.exists(dir_path+"/links.txt"):
        # The links file will keep a record of all of the links found in the domain
        f = open(dir_path+"/links.txt", 'w')
        f.close()

    # Pass the path to the domain's directory out (cwd+"/data/"+domain)
    return dir_path



def save_page (dir_path, page_inst, domain):
    '''
    Save the scraped data stored in the page object to a file at dir_path.
    This will over write an existing file if there is one with the same url
    -domain: used for a title of the file. Same as the page domain
    -page_inst: page object holding all of the data for the page
    -dir_path: path to the file
    O(1)
    '''
    # Create a list of words with the weighted values of differnt page parts
    array_to_save = []

    # The title is the most important so multiply it's frequencies by five and add the words
    for i in range(5):
        for word in page_inst.title:
            array_to_save.append(word)

    # The headings are the next most important so double their frequencies and add the words
    for i in range(2):
        for word in page_inst.heading:
            array_to_save.append(word)

    # Add the rest of the words found in the page's text
    for word in page_inst.text:
        array_to_save.append(word)

    # Open the file to save the data to
    f = open(dir_path+".txt", 'w')
    # Filter and save the data
    f.write(' '.join(filter_words(array_to_save))+'\n')
    f.close()



def getDomain(url):
    '''
    Returns the domain name for the given url
    O(1)
    '''
    try:
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        domainTitle = '{uri.netloc}'.format(uri=parsed_uri)
        return domainTitle
    except:
        return None



def collect(url, visited = None):
    '''
    Used to access a new page and put it's data into a page instance
    Controls the users specified operations
    Runs only if it needs to
    Running time depends on factors such as internet speed and cached results.
    '''
    # Find the locations of the files
    file_path = os.getcwd()+'/data/'+getDomain(url)

    # Create an empty set if visited is not supplied
    if visited is None:
        if os.path.exists(file_path):
            visited = set(os.listdir(file_path))

        else:
            visited = set()

    # Check if there is data existing for the website
    if os.path.exists(file_path):
        # Check if the page has been visited
        if url.replace('/', '|')+'.txt' not in visited:
            scrape(url)
    else:
        scrape(url)

    return visited




def purge():
    '''
    removes all of the data that has been collected
    O(1)
    '''
    cwd = os.getcwd()
    shutil.rmtree(cwd+'/data')
    print("Data purged.")
    return None

def remove():
    '''
    Removes all of the data that has been collected for one domain
    O(1)
    '''
    url = input('Enter a url for which you would like to remove the data for.\n')
    re_enter(url)
    shutil.rmtree(os.getcwd()+'/data/'+getDomain(url))
    return None

def skip():
    '''
    Don't collect any Data
    O(1)
    '''
    url = input('Please enter a url to skip the data collection for.\n')
    re_enter(url)
    return url

def re_enter(url):
    '''
    Check if user entered a non-existant url/domain
    '''
    # Check to ensure a valid URL was entered
    while getDomain(url) is None:
        url = input("Invalid url. Try another. Be sure to include 'https://''")
    # Get the file path
    file_path = os.getcwd()+'/data/'+getDomain(url)

    #Ensure data exists
    while not os.path.exists(file_path):
        url = input('No data exists yet for: '+file_path+'\nEnter a different url.\n')
        file_path = os.getcwd()+'/data/'+getDomain(url)

    return url

def list_collected_domains():
    '''
    Display a list of the collected domains
    O(1)
    '''
    try:
        for data_dir in os.listdir(os.getcwd()+'/data/'):
            # Print out the direcorys
            if data_dir != "links.txt":
                # Get the number of pages scraped
                count = 0
                for p in os.listdir(os.getcwd()+'/data/'+data_dir):
                    count += 1
                print('https://'+data_dir+'  :   '+str(count))
    except:
        pass
    print('\n')
    return None
