#!/usr/bin/python
# -*- coding: utf8 -*-

import urllib2

class TLDExtractor(object):
	# Based on:
	# Hugh Bothwell @ http://stackoverflow.com/questions/4916890/extract-2nd-level-domain-from-domain-python
	
	MASTER_URL = "http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/effective_tld_names.dat?raw=1"
	TLDS       = None

	@classmethod
	def loadDB(self, filename = None):
		if filename is None:
			F = urllib2.urlopen(TLDExtractor.MASTER_URL)
		else:
			F = open(filename)
		
		lines = []
		
		for line in F:
			line = line.strip()
			
			if line[:2] is '//' :
				# comment
				continue
				
			if not len(line) :
				# empty line
				continue
				
			lines.append(line)
			
		TLDExtractor.TLDS = set(lines)

	def __init__(self, filename = None):
		if TLDExtractor.TLDS is None:
			TLDExtractor.loadDB(filename)

	def getTLD(self, url):
		url    = url.lower().strip()
		chunks = url.split('.')

		# Look for exceptional match, e.g. !parliament.uk
	
		for start in range(len(chunks)):
			test = '.' . join(chunks[start:])
			excltest =  "!" + test

			if excltest in TLDExtractor.TLDS:
				# for !parliament.uk we must return just "uk"
				return '.' . join(chunks[start + 1:])

		# Look for "normal" domain.

		best_match = None

		for start in range(len(chunks)-1, -1, -1):
			test = '.' . join(chunks[start:])

			startest = "." . join( ['*'] + chunks[start + 1 : ] )
			
			#print start, test, startest, excltest

			if test in TLDExtractor.TLDS or startest in TLDExtractor.TLDS:
				best_match = test

		return best_match

	def getDomains(self, url):
		urls = url.split('.')
		
		tld = self.getTLD(url)

		if tld is None:
			return None
			
		tld = tld.split('.')
			
		domain = ".".join( urls[- len(tld) - 1 : ] )
		tld2   = ".".join( tld )
		tld    =           urls[-1]
		
		return (domain, tld2, tld)

	def getDomain(self, url):
		x = self.getDomains(url)
		
		if x is None:
			return None
			
		return x[0]



if __name__ == '__main__':
	tldx = TLDExtractor("tld.dat")

	urls = [
		"www.niki.miki.bg"	,
		"www.niki.1.bg"		,
		"www.niki.co.jp"	,
		"www.niki.co.kr"	,
		"www.niki.com.pr"	,
		"www.niki.us"		,
		"www.niki.ny.us"	,
		"www.президент.рф"	,
		"www.niki.co.uk"	,
		"www.parliament.uk"	,
		"musedoma.museum"	,
		"niki.museum"		,
		"www.niki.national.museum"	,

		"www.niki.uk"		,
		"www.niki.pr"		,
		"www.niki.AT"		,
		"www.nonexistent.hello"	,
		""			,
		"com"			,
		"uk"
	]

	for url in urls:
		dom = tldx.getDomains(url)
		
		if dom:
			print "%-30s : %-20s" % ( url, dom[0] )
		else:
			print "%-30s : ***ERROR***" % ( url, )


