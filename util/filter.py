def filterGold(urlFin, urlFout, labelChosen):
  fin = open(urlFin, 'rt', encoding="utf8")
  fout = open(urlFout, 'w', encoding="utf8")

  count = 0
  temp = ""
  for line in fin:
    if (len(line) != 1):
      if (line.split(" ")[0] == "#"):
        temp += line
      else:
        fields = line.split("\t")
        if (fields[7] == labelChosen) or (labelChosen == "total"):
          temp += line
          count += 1
    else:
      fout.write(temp + "\n")
      temp = ""

  fin.close()
  fout.close()


def filterFile(urlFin, urlGoldFiltered, urlFout):
  fin = open(urlFin, 'rt', encoding="utf8")
  fout = open(urlFout, 'w', encoding="utf8")

  count = 0
  temp = ""
  sent_id = 1
  for line in fin:
    if (len(line) == 1):
      sent_id += 1
      fout.write("#\n#\n" + temp + "\n")
      temp = ""
      count += 1
    else:
      fields = line.split("\t")
      if (isExist("test-s" + str(sent_id), fields[0], urlGoldFiltered)):
        temp += line
      
  print(str(count))
  fin.close()
  fout.close()

def isExist(sent_id, word_id, urlChosen):
	fin2 = open(urlChosen, 'rt', encoding="utf8")
	sent_found = False
	for line in fin2:
		if (len(line) != 1):
			if (line.split(" = ")[0] == "# text") or (line.split(" = ")[0] == "# sent_id"):
				if (line.split(" = ")[0] == "# sent_id"):
					if not (sent_found) and line.split(" = ")[1].replace("\n","") == sent_id:
						sent_found = True
					elif int(sent_id.replace("test-s", "")) < int(line.split(" = ")[1].replace("test-s", "").replace("\n", "")) and (sent_found):
						fin2.close()
						return False
			else:
				fields = line.split("\t")
				if (int(fields[0]) > int(word_id)) and (sent_found):
					fin2.close()
					return False
				if (int(fields[0]) == int(word_id)) and (sent_found):
					fin2.close()
					return True
		else:
			if (sent_found):
				fin2.close()
				return False
	fin2.close()
	return False