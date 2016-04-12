from database import *
from search import search
import os
import sys
import requests

# Define alternate commands for database managment
db_commands = {'purge':purge, 'skip':skip, 'remove':remove, 'ls':list_collected_domains}

#Get the user to input a page on the domain that is to be searched
base_url = input("\nHello!\nWelcome to this web search program.\nGo ahead enter the url \
that you want to search:\n")

url = base_url
print()

#Give managment aspect to the database
if url in db_commands:
    url = db_commands[url]()
    base_url = url

else:
    # Ensure page can be reached
    while True:
        try:

            r = requests.get(url, verify = False)#Get the pages data
        except:
            url = input('Please enter a different URL the last one was invalid or could not be connected to.\n')
            base_url = url
            continue
        break

    file_path = os.getcwd()+'/data/'+getDomain(url)

    # Validity check for the number of links
    depth = None
    while type(depth) is not int:
        depth = input("How many links would you like to check.\n")
        try:
            depth = int(depth)
        except:
            pass
        if type(depth) is not int:
            print("Invalid number. Type provided:"+str(type(depth)))

    # Get the initial page file
    visited = collect(url)

    #get the info for the next page
    domain = getDomain(url)
    dir_path = get_dir(domain)
    cwd = os.getcwd()
    # Open links file and get the data and properties
    links = open(cwd+'/data/'+domain+'/links.txt', 'r+')
    current_links = links.readlines()
    length_of_file = len(current_links)
    line_in_file = 0

    #While there are still more pages to scrape, scrape them
    while line_in_file < length_of_file and line_in_file < int(depth)+1:


        # Update the current version of the file
        links.close()
        links = open(cwd+'/data/'+domain+'/links.txt', 'r+')
        current_links = links.readlines()
        length_of_file = len(current_links)
        sys.stdout.write(str(line_in_file+1)+'/'+str(depth)+'\r')
        sys.stdout.flush()
        url = current_links[line_in_file]
        try:
            visited = collect(url, visited)
        except:
            pass
        line_in_file += 1


    links.close()

word = ''

if url is not None:
    while word != '_end_':
        word = input("Please enter a word to search for: ")
        result = search(word, base_url)
        print(result)
