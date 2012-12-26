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
import os
import sqlite3
import time


#
# CONSTANTS AND DEFINITIONS
#
_PATH_DB = os.path.join(os.path.dirname(__file__), 'mussum.db')

_QUERY_ADD = 'INSERT INTO Machines (name, ip, id, grp, user, start) VALUES (?, ?, ?, ?, NULL, ?)'
_QUERY_ASSOCIATE = 'INSERT INTO Permissions (user, grp) VALUES (?, ?)'
_QUERY_CREATE_MACHINES = 'CREATE TABLE IF NOT EXISTS Machines (name VARCHAR PRIMARY KEY, ip CHAR(15), id SMALLINT, grp VARCHAR, user VARCHAR, start INT)'
_QUERY_CREATE_PERMISSIONS = 'CREATE TABLE IF NOT EXISTS Permissions (user VARCHAR, grp VARCHAR, PRIMARY KEY(user, grp))'
_QUERY_GET_AVAILABLE = 'SELECT name FROM Machines WHERE user is NULL ORDER BY name ASC'
_QUERY_GET_BY_USER = 'SELECT name FROM Machines WHERE user=? ORDER BY name ASC'
_QUERY_GET_INFO = 'SELECT name, ip, id, grp, user, start FROM Machines where name=?'
_QUERY_GET_MACHINES = 'SELECT name FROM Machines ORDER BY name ASC'
_QUERY_GET_RESERVED = 'SELECT name FROM Machines WHERE user is not NULL ORDER BY name ASC'
_QUERY_GET_USERS = 'SELECT DISTINCT user from Machines WHERE user is not NULL ORDER BY user ASC'
_QUERY_GET_USERS_BY_GROUP = 'SELECT user FROM Permissions WHERE grp=?'
_QUERY_REMOVE = 'DELETE FROM Machines WHERE name=?'
_QUERY_RESERVE = 'UPDATE Machines SET user=?, start=? WHERE name=?'
_QUERY_UNASSOCIATE = 'DELETE FROM Permissions Where user=? AND grp=?'


