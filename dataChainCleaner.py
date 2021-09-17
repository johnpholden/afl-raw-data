"""
This script parses 2021 AFL match chains and identifies which team 'owns' a specific chain.

This script produces no output, but rather idenitifes how to assign a specific chain to a team.

Each chain gets parsed as soon as a new chain is found, so the data must be ordered by chain for this to work properly.
However this is how the raw data is presented, so it works as long as you don't adjust that.

It saves each row in the chain to a list, when a new chain is found it parses the list and picks the team with the most instances in the chain.
This does not guarantee a correct result but worked well in testing.

written by John Holden
"""

import os
import csv

event = []	#if you're looking to parse specific events, include them in this list
chainTeam = ''

#load the data one csv at a time
for i in range(1,26):
	leadingZero = ''
	if i < 10:
		leadingZero = '0'
	fileName = 'match_chains_2021_' + leadingZero + str(i) + '.csv'

	with open(fileName, 'r') as csvfile:
		getLine = csv.reader(csvfile, delimiter=',')
		oldrow = None	#this stores the last parsed row into memory for comparison
		activeChain = []	#this stores a list of rows which gets parsed as soon as a new chain is identified
		ignoreRow = 0	#if an event is found, ignore the rest of the chain (not necessary)
		for row in getLine:
			if oldrow:
				if oldrow[12] != row[12]:
					home = activeChain.count(row[1])
					away = activeChain.count(row[2])
					chainTeam = 'NA'
					if home > away:
						chainTeam = row[1]
					elif away > home:
						chainTeam = row[2]
					activeChain = []
					ignoreRow = 0
				if oldrow[15] != row[15]:
					activeChain = []
					rowAppender = []
					ignoreRow = 0
			if row[20] in event:
				home = activeChain.count(row[1])
				away = activeChain.count(row[2])
				chainTeam = 'NA'
				if home > away:
					chainTeam = row[1]
				elif away > home:
					chainTeam = row[2]
				activeChain = []
				rowAppender = []
				ignoreRow = 1
				
			#append the active team to the chain to see whose chain it is
			if ignoreRow == 0:
				activeChain.append(row[19])
			oldrow = row
