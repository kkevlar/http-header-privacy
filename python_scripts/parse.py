#!/bin/usr/python3

import sys
from StringToken import stringToken

def parse():
	infile = open(sys.argv[1], "r")
	fileText = stringToken(infile.read(), "\n")
	infile.close()

	for i in range(0, len(fileText)):
		fileText[i] = stringToken(fileText[i], "[]")

	i = 0
	length = len(fileText)
	while i < length:
		if fileText[i][0] != "bazz":
			fileText.pop(i)
		else:
			i += 1

	for i in range(0, len(fileText)):
		fileText[i].pop(0)

	return fileText


	# outfile = open(sys.argv[2], "w")
	# writestr = ""

	# outfile.write(writestr)
	# outfile.close()

parse()
