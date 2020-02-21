# 03/23/18
# Justin Privitera
# StringToken
# v1.3
#
# Version History:
# 03/22/18 v1.0 - completed basic functionality
# 03/22/18 v1.1 - fixed bug where if input line was one character then nothing would display
# 03/22/18 v1.2 - fixed bug where if the last word was a single character it would not be added,
#                 fixed bug where single character inputs were not filtered
#                 fixed bug where final words were not showing up
# 03/23/18 v1.3 - added modes to the function to add greater functionality, read about them below.
#
# I was disappointed with the poor functionality of the python split function, 
# so I decided to make my own, more similar to the strtok() function in C.
#
# It takes an input String and a String of characters to split with,
# then returns a list of each word, as defined by input.
#
# mode 's' is standard, so it removes the tokens and returns a list of words separated by them
# mode 'f' is full, so it simply separates around the tokens but does not remove them from the output list
#
# At the end of the file are two simple tests with input and output

def stringToken(line, spliterator, mode = 's'): # mode 's' = standard, mode 'f' = full

	splitTokens = list(spliterator)
	wordList = []

	j = 0
	for i in range(0, len(line)):
		if line[i] in splitTokens:
			wordList.append(line[j : i]) # adds words to the list
			j = i + 1
			if mode == 'f':
				wordList.append(line[i])
		if i == len(line) - 1:
			wordList.append(line[j : i + 1]) # adds the final word to the list
	
	i = 0
	length = len(wordList)
	while i < length:
		if '' == wordList[i]:
			del wordList[i] # removes null strings from the list
			i -= 1
			length -= 1
		i += 1

	return wordList

# A simple i/o test to demonstrate functionality
#
# print("Enter a line: ")
# line = input()
# print("Enter a sequence of tokens: ")
# tokens = input()

# words = stringToken(line, tokens)
# print("Standard mode: " + str(words))

# words = stringToken(line, tokens, 'f')
# print("Full mode: " + str(words))

# A simple test incorporating the newline and tab characters

# print("Entered following string:")
# line = "\t1, 2, 3\n4, \t5, 6"
# print(line)
# print("Entered following tokens:")
# tokens = " ,\n\t"
# print(",'newline'")

# words = stringToken(line, tokens, 's')
# print("Standard mode: " + str(words))

# words = stringToken(line, tokens, 'f')
# print("Full mode: " + str(words))