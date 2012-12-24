# Written by Brian Baskin - cmdLabs (Newberry Group)
# Version 1.0 - April 2011
# Usage: ip2cc [-i <ip>] [-f <file] [-c] [-t] [-v]
# Converts an IP address to a country code
# Input via stdin, -i, or -f
# Output to stdout as raw, -c CSV, or -t TSV
# -v provides verbose details

import sys
import os
import pygeoip
import argparse 

TSVout = False
CSVout = False
fileread = True
usestdin = False
inputfile = ''

geo = pygeoip.GeoIP('GeoIP.dat')


if not sys.stdin.isatty():
        usestdin = True
        fileread = False

parser = argparse.ArgumentParser(description='cmdLabs IP2CC v0.1')
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-i', action="store", dest="ip", help="Specifies individual IP", default=[])
parser.add_argument('-f', action="store", dest="infile", help="Specifies input file", default=[])
parser.add_argument('-c', action="store_true", help="Enable CSV output", default=False)
parser.add_argument('-t', action="store_true", help="Enable TSV output", default=False)
parser.add_argument('-v', action="store_true", dest="verbose", help="Enable verbose output", default=False)
results = parser.parse_args()


if results.c:
        CSVout = True
        if results.verbose:
                print ": Enabling CSV output"
if results.t:
        TSVout = True
        if results.verbose:
                print ": Enabling TSV output"

if not usestdin and len(results.ip) > 0:
        fileread = False
        ip_list = [results.ip]
        
if not usestdin and fileread and len(results.infile) > 0:
        if os.path.exists(results.infile):
                if results.verbose:
                        print ": Reading data from \"%s\"" % results.infile
                inputfile = results.infile
        else:
                print "::: File \"%s\" not found" % results.infile
                quit()
        

if fileread:
        try:
  	FILE = open(inputfile, "r")
        	ip_list = FILE.readlines()
        	FILE.close()
	except: 
		print "File not found or could not be opened."
		quit()
elif usestdin:
        ip_list = sys.stdin.readlines()
else:
        ip_list = [results.ip]



for ip_raw in ip_list:
        ip = ip_raw.strip("\r\n")
        ip = ip.strip()
        country = geo.country_code_by_addr(ip)

        if country == "":
                country = "Internal"

        if CSVout:
        	stringout = "%s,%s" % (ip, country)
        elif TSVout:
		stringout = "%s\t%s" % (ip, country)
	else:
                stringout = (country)

        print(stringout)
