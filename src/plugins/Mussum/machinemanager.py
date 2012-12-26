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
from db import DataBase


#
# CODE
#
class MachineManager(object):
    """
    This represents an entity which manages a set machines available to be used
    """

    def __init__(self):
        """
        Constructor. Initializes the list of machines.

        @rtype: None
        @returns: nothing
        """
        self.__db = DataBase()
    # __init__()

    def add(self, name, ip = None, id = None, group = None):
        """
        Adds a machine with the passed name

        @type  name: basestring
        @param name: machine name

        @type  ip: basestring
        @param ip: machine IP address

        @type  id: basestring
        @param id: machine ID in its controller (IVM, HMC, BladeCenter, ...)

        @type  group: basestring
        @param group: group the machine belongs to

        @rtype: bool
        @retruns: 0 - success
                  1 - machine already exists
        """
        # machine already exists: error
        if name in self.__db.getMachines():
            return 1

        # add machine
        self.__db.add(name, ip, id, group)

        # success
        return 0
    # add()

    def getInfo(self, name):
        """
        Returns info about the machine with the passed name, or None if the
        machine does not exist. The info is returned as a dictionary like this:

            info = {
                'name': 'machineA',   # machine name
                'ip': '192.168.0.37', # machine ip
                'id': 2,              # machine id
                'group': 'groupA'     # group the machine belongs to
                'user': 'userX',      # who is using the machine, or None
                'start': 1309049448,  # when machine became reserved or
            }                         # available, as returned by time()

        @type  name: basestring
        @param name: machine name

        @rtype: dict or None
        @returns: info about the machine, None if it does not exist
        """
        # machine does not exist: error
        info = self.__db.getInfo(name)

        if len(info) == 0:
            return None

        # exists: return info
        return info
    # getInfo()

    def listAvailable(self):
        """
        Returns the names of all machines that are currently available

        @rtype: list
        @retruns: names of all machines that are currently available
        """
        return self.__db.getAvailable()
    # listAvailable()

    def listByUser(self, user):
        """
        Returns the names of all machines that are currently reserved

        @rtype: list
        @retruns: names of all machines that are currently reserved
        """
        return self.__db.getByUser(user)
    # listByUser()

    def listMachines(self):
        """
        Returns the names of all machines contained in this manager

        @rtype: list
        @retruns: names of all machines contained in this manager
        """
        return self.__db.getMachines()
    # listMachines()

    def listReserved(self):
        """
        Returns the names of all machines that are currently reserved

        @rtype: list
        @retruns: names of all machines that are currently reserved
        """
        return self.__db.getReserved()
    # listReserved()

    def listUsers(self):
        """
        Returns the users which currently have reserved machines

        @rtype: list
        @retruns: users which currently have reserved machines
        """
        return self.__db.getUsers()
    # listUsers()

    def release(self, name):
        """
        Adds a machine with the passed name

        @type  name: basestring
        @param name: machine name

        @rtype: int
        @retruns: 0 - success
                  1 - machine does not exist
        """
        # machine does not exist: error
        if name not in self.__db.getMachines():
            return 1

        # release machine
        self.__db.reserve(name, None)

        # success
        return 0
    # release()

    def remove(self, name):
        """
        Removes the machine with the passed name

        @type  name: basestring
        @param name: machine name

        @rtype: int
        @retruns: 0 - success
                  1 - machine does not exist
        """
        # machine does not exist: error
        if name not in self.__db.getMachines():
            return 1

        # remove machine
        self.__db.remove(name)

        # success
        return 0
    # remove()

    def reserve(self, name, user):
        """
        Sets the machine with the passed as reserved for the passed user

        @type  name: basestring
        @param name: machine name

        @type  user: basestring
        @param user: user the machine is to be reserved for

        @rtype: int
        @retruns: 0 - success
                  1 - machine does not exist
                  2 - machine is already reserved
                  3 - user has no permissions
        """
        # machine does not exist: error
        info = self.__db.getInfo(name)

        if len(info) == 0:
            return 1

        # machine is already reserved: error
        if info['user'] != None:
            return 2

        # user has no permissions: error
        group = info['group']

        if group != None and user not in self.__db.getUsersByGroup(group):
            return 3

        # reserve machine
        self.__db.reserve(name, user)

        # success
        return 0
    # reserve()

# MachineManager


