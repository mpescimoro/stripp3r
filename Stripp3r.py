#!/usr/bin/env python

"""
Author : pescimoro.mattia@gmail.com
Licence : GPL v3 or any later version

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from html.parser import HTMLParser
from urllib.request import urlopen
import datetime
import time
import locale
import requests
from lessonEntity import Lesson
from bs4 import BeautifulSoup # html5 smart parser

# set the locale to italian. This is mandatory for operate with the dates into the University of Brescia pages. It allow
# the right interpretation of the date string in italian (month name) and make the script independent from the system
# locale
locale.setlocale(locale.LC_ALL, "it_IT")


class MLStripper(HTMLParser):
    def __init__(self):  # Override here
        HTMLParser.__init__(self)
        # todo: add documentation
        self.immolation = False
        # is the line counter for parsing the header data
        self.is_header = 0
        # is the time of the firts hour of lessons. Mandatory to calculate the start hour from offsets
        self.firstHour = datetime.datetime.strptime("08:30", "%H:%M")
        # the lesson database entity
        self.lesson = Lesson()
        self.dataLine = 0
        self.semesterStartDate = datetime.datetime
        self.semesterEndDate = datetime.datetime

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for attr in attrs:
                if attr[0] == 'id':
                    self.immolation = True
                    # Hours coded from 0 to 9 as the nine hours avalaible in a standard lesson day from 08:30 to 09:30
                    # Day coded form 0 to 6 where 0 is monday and 6 is sunday.
                    coords = attr[1].split(sep='_')  # Format as follow: DAY_HOUR
                    self.lesson.day = coords[1]
                    # calculate the correct start hour for the lesson
                    dt = self.firstHour + datetime.timedelta(hours=int(coords[2]))
                    self.lesson.hour = dt.time()
                    # print(self.lesson.hour) #DEBUG
                    # print(coords) #DEBUG
        if tag == 'td':
            for attr in attrs:
                # find the header with the information regarding the semester
                if attr[1] == 'ttTitleTD':
                    # count the lines of the header
                    self.is_header += 1
                    # print('Pippo '+str(self.is_header)) #DEBUG

    def handle_endtag(self, tag):
        if tag == 'table':  # or tag == 'br' #DEBUG
            self.immolation = False

    def handle_data(self, data):
        if self.is_header > 0:
            self.is_header += 1
            # print('Pippo '+str(self.is_header)) # DEBUG
        if self.immolation and data.strip():
            # count the 4 lines of data for the lesson (subject, teacher, rooms, address)
            if self.dataLine <= 3:
                # pass #DEBUG
                if self.dataLine == 0:
                    self.lesson.subject = data
                    print(self.lesson.subject) #DEBUG
                if self.dataLine == 1:
                    self.lesson.teacher = data
                    print(self.lesson.teacher) #DEBUG
                if self.dataLine == 2:
                    self.lesson.rooms = data
                    print(self.lesson.rooms) #DEBUG
                if self.dataLine == 3:
                    self.lesson.address = data
                    print(self.lesson.address) #DEBUG
                # print(data.upper())  # DEBUG
                self.dataLine += 1
            # if is the last line
            if self.dataLine == 4:
                print("---------------------------------------")  # DEBUG
                self.lesson.semesterStartDate = self.semesterStartDate
                self.lesson.semesterEndDate = self.semesterEndDate
                self.dataLine = 0
                self.lesson.persist()
        #         reset the entity
                self.lesson = Lesson()
        if self.is_header == 9:  # find the correct line
            # print(data.upper()) #DEBUG
            # extract the data information and foreach date create the datetime object
            line = data.split(sep="-")
            self.semesterStartDate = datetime.datetime.strptime(line[0], ": %A %d %B %Y ")
            self.semesterEndDate = datetime.datetime.strptime(line[1], " %A %d %B %Y")
            # print(self.semesterStartDate) #DEBUG
            # print(self.semesterEndDate) #DEBUG
            self.is_header = 0


# URL goes here

AA ='2015-2016'
unknownCode = '160'
# is the homepage of the calendars
url = 'https://calendari.unibs.it/EasyCourse/Orario/Area_di_Scienze_Ingegneristiche/'+AA+'/'+unknownCode+'/'
html_doc = requests.get(url+'index.html')

htmlSoup = BeautifulSoup(html_doc.text, 'html.parser')
courses = []
# find all the links to the courses calendar from the menu of the index page.
for link in htmlSoup.find_all('a'):
    if link.get('href').find('Curricula', 0, 10) == 0:
        courses.append(url+link.get('href'))
for calendar in courses:
    fetch = urlopen(calendar)
    parser = MLStripper()
    data = fetch.read().decode('iso-8859-1')  # Welcome back to 1987!
    parser.feed(data)  # OM NOM NOM
    parser.close()

# DISCLAIMER: this is random coding that relies on HTML formatting of a specific webpage. 
# Thus the only thing that keeps it working is the belief in lazy people.
