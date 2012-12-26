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
from machinemanager import MachineManager
from supybot.commands import *

import readwiki
import supybot.callbacks as callbacks
import supybot.ircutils as ircutils
import supybot.plugins as plugins
import supybot.utils as utils
import time


#
# CODE
#
class Mussum(callbacks.Plugin):
    """
    Add the help for "@plugin help Mussum" here
    This should describe *how* to use this plugin.
    """
    threaded = True

    def __init__(self, irc):
        """
        Constructor
        """
        # call base constructor
        callbacks.Plugin.__init__(self, irc)

        # initialize internal state
        self.__manager = MachineManager()
    # __init__()

    def __formatList(self, entries):
        """
        Formats the passed list of entries and returns it as a string

        @type  entries: list
        @param entries: list to be formatted

        @rtype: basestring
        @returns: formatted string
        """
        # no entries: return 'no machines'
        if len(entries) == 0:
            return 'no machines'

        # one entry: return it
        if len(entries) == 1:
            return entries[0]

        # N entries: return 'A, B, ..., M and N'
        return '%s and %s' % (', '.join(entries[:-1]), entries[-1])
    # __formatList()

    def __formatTime(self, interval):
        """
        Formats the passed time interval as a string representing it rounded
        in seconds, minutes, hours or days.

        @type  interval: int
        @param interval: time interval in seconds

        @rtype: basestring
        @returns: formatted string
        """
        # less than minute: return as seconds
        if interval < 60:
            return '%ss' % interval

        # less than hour: return as minutes
        if interval < 3600:
            return '%sm' % (interval / 60)

        # less than day: return as hours
        if interval < 86400:
            return '%sh' % (interval / 3600)

        # at least one day: return as days
        return '%sd' % (interval / 86400)
    # __formatTime()

    def add(self, irc, msg, args):
        """
        Adds the machines whose names are passed as args
        """
        # no arg passed: show how to use
        if len(args) == 0:
            irc.reply('Usage: add <machine 1> [... <machine N>]',
                      prefixNick=True)
            return

        # add machines
        for arg in args:

            # error adding machine: report it
            if self.__manager.add(arg) != 0:
                irc.reply('Machine %s already exists' % arg, prefixNick=False)
                continue

            # success: report it
            irc.reply('Machine %s added' % arg, prefixNick=False)
    # add()

    def cerveja(self, irc, msg, args):
        """
        Checks to see if the bot is alive.
        """
        irc.reply('Suco de cevadis!', prefixNick=True)
    # cerveja()

    def free(self, irc, msg, args):
        """
        Releases the machine whose name is passed as argument
        """
        # no arg passed: show how to use
        if len(args) == 0:
            irc.reply('Usage: free <machine 1> [... <machine N>]',
                      prefixNick=True)
            return

        # free machines
        for machine in args:

            # machine released: done
            status = self.__manager.release(machine)

            if status == 0:
                irc.reply('Machine %s has been released' % machine,
                          prefixNick=False)
                continue

            # machine does not exist: error
            if status == 1:
                irc.reply('Machine %s does not exist' % machine,
                          prefixNick=True)
                continue
    # free()

    def info(self, irc, msg, args):
        """
        Shows info for the machine whose name is passed as argument
        """
        # no arg passed: show how to use
        if len(args) == 0:
            irc.reply('Usage: info <machine 1> [... <machine N>]',
                      prefixNick=True)
            return

        # tell the user to see the info in pvt
        irc.reply('pvt', prefixNick=True)

        # show machines
        for machine in args:

            # machine does not exist: no info
            info = self.__manager.getInfo(machine)

            if info == None:
                irc.reply('Machine %s does not exist' % machine,
                          prefixNick=True)
                continue

            # get how long machine is in the current state
            interval = self.__formatTime(int(time.time()) - info['start'])

            # send info
            irc.reply('# Name   : %s' % info['name'], private=True)
            irc.reply('# Ip     : %s' % info['ip'], private=True)
            irc.reply('# Id     : %s' % info['id'], private=True)
            irc.reply('# Group  : %s' % info['group'], private=True)

            # machine is available: report it
            if info['user'] == None:
                irc.reply('# Status : available (%s)' % interval, private=True)
                continue

            # machine is reserved: also show for whom
            irc.reply('# Status : reserved (%s)' % interval, private=True)
            irc.reply('# User   : %s' % info['user'], private=True)
    # info()

    def reserve(self, irc, msg, args):
        """
        Reserves the machine whose name is passed as argument
        """
        # no arg passed: show how to use
        if len(args) == 0:
            irc.reply('Usage: reserve <machine 1> [... <machine N>]',
                      prefixNick=True)
            return

        # get machine and reserver name
        for machine in args:
            user = msg.nick

            # machine reserved: done
            status = self.__manager.reserve(machine, user)

            if status == 0:
                irc.reply('Machine %s has been reserved for %s' % (machine,
                          user), prefixNick=False)
                continue

            # machine does not exist: error
            if status == 1:
                irc.reply('Machine %s does not exist' % machine,
                          prefixNick=True)
                continue

            # machine already reserved: error
            if status == 2:
                irc.reply('Machine %s is already reserved' % machine,
                          prefixNick=True)
                continue

            # user has no permissions: error
            if status == 3:
                irc.reply('User %s has no permissions to reserve machine %s' %
                          (user, machine), prefixNick=True)
                continue
    # reserve()

    def show(self, irc, msg, args):
        """
        List the machines depending on the passed argument: all, reserved, free
        """
        # no arg passed: show how to use
        if len(args) == 0:
            irc.reply('Usage: show (all | reserved | free)', prefixNick=True)
            return

        # all: list all machines
        arg = args[0]

        if arg == 'all':
            machines = self.__formatList(self.__manager.listMachines())
            irc.reply('Registered machines: %s' % machines, prefixNick=True)
            return

        # reserved: list only reserved machines
        if arg == 'reserved':
            machines = self.__formatList(self.__manager.listReserved())
            irc.reply('Reserved machines: %s' % machines, prefixNick=True)
            return

        # free: list only available machines
        if arg == 'free':
            machines = self.__formatList(self.__manager.listAvailable())
            irc.reply('Available machines: %s' % machines, prefixNick=True)
            return

        # invalid arg: show how to use
        irc.reply('Usage: show (all | reserved | free)', prefixNick=True)
    # show()

    def update(self, irc, msg, args):
        """
        List the machines reserved by user
        """
        # tell the use machines are being retrieved from wiki
        irc.reply('Retrieving machines table from wiki', prefixNick=False)
        
        # retrieve machines from wiki
        for machine in readwiki.parseMachinesTable():
        
            # machine without name: ignore
            name = machine.get('name', None)
            
            if name == None:
                continue

            # get machine info
            ip = machine.get('ip', None)
            id = machine.get('id', None)
            group = machine.get('group', None)
        
            # error adding machine: report it
            if self.__manager.add(name, ip, id, group) != 0:
                irc.reply('Machine %s already exists' % name, prefixNick=False)
                continue

            # success: report it
            irc.reply('Machine %s added' % name, prefixNick=False)
    # update()

    def users(self, irc, msg, args):
        """
        List the machines reserved by user
        """
        output = []

        for user in self.__manager.listUsers():
            machines = self.__formatList(self.__manager.listByUser(user))
            output.append('%s - %s' % (user, machines))

        irc.reply('Machines by user: %s' % ' * '.join(output), prefixNick=False)
    # users()

Class = Mussum


