CMPUT 275 Final Project
Brad Ofrim
Jordan Lane

Web Domain Searcher

**Ensure you have a reliable internet connection

**Also if you have a Mac, the testing will be much faster incomparison to
the Ubuntu VM based on my test results.

**

Description:
  This program allows the user to scrape internet domains and
  search the domain for keywords. The program will first compile
  a database of webpages from the domain of the user supplied URL.
  This part takes a long time since the program must send a request
  and wait for a response from the website. The program will then
  search it's database to find the page with the most frequent use
  of the user inputted keywords.

Installation:
  To use the program open the terminal and follow a few setup steps:

  -Ensure pip3 is installed

  -Install requests: $ sudo pip3 install requests

  -Install beautiful soup 4: $ sudo pip3 install beautifulsoup4

  -Install lxml parser: $ pip3 install lxml

  -Install Natural Language toolkit: sudo pip3 install -U nltk
    (or visit http://www.nltk.org/install.html)
      -Open python interpreter
      -run: >>> import nltk
            >>> nltk.download()
      -click on the "corpora" tab of the pop up window
      -find "stopwords" from the list, double click it

Directions:

  Now that all of the installation steps are complete. You can actually
  run the program by following these steps:

  -Open the terminal

  -Navigate to the directory with the project's files

  -Run: $ python3 UI.py

  -When prompted enter a URL of a webpage
      This URL must be a valid URL of the program will give errors
      It must start with http:// or https://
      Some pages won't work at all and others may work on occasion.
      Most pages should work fine though.
      Wikipedia will work some times and not others. If a page returns
      no search results try different words or try a different domain.
      This inconsistency is probably something to do with the website
      and as far as I can tell not to do with this program.

  -When prompted, enter the number of links that you would like the program
    to search. Keep in mind that on average the program will take about
    one second per page. Some pages will be faster than others (youtube is
    pretty fast). The process is drastically sped up if the domain has already
    been scraped. It still will take a few seconds to check to see if it has
    all of the data that it needs when the data already exists in the database.
    There is a way to not scrape if the data is already collected. It is
    explained later. You can search as many links as you want
    but the data collection program will slow down as it is taxed by processes
    such as ensuring that is is not adding links to the file containing all of
    the links that it has found.

    I would recommend scraping 100-500 links to get decent results. The longer
    if runs, the better the results it will get. The program will preform quite
    well up until the 3000 - 5000 link mark.

  -Wait for the program to store the contents of the pages

  -When prompted, input search words and the program will output a url to the
    page that it found that had the most frequent occurrences of the search
    words.
      *Note: If you enter multiple words the program will still function fine,
      but the page will most likely not be the one that you actually want. The
      program does not account for substrings or sentences, it simply counts
      frequencies. Only enter a few words (2 or 3) for best accuracy.

  -Try copying the link that the program provides into a web browser and
    search that specific page for you key words to check the results of the
    program.

Other functionality:
  -There are a few commands that provide more functionality to this project.
    Enter these instead of entering the initial URL:

    -purge: Deletes all data.
    -remove: Prompts user for a URL to remove the data for the URL's domain
    -skip: Prompts user for a URL to skip the data collection for and just
      go to the searching part (very useful)
    -ls: print a list of the collected domains and the amount of links they have


Advice for testing:
  The program will work on any size of website but I have found that it is
  very useful for smaller domains where there are less than 100 links that
  comprise the whole domain. In this case the program is able to search the
  full website and it provides useful results. When a large website is used
  the program is unable to cover much of the domain and will often output only
  a few pages if they have lots of words on them.

Algorithms:
    There are various parts of this program that use programming techniques.
  Dynamic programming was useful for functions such as "find_all_files",
  where the program is able to recurse through a directory with directories
  inside of it in order to find all of the files that it needs (Useful for
  specific cases but generally not actually used by the program). Recursion
  was also used in functions such as "get_contents".
    The most algorithmic portion is the program is the "find_word" function that
  utilizes binary search in order to quickly find words from a long array of
  alphabetically sorted words. This is the heart of the program and I do realize
  that a dictionary could have been used for quick lookup as well, however since
  the dictionary would have to be made every time, that would be linear and in
  this case it is simply logarithmic. If all data was only used once, it would
  have made sense to use dictionaries and add words as the key and frequencies
  as the values, but reading a file allows the data to be accessed later once
  a database is established.

  Testing:
    To test this program, I would recommend try in a website such as:
    http://www.apple.com/ca/ and running it a few times on this domain.
    Try first running it on about 50 links. Then try running it on 100 links.
    After these, try entering 'skip' instead of a URL at first, then enter
    the apple website url and then your keywords.
    Search for words like "iphone" or "mac" and see what is returned.
    Test a random sequence of characters or a word that you would not expect to
    be on the domain.

  If the program halts, try re-setting the internet connection and try again or
  re run the program on the same domain.




  Finally, if you would like to test an already scraped website download the
  folder from this link:
  https://www.dropbox.com/sh/u1nkyu6gcjjh2eu/AACB7yLuDXcPFYHXClDjU4K9a?dl=0

  Do not rename it. Place this folder inside the 'data' folder in the directory
  with all of the other file. Use the 'skip' command when prompted for a
  URL then enter https://www.worldsurfleague.com when prompted again for a URL.
  Search anything from that page that has to do with surfing! (beach, surf,
  water etc.)
