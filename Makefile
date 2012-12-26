# -
# This will generate HTML and PDF versions of the IBMIT User's Manual from the
# docbook sources
#
# Usage:
#
#   make [target] [variables]
#
# Targets:
#
#   all           Build the preload RPM package
#
# Variables:
#
#   RPMBUILD_DIR     Directory used by rpmbuild to work.
#
# Author: Rodrigo Dias Cruz <rdc@br.ibm.com>
# Copyright (C) 2011 IBM Corp.
# -

#
# VARIABLES
#
RPMBUILD_DIR = /usr/src/packages/SOURCES


#
# RULES
#
all:
	cp -a src /var/tmp/supybot-mussum-1.0
	tar -C /var/tmp/ -czf $(RPMBUILD_DIR)/supybot-mussum-1.0.tar.gz supybot-mussum-1.0/
	rm -rf /var/tmp/supybot-mussum-1.0/
	rpmbuild -bb supybot-mussum.spec
