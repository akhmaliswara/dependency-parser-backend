# Find all sentence that have false label in compared file, 
# and have true label in observed file
import sys
import functools

# urlGold = sys.argv[1]
# urlObserved = sys.argv[2]
# urlCompared = sys.argv[3]
# typeChecked = sys.argv[4]

def isIncludedLabel(labelChosen, currentCheckedLabel):
  if (labelChosen == ''):
    return True
  else:
    return (labelChosen == currentCheckedLabel)

def compare(urlGold, urlObserved, urlCompared, typeChecked, labelChosen=''):
  finGold = open(urlGold, 'rt', encoding="utf8")
  finObserved = open(urlObserved, 'rt', encoding="utf8")
  finCompared = open(urlCompared, 'rt', encoding="utf8")

  lineObserved = finObserved.readlines()
  lineCompared = finCompared.readlines()

  listIDSentAndWord = []
  idSentence = 1
  lineNumber = 1
  tempIDWord = []
  tempLabel = []

  for line in finGold:
    # print(f'lineNumber : {lineNumber}')	
    if (len(line) != 1):
      if (line[0] != '#'):
        fields = line.split("\t")
        fieldsObserved = lineObserved[lineNumber - 1].split("\t")
        # print(fieldsObserved)
        # print(lineNumber)
        fieldsCompared = lineCompared[lineNumber - 1].split("\t")
        if (isIncludedLabel(labelChosen, fields[7])):
          if (fields[7] == fieldsObserved[7]) and (typeChecked != 'head'):
            if (fieldsObserved[7] != fieldsCompared[7]):
              tempIDWord.append((fields[0], fields[1]))
              tempLabel.append(fieldsCompared[7])
          elif (fields[6] == fieldsObserved[6]) and (typeChecked == 'head'):
            if (fieldsObserved[6] != fieldsCompared[6]):
              tempIDWord.append((fields[0], fields[1]))
      elif (lineObserved[lineNumber - 1][0] != '#'):
        lineNumber -= 1
    else:
      if (tempIDWord != []):
        listIDSentAndWord.append([idSentence, tempIDWord, tempLabel])
        tempIDWord = []
        tempLabel = []
      idSentence += 1
    lineNumber += 1

  for elmt in listIDSentAndWord:
    print(elmt)
    
  print(f'total ID Sentence: {len(listIDSentAndWord)}')
  result = list(map(lambda x: len(x[1]), listIDSentAndWord))
  if (len(listIDSentAndWord) != 0):
    resultfix = functools.reduce(lambda a, b: a+b, result)
  else:
    resultfix = 0
  print(f'total Word: {resultfix}')
  return {'list': listIDSentAndWord, 'totalID': len(listIDSentAndWord), 'totalWord': resultfix}