#
# CODE
#
class DataBase(object):
    """
    This is an entity that handles deals with the database by retrieving and
    storing data
    """

    def __init__(self):
        """
        Constructor

        @rtype: None
        @returns: nothing
        """
        # connect to database
        self.__conn = sqlite3.connect(_PATH_DB, check_same_thread = False)

        # create machines table if it does not exist yet
        self.__write(_QUERY_CREATE_MACHINES)
    # __init__()

    def __select(self, query, params = ()):
        """
        Executes the passed SELECT query and returns the resulting rows

        @type  query: basestring
        @param query: SELECT query to be executed

        @type  params: tuple
        @param params: parameters for the SELECT query

        @rtype: list
        @returns: query resulting rows
        """
        # get cursor to execute operations
        c = self.__conn.cursor()

        # execute the query
        result = c.execute(query, params)
        rows = result.fetchall()
        c.close()

        # return the results
        return rows
    # __select()

    def __write(self, query, params = ()):
        """
        Executes the passed SQL query and commits to DB at the end

        @type  query: basestring
        @param query: SQL query to be executed

        @type  params: tuple
        @param params: parameters for the SQL query

        @rtype: None
        @returns: nothing
        """
        # get cursor to execute operations
        c = self.__conn.cursor()

        # execute the query
        c.execute(query, params)
        c.close()

        # commit transaction
        self.__conn.commit()
    # __write()

    def add(self, name, ip, id, group):
        """
        Adds a machine with the passed name and other info

        @type  name: basestring
        @param name: machine name

        @type  ip: basestring
        @param ip: machine IP address

        @type  id: basestring
        @param id: machine ID in its controller (IVM, HMC, BladeCenter, ...)

        @type  group: basestring
        @param group: group the machine belongs to

        @rtype: None
        @returns: noting
        """
        # build params: machine name, ip, id and current time
        params = (name, ip, id, group, int(time.time()))

        # execute the update query
        self.__write(_QUERY_ADD, params)
    # add()

    def associate(self, user, group):
        """
        Associates the passed user to the passed group

        @type  user: basestring
        @param user: user name

        @type  group: basestring
        @param group: group name

        @rtype: None
        @returns: noting
        """
        self.__write(_QUERY_ASSOCIATE, (user, group))
    # associate()

    def getAvailable(self):
        """
        Returns the names of all currently reserved machines

        @rtype: list
        @returns: names of all currently reserved machines
        """
        # execute select query
        rows = self.__select(_QUERY_GET_AVAILABLE)

        # return names
        return [r[0] for r in rows]
    # getAvailable()

    def getByUser(self, user):
        """
        Returns the names of all machines that are currently reserved for the
        passed user

        @type  user: basestring
        @param user: passed user

        @rtype: list
        @returns: names of all machines currently reserved for the user
        """
        # execute select query
        rows = self.__select(_QUERY_GET_BY_USER, (user,))

        # return names
        return [r[0] for r in rows]
    # getByUser()

    def getInfo(self, name):
        """
        Returns info about the machine with the passed name

        @type  name: basestring
        @param name: machine name

        @rtype: dict
        @returns: info about the machine with the passed name
        """
        # execute select query
        rows = self.__select(_QUERY_GET_INFO, (name,))

        # no row returned: return empty info
        if len(rows) == 0:
            return {}

        # return info
        return {
            'name': rows[0][0],
            'ip': rows[0][1],
            'id': rows[0][2],
            'group': rows[0][3],
            'user': rows[0][4],
            'start': rows[0][5],
        }
    # getInfo()

    def getMachines(self):
        """
        Returns the names of all registered machines

        @rtype: list
        @returns: names of all registered machines
        """
        # execute select query
        rows = self.__select(_QUERY_GET_MACHINES)

        # return names
        return [r[0] for r in rows]
    # getMachines()

    def getReserved(self):
        """
        Returns the names of all currently reserved machines

        @rtype: list
        @returns: names of all currently reserved machines
        """
        # execute select query
        rows = self.__select(_QUERY_GET_RESERVED)

        # return names
        return [r[0] for r in rows]
    # getReserved()

    def getUsers(self):
        """
        Returns the users which currently have reserved machines

        @rtype: list
        @returns: users which currently have reserved machines
        """
        # execute select query
        rows = self.__select(_QUERY_GET_USERS)

        # return names
        return [r[0] for r in rows]
    # getUsers()

    def getUsersByGroup(self, group):
        """
        Returns the users which belong to be passed group

        @type  group: basestring
        @param group: group name

        @rtype: list
        @returns: users which belong to be passed group
        """
        # execute select query
        rows = self.__select(_QUERY_GET_USERS_BY_GROUP, (group,))

        # return users
        return [r[0] for r in rows]
    # getUsersByGroup()

    def remove(self, name):
        """
        Removes the machine with the passed name

        @type  name: basestring
        @param name: machine name

        @rtype: None
        @retruns: nothing
        """
        self.__write(_QUERY_REMOVE, (name,))
    # remove()

    def reserve(self, name, user):
        """
        Sets the machine with the passed name as reserved for the passed user.
        If user is passed as None, the effect is to set the machine as reserved
        for no one.

        @type  name: basestring
        @param name: machine name

        @type  user: basestring or None
        @param user: user the machine is to be reserved for

        @rtype: None
        @retruns: nothing
        """
        # build params: user, current time, machine name
        params = (user, int(time.time()), name)

        # execute the update query
        self.__write(_QUERY_RESERVE, params)
    # reserve()

    def unassociate(self, user, group):
        """
        Unassociates the passed user from the passed group

        @type  user: basestring
        @param user: user name

        @type  group: basestring
        @param group: group name

        @rtype: None
        @returns: noting
        """
        self.__write(_QUERY_UNASSOCIATE, (user, group))
    # unassociate()

# DataBase


