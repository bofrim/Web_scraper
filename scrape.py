import database
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from sort import*
import os

def get_contents(tag, conts = None):
    '''
    Recursively finds all of the string contents in a tag
    Use dymanic table to keep track of all of the strings
    O(num of words)
    '''
    if conts is None:
        conts = []

    # When there is a directly accessible string retrieve it
    if tag.string is not None:
        # Append and return the new contnts list when a string is found
        for word in tag.string.split():
            conts.append(word)
        return conts

    # When there is not a directly accessible string, look in each subtag
    else:
        for c in tag.contents:
            conts = get_contents(c, conts)
    return conts



def relevant_url(link, domain):
    '''
    Check if a given url is relavent
    It must be of the same domain and cannot be a link to a file
    O(1)
    '''
    # Ensure the link is of the same domain that we are looking at
    # Ensure the link has substance (not just '/') and the link is not a file
    if (str(link)[0] is "/" or database.getDomain(link) == domain) \
    and len(str(link)) > 1 \
    and not link.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mp3', '.pdf', '.txt')):
        # Link was valid
        return True
    else: # Link was not valid
        return False



def add_links(links, url):
    '''Add to the domain's links file
    O(num of links)
    '''
    # Locate the file
    cwd = os.getcwd()
    domain = database.getDomain(url)
    dir_path = os.getcwd()+'/data/'+domain

    # Remove any duplicate links
    links = set(links)
    links_to_add = set()

    # Get the links file for the domain
    f = open(dir_path+"/links.txt", 'r+')
    # Get all of the links that are already in the file
    links_file = f.read().splitlines() # <<<<<<<<<<<<<<<<----------------------<-<

    for link in links:
        # Only get the links that are relavent
        if relevant_url(link, domain):
            # Some links need to be constructed
            if link[0] is "/":
                link = 'https://'+domain+link
            # Standardize the ending of the files
            if link[-1] is '/':
                link = link[:-1]
            # Standardize a secure prefix
            link = link.replace('http://', 'https://')
            # Only add the link if it does not already exist in the file
            if link not in links_file:
                # Add to the set of links that will be added
                links_to_add.update([str(link)])

    # Add all of the valid links and save the file
    for s in links_to_add:
        f.write(s+"\n")
    f.close()



def scrape(url):
    '''
    Get all of the information from the page at the given url
    Save the data from the page to a file specific for that url
    O(num of words)
    '''
    r = requests.get(url, verify = False)#Get the pages data


    the_page = BeautifulSoup(r.content, 'lxml')#Converts data to Beautiful Soup object

    # Get the base domain for the given url
    domain = database.getDomain(url)
    # Find the path to where the page's data should be saved
    dir_path = database.get_dir(url)

    # Add all of the links to the links file
    links = the_page.find_all("a")
    for i in range(len(links)):
        links[i] = links[i].get("href")# Get the link
    add_links(links, url)

    # Get the title of the page
    title = the_page.title.string.split()

    #Get the important words in the headings
    heading = []
    for i in range(1,7):
        # Create a list for the heading tags
        h_tags = the_page.find_all("h"+str(i))
        # Go through each tag in the list and get its data
        for h in h_tags:
            h_contents = get_contents(h) # Returns an array of a bucnch of words
            if h_contents is not None and len(h_contents) is not 0:
                for word in h_contents:
                    heading.append(word)

    # Get all of the page's text
    text = []
    paragraphs = the_page.find_all("p")
    for p in paragraphs:
        p_contents = get_contents(p)
        if p_contents is not None and len(p_contents) is not 0:
            for word in p_contents:
                text.append(word)

    #lists = the_page.find_all("li")
    #   for l in lists:
    #     l_contents = get_contents(l)
    #     if l_contents is not None and len(l_contents) is not 0:
    #         for word in l_contents:
    #             text.append(word)

    # Add the data from the page to a Page instance and save it to a file
    page_inst = database.Page(title, heading, text)
    database.save_page(dir_path+'/'+url.replace('/', '|'), page_inst, domain)
