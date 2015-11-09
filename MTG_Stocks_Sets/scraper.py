import os
import sys
import math
import string
import re

# return the string between the 'first' and 'last' substrings specified in the args
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# open write file
wfile = open('id_price.dat', 'w')

list_dir = os.listdir(os.getcwd())
for ele in list_dir:
	# open only files that correspond to the price data
	if ( ele[-4:] == ".htm" ):
		fname = ele

		with open(fname) as f:

			# ignore all the lines before the price table begins.
			# this is a consequence of ads at the top of the page that would have 'multiverseid' substring in their line
			for line in f:
				if (line.rstrip() == "<table class='table table-striped table-condensed' style='width: 100%;'>"):
					break

			for line in f:

				line.rstrip().find("multiverseid")
				if ( line.rstrip().find("multiverseid") != -1):
					card = line.rstrip()
					multiverseid = find_between(card,"multiverseid=","\" ")
					price = find_between(card, ">$", "</td></tr>")

					wfile.write(multiverseid + "\t" + price + "\n")

wfile.close()