#!/usr/bin/python3

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
		if fileText[i][0] != "bazz ":
			fileText.pop(i)
			length -= 1
		else:
			i += 1

	for i in range(0, len(fileText)):
		fileText[i].pop(0)

	for i in range(0, len(fileText)):
		j = 0
		length = len(fileText[i])
		while j < length:
			if fileText[i][j] == ' ':
				fileText[i].pop(j)
				length -= 1
			else:
				j += 1

	return fileText

def generate_csv(fileText):
	outfile = open(sys.argv[2], "w")
	writestr = ""

	for i in range(0, len(fileText)):
		for j in range(0, len(fileText[i]) - 1):
			writestr += fileText[i][j] + "~"
		writestr += fileText[i][len(fileText[i]) - 1] + "\n"

	outfile.write(writestr)
	outfile.close()

generate_csv(parse())
