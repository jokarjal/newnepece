#!/usr/bin/env python3

import urllib.request
import os
import re
from bs4 import BeautifulSoup
from time import sleep
import sys

URL = "http://mangastream.com/manga/one_piece"
newest = 0
save_location = "newnepece.dat"

def getfromurl(url):
    try:
        html = urllib.request.urlopen(url).read()
        return html
    except Exception as e:
        print(e)
        return

def parse(data):
    global newest
    chapter = list()
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
                element = chapter_url_str, chapter_number, chapter_name
                chapter.append(element)
                return chapter
            else:
                return
        except:
            return

def parsehtml(html):
    soup = BeautifulSoup(html)
    r = []
    for e in soup.findAll('a', attrs={'href': re.compile("http://readms.net/r/one_piece")}):
        r.append(e)
    return r

def save(savable):
    output = os.path.join(os.getcwd(),save_location)
    with open(output,'w+') as out:
        for element in savable:
            try:
                line_to_write = element[0] + " " + element[1] + " - " + element[2]
            except:
                line_to_write = ''
            out.write(line_to_write+"\n")

def load():
    load_file = os.path.join(os.getcwd(),save_location)
    try:
        with open(load_file,"r") as ins:
            lines = []
            for line in ins:
                lines.append(line)
        return parse(lines)
    except:
        save('')

def mainloop():
    while(True):
        data = getfromurl(URL)
        if data:
            loc = parsehtml(data)
            t = parse(loc)
            if t:
                print("New Chapter: {} - {} {}".format(t[0][1],t[0][2],t[0][0]))
                save(t)
        sleep(600)

if __name__ == "__main__":
    try:
        load()
        mainloop()
    except KeyboardInterrupt:
        print("Exiting")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
