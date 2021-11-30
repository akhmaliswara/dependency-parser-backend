def getSentenceWithID(id, urlInput):
	fin = open(urlInput, 'rt', encoding="utf-8")
	print(id)
	idSentence = 1
	result = ""

	for line in fin:
		if (len(line) != 1):
			if (idSentence == id):
				result += line
		else:
			if (idSentence == id):
				if (result[0] != '#'):
					result = "#\n#\n" + result
				return result
			idSentence += 1

	fin.close()


def getAllSentence(urlInput):
	fin = open(urlInput, 'rt', encoding="utf-8")

	result = []
	temp = ""
	countWord = 0
	countSentence = 0

	for line in fin:
		if (len(line) != 1):
			temp += line
			fields = line.split("\t")
			if (line[0] != '#') and (fields[3] != "_"):
				countWord += 1
		else:
			if (temp[0] != '#'):
				temp = "#\n#\n" + temp
			result.append(temp)
			temp = ""
			countSentence += 1 

	fin.close()
	print("count Word: " + str(countWord))
	print("count Sentence: " + str(countSentence))
	return result