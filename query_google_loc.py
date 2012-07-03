#!/usr/bin/python
"""
Copyright (C) 2010 Kees Cook <kees@outflux.net>
License: GPLv3
Find location of a MAC address via Google Location Services
http://code.google.com/p/gears/wiki/GeolocationAPI

Note: Google also uses your IP address to determine location, and if your IP
doesn't match up to where the MAC addresses are, they may return a location
of your city.

"""

import urllib2
from sys import argv
import json


def request_loc(bssid):
	loc_req = {
		'version': '1.1.0',
		'request_address': True,
		'address_language': 'en',
		'wifi_towers': []
	}
	
	for b in bssid:
		loc_req['wifi_towers'].append({
			'mac_address': b.replace(':', '-'),
			'signal_strength': 1
		})

	data = json.dumps(loc_req)
	return urllib2.urlopen('https://www.google.com/loc/json', data).read()


def print_loc(*bssid):
	loc_json = json.loads(request_loc(bssid))
	print bssid,
	try:
		print ("%(city)s, %(country)s" % loc_json['location']['address']),
		print "(%sm)" % loc_json['location']['accuracy']
	except KeyError, e:
		pass

	print loc_json['location']

	if loc_json['location']['accuracy'] >= 15000:
		print "# Accuracy of 15km or higher seems to indicate unknown location..."

	print ""

	
def main():
	if len(argv) == 1:
		# test mode
		nets = ['00:88:88:88:00:2A', '00:88:88:88:00:2B']
	elif argv[1].lower() == '--triangulate':
		# display data using all of the mac addresses at once.
		print "Using triangulate mode."
		print_loc(*argv[2:])
		return
	else:
		nets = argv[1:]

	for line in nets:
		print_loc(line)


if __name__ == "__main__":
	main()
