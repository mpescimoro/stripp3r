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

class MLStripper(HTMLParser):
    def __init__(self): # Override here
        HTMLParser.__init__(self)
        self.immolation = False 

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for attr in attrs:
                if attr[0] == 'id':
                    self.immolation = True
                    coords = attr[1] # Format as follow: DAY_HOUR
                    print(coords.upper())

    def handle_endtag(self, tag):
        if tag == 'table': # or tag == 'br'
            self.immolation = False

    def handle_data(self, data):
        if self.immolation and data.strip():
            print(data.upper())

# URL goes here
url = 'https://calendari.unibs.it/EasyCourse/Orario/Area_di_Scienze_Ingegneristiche/2014-2015/85/Curricula/Ingegneriainformatica_LaureatriennaleDM270_3_Curriculumgeneraleaa2012-13_05713.html'
fetch = urlopen(url)
parser = MLStripper()
data = fetch.read().decode('iso-8859-1') # Welcome back to 1987!
parser.feed(data) # OM NOM NOM
parser.close()

# DISCLAIMER: this is random coding that relies on HTML formatting of a specific webpage. 
# Thus the only thing that keeps it working is the belief in lazy people.
