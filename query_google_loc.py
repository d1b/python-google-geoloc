#!/usr/bin/python
# Copyright (C) 2010 Kees Cook <kees@outflux.net>
# License: GPLv3
# Find location of a MAC address via Google Location Services
# http://code.google.com/p/gears/wiki/GeolocationAPI
import urllib2
import simplejson

def request_loc(bssid):
	loc_req = { 'version': '1.1.0', 'request_address': True,\
	'address_language': 'en','wifi_towers': [] }

	loc_req['wifi_towers'] += [{ 'mac_address': bssid.replace(':','-'), \
		'signal_strength': 1 } ]
	data = simplejson.JSONEncoder().encode(loc_req)
	return urllib2.urlopen('https://www.google.com/loc/json', data).read()

def print_loc(bssid):
	loc_json = simplejson.loads(request_loc(bssid))
	print bssid,
	try:
		print loc_json['location']['address']['city'], loc_json['location']['address']['country']
	except KeyError, e:
		print loc_json['location']
	if loc_json['location']['accuracy'] >= 22000:
		print "# N.B. Accuracy of 22000 or higher seems to indicate unknown location..."

if __name__=="__main__":
	for line in """00:88:88:88:00:2A 00:88:88:88:00:2B""".split(" "):
		print_loc(line)
