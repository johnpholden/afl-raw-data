"""
This script generates a point cloud in tab separated format, with the x/y values delimited in the same column by a pipe.
I manually replace this pipe with a tab before importing into visualisation software.

This loads the data line by line into the software, parses each chain, and assigns an owner to each chain. Once an attempt at goal is made, 

(C) 2021 by John Holden
"""

import os
import csv

#dataTypes = ['Ground Kick','Kick','Mark on Lead','Handball','Hard Ball Get','Uncontested Mark','Contested Mark','Spoil']
#dataTypes = ['Ground Kick', 'Kick', 'Handball', 'Loose Ball Get Crumb', 'Loose Ball Get','Hard Ball Get','Gather']
dataTypes = ['Kick', 'Handball', 'Ground Kick']

#these dictionaries hold our point clouds, ctr is a counter and score is the sum of the score
xyCtr = {}
xyScore = {}

#define the output file
input_file = "match_expscore_3"

csvfile2 = open(input_file + '_output.csv', 'w')
output = csv.writer(csvfile2, delimiter='\t')

#load the data one csv at a time
for i in range(1,27):
	leadingZero = ''
	if i < 10:
		leadingZero = '0'
	fileName = 'match_chains_2021_' + leadingZero + str(i) + '.csv'

	with open(fileName, 'r') as csvfile:
		getLine = csv.reader(csvfile, delimiter=',')
		oldrow = None	#this stores the last parsed row into memory for comparison
		activeChain = []	#this stores a list of rows which gets parsed as soon as a new chain is identified
		activeChainId = -1 #the number of the currently active chain
		rowAppender = []	#this stores all events since the last goal/behind/shot on goal
		ignoreRow = 0	#if a scoring event is found, ignore the rest of the chain
		for row in getLine:
			#create an additional column to track who wins the chain
			row.append('NA')
			if oldrow:
				#the 12th column represents the chain number, if they're different log the chain
				if oldrow[12] != row[12]:
					#the team names in column 19 should match the home team name or away team name
					#whichever team is more common in the chain gets assigned the chain
					#THIS IS NOT GUARANTEED TO WORK but had a 100% success rate in manually checked data, so am comfortable with this
					home = activeChain.count(row[2])
					away = activeChain.count(row[3])
					chainTeam = 'NA'
					if home > away:
						chainTeam = row[2]
					elif away > home:
						chainTeam = row[3]
					for r in rowAppender:
						if activeChainId == r[12]:
							r[26] = chainTeam
					activeChain = []
					activeChainId = -1
					ignoreRow = 0
				if oldrow[15] != row[15]:
					#reset after each quarter ends without doing anything else
					activeChain = []
					activeChainId = -1
					rowAppender = []
					ignoreRow = 0
			if row[20] in ['Goal','Behind','Shot At Goal']:
				#figure out which team owns the current chain - this should probably be functionalised
				home = activeChain.count(row[2])
				away = activeChain.count(row[3])
				chainTeam = 'NA'
				if home > away:
					chainTeam = row[2]
				elif away > home:
					chainTeam = row[3]
				
				#inefficient loop but it's fine for our purposes
				for r in rowAppender:
					if activeChainId == r[12]:
						r[26] = chainTeam

				expScore = 0
				if row[20] == 'Goal':
					expScore = 6
				elif row[20] == 'Behind':
					expScore = 1
					
				for r in rowAppender:
					exprScore = 0	#variable to translate the expected score to the team in possession
					#get the point on the pitch - assigning these to int variables makes it easier to parse
					xy = ''
					xval = int(r[24])
					yval = int(r[25])
					#if the assigned chain equals the team
					if r[24] != '' and r[25] != '':
						if r[26] == r[19]:
							#we reproject the x-y coords to flip across the y axis since they are flipped in the data set
							xy = str(xval)+'|'+str(yval*-1)
						#if the assigned team to the chain does not equal NA
						elif r[26] != 'NA':
							#we reproject the x-y coords to flip across the x axis
							xy = str(xval*-1)+'|'+str(yval)
						
					#if the scoring team equals the team with the ball in the chain, then give them full points
					if r[19] == row[19]:
						exprScore = expScore
					else:
						exprScore = expScore * -1
					
					if xy in xyCtr and xy != '':
						xyCtr[xy] = xyCtr[xy] + 1
						xyScore[xy] = xyScore[xy] + exprScore
					elif xy != '':
						#initialise the variables if they don't exist
						xyCtr[xy] = 1
						xyScore[xy] = exprScore
				
				#clear all the data
				activeChain = []
				activeChainId = -1
				rowAppender = []
				#don't add this row, or any rows that follow in the chain number, to the event list for the previous chains
				ignoreRow = 1
				
			#append the active team to the chain to see whose chain it is
			if ignoreRow == 0:
				activeChain.append(row[19])
				activeChainId = row[12]
				if row[20] in dataTypes:
					#add the current row to the list of rows we'll end up processing
					rowAppender.append(row)
			#save the older row so we can do delta(change) analysis on it
			oldrow = row
			
for key in xyCtr:
	outputRow = []
	outputRow.append(key)
	outputRow.append(xyCtr[key])
	outputRow.append(xyScore[key])
	output.writerow(outputRow)
