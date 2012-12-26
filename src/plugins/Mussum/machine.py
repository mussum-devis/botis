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


#
# CODE
#
class Machine(object):
    """
    This represents a machine. A machine has info to describe it and may be
    reserved or free to be used.
    """
    
    def __init__(self, name, ip, id):
        """
        Constructor
        
        @type  name: basestring
        @param name: machine name
        
        @type  ip: basestring
        @param ip: machine IP address
        
        @type  id: basestring
        @param id: machine ID in its controller (IVM, HMC, BladeCenter, ...)
        
        @rtype: None
        @returns: nothing
        """
        # machine description
        self.__name = name
        self.__ip = ip
        self.__id = id
        
        # usage state
        self.__reserved = False
        self.__user = None
    # __init__()

    def isReserved(self):
        """
        Returns True if the machine is reserved, False otherwise
        
        @rtype: bool
        @retruns: True if the machine is reserved, False otherwise
        """
        return self.__reserved
    # isReserved()
    
    def release(self):
        """
        Sets this machine as available for use
        
        @rtype: None
        @retruns: nothing
        """
        self.__reserved == False
    # release()

    def reserve(self, user):
        """
        Sets this machine as reserved for the passed user
        
        @type  user: basestring
        @param user: user the machine is to be reserved for
        
        @rtype: bool
        @retruns: True on success, False otherwise
        """
        # machine is already reserved: error
        if self.__reserved == True:
            return False
        
        # reserve machine
        self.__reserved = True
        self.__user = user
        
        # success
        return True
    # reserve()

# Machine


