def evaluate(urlGold, urlSystem, filterLabel):
  finGold = open(urlGold, 'rt', encoding="utf8")
  finSystem = open(urlSystem, 'rt', encoding="utf8")

  isExistComment = False
  total = 0
  correctHeadOnly = 0
  correctHeadLabel = 0
  correctLabelOnly = 0

  idSentence = 0
  idWord = 1
  idSentWordMiss = []  
  arrLabelFalse = {}

  i = 0
  arrLineGold = []
  print(filterLabel)

  for line in finGold:
    arrLineGold.append(line.replace("\n",""))
    if (len(line) != 1):
      if (line.split(" = ")[0] != "# text") and (line.split(" = ")[0] != "# sent_id"):
        label = line.split("\t")[7]
        if ((filterLabel == "") or (label == filterLabel)):
          total += 1 

  for line in finSystem:
    if (len(line) != 1):
      if (line[0] != "#") and (line != "\n")and ( line != " \n"):
        fieldsSystem = line.replace("\n","").split("\t")
        if (fieldsSystem[0] == '1'):
          if (not isExistComment):
            i += 2
          idSentence += 1
          idWord = 1
        fieldsGold = arrLineGold[i].split("\t")
        if ((filterLabel == "") or (fieldsGold[7] == filterLabel)):
          if (fieldsSystem[6] == fieldsGold[6]):
            correctHeadOnly += 1
            if (fieldsSystem[7] == fieldsGold[7]):
              correctHeadLabel += 1
          if (fieldsSystem[7] == fieldsGold[7]):
            correctLabelOnly += 1
          else:
            if (fieldsSystem[7] not in arrLabelFalse):
              arrLabelFalse[fieldsSystem[7]] = 1
            else:
              arrLabelFalse[fieldsSystem[7]] += 1
            idSentWordMiss.append([idSentence, idWord, fieldsSystem[1]])
      elif (line[0] == '#'):
        isExistComment = True
    i += 1
    idWord += 1

  sort_arr = sorted(arrLabelFalse.items(), key=lambda x: x[1], reverse=True)
  arrMissLabel = list(map(lambda x: (x[0], x[1], x[1]*100.0/total), sort_arr))
  uas = (correctHeadOnly*100.0/total)
  las = (correctHeadLabel*100.0/total)
  la = (correctLabelOnly*100.0/total)
  result = {'UAS': uas, 'LAS': las, 'LA': la, 'missLabel': arrMissLabel, 'idMissList' : idSentWordMiss}
  return result