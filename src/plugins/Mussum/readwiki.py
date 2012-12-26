#
# Copyright (c) 2011, Rodrigo Dias Cruz
# All rights reserved.
#
# This file is part of Mussum IRC-Bot.
#
# Mussum IRC-Bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mussum IRC-Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Mussum IRC-Bot. If not, see <http://www.gnu.org/licenses/>.
#


#
# IMPORTS
#
import re
import urllib2


#
# CONTANTS AND DEFINITIONS
#
ENTRY = re.compile('(<.*>)*(.*)')
MACHINES_URL = 'https://ltc3.linux.ibm.com/wiki/LTCBrazil/UPP/Machines?action=raw'


#
# CODE
#
def getMachinesPage():
    """
    Downloads the machines wiki page and returns its lines as an array

    @rtype: list
    @returns: lines of the machines wiki page
    """
    # download the page
    stream = urllib2.urlopen(MACHINES_URL)
    data = stream.read()
    stream.close()

    # split into lines and return
    return data.splitlines()
# getMachinesPage()

def parseLine(headers, line):
    """
    Strips the passed line into columns separated by || and returns a dictionary
    mapping the passed headers to those columns

    @type  headers: list
    @param headers: headers to be used

    @type  line: basestring
    @param line: line to be parsed

    @rtype: dict
    @returns: mapping of headers to columns
    """
    # split the passed line into columns removing any leading <...> tags
    columns = []
    
    for column in line.split('||')[1:-1]:
        columns.append(ENTRY.match(column).groups()[1].strip() or None)
    
    # map headers to columns and return
    mapping = {}

    for key, value in zip(headers, columns):
        mapping[key] = value

    return mapping
# parseLine()

def parseMachinesTable():
    """
    """
    # list
    machines = []

    # ble
    lines = getMachinesPage()

    # ble
    handler = skipTrash
    index = 0

    while handler != None:
        handler, index = handler(machines, lines, index)

    # bli
    return machines
# parseMachinesTable()

def parseTable(machines, lines, index):
    """
    """
    # get headers
    headers = [h.strip().lower() for h in lines[index].split('||')[1:-1]]
    index += 1

    # parse lines and map headers to columns
    for line in lines[index:]:
        if line[0:2] != '||':
            return skipTrash, index

        # xxx
        machines.append(parseLine(headers, line))
        index += 1

    # no more lines: stop state machine
    return None, -1
# parseTable()

def skipTrash(machines, lines, index):
    """

    @rtype: Array
    @returns:
    """
    # iterate over lines until a table header is found
    for line in lines[index:]:
        if line[0:2] == '||':
            return parseTable, index

        index += 1

    # no table header found: stop state machine
    return None, -1
# skipTrash()


