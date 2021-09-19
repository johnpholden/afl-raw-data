# afl-raw-data
This repository stores raw data generated from the raw 2021 AFL data.

dataChainCleaner.py - sample code for assigning chains

dataExpectedScoreOnPitchv2.py - code which cleans each CSV file, assigns an expected score to each point on the pitch, and outputs a point cloud in text format.

playerPointsAddedVsExpected.csv - How many points a player added (or subtracted) based on the average expected points at the location of their scoring shots. Includes shots at goal worth zero points, and is adjusted based on whether the shot was a set shot or was a kick from play.
