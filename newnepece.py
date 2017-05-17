#!/usr/bin/env python3

"""
newnepece.py
Usage: newnepece.py
Checks MangaStream page for new One Piece chapters
and should it find a new one, prints the chapter number,
name and URL to command line.
"""

import urllib.request
import os
import re
from bs4 import BeautifulSoup
from time import sleep
import sys

URL = "http://mangastream.com/manga/one_piece"
newest = 0
save_location = "newnepece.dat"
chapter = ()

def getfromurl(url):
    """
    Gets HTML for the specific page and returns it as array of bytes.

    Args: 
        url (str): location of the page

    Returns:
        bytes, the HTML page requested
    """
    try:
        html = urllib.request.urlopen(url).read()
        return html
    except Exception as e:
        print(e)
        return

def parse(data):
    """
    Parses a list of elements for chapters, returns either Boolean True
    if there is a new chapter or Boolean False if there are no new chapters.
    
    Args:
        data (list): A list of elements to be parsed

    Returns:
        Boolean: True if a new chapter is found, False otherwise.
    """
    global chapter
    global newest
    regex_url = re.compile("http://readms.net/r/one_piece/[0-9]+/[0-9]+/1")
    regex_number_and_name = re.compile("[0-9]+.?-.?[\"a-zA-Z0-9\?\!\,\.\'\:\s]+")
    for element in data:
        searchable = str(element)
        try:
            chapter_url = re.search(regex_url,searchable)
            chapter_number_and_name = re.search(regex_number_and_name,searchable)
            cnn = chapter_number_and_name.group(0)
            dash_index = cnn.find('-')
            chapter_number = cnn[0:(dash_index-1)]
            chapter_name = cnn[(dash_index+2):]
            chapter_url_str = chapter_url.group(0)
            if int(chapter_number) > newest:
                newest = int(chapter_number)
                chapter = chapter_url_str, chapter_number, chapter_name
                return True
            else:
                return False
        except:
            return False

def parsehtml(html):
    """
    Searches bytes for lines with link to One Piece chapter.
    Returns a list with aforementioned chapters.

    Args:
        html (bytes): data to be searched for

    Returns:
       list: a list of data
    """
    soup = BeautifulSoup(html)
    r = []
    for e in soup.findAll('a', attrs={'href': re.compile("http://readms.net/r/one_piece")}):
        r.append(e)
    return r

def save(savable):
    """
    Saves a tuple to a file. Does not return anything.

    Args:
        savable (tuple): the data that should be saved.
    """
    output = os.path.join(os.getcwd(),save_location)
    with open(output,'w+') as out:
        try:
            line_to_write = savable[0] + " " + savable[1] + " - " + savable[2]
        except:
            line_to_write = ''
        out.write(line_to_write+"\n")

def load():
    """
    Loads data from a file to a list, in case the file contains
    more than one line which it shouldn't. Never know though.
    Returns Boolean True if loading the file was successful,
    otherwise returns Boolean False and creates the file with
    nothing in it.

    Returns:
       Boolean: True if successful, False otherwise.
    """
    global chapter
    load_file = os.path.join(os.getcwd(),save_location)
    try:
        with open(load_file,"r") as ins:
            lines = []
            for line in ins:
                lines.append(line)
            if parse(lines):
                return True
            else:
                return False
    except:
        save('')
        return False

def mainloop(n):
    """
    The main loop. Runs from here to eternity,
    sleeping for n seconds between runs.
    First we check whether or not we can get HTML
    from the (as of now hard-coded) URL - if we can,
    we parse this HTML with parsehtml, after which we
    parse the data provided by parsehtml. If, while parsing,
    we find that a new chapter has been released, we print
    a message that tells this and save the info.
    
    Args:
        n (int): time to sleep between runs.
    """
    while(True):
        data = getfromurl(URL)
        if data:
            loc = parsehtml(data)
            t = parse(loc)
            if t:
                print("New Chapter: {} - {} {}".format(chapter[1],chapter[2],chapter[0]))
                save(chapter)
        sleep(n)

if __name__ == "__main__":
    try:
        load()
        mainloop(600)
    except KeyboardInterrupt:
        print("Exiting")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
