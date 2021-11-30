import stanza
import os

STANZA_PARSER_URL = 'parser/stanza/parser.py'
SPACY_PARSER_MODEL_URL = 'parser/spacy/model/model-spacy-best-ud' 

def sentenceToDep(sentence):
	# Format sentence: conllu sentence (without comment)
	json = {"words" : [], "arcs" : []}
	sentence = sentence.split("\n")
	for line in sentence:
		label = line.split("\t")
		if (len(label) > 1):
			words_append = {
				"text": label[1], 
				"tag": label[4]
			}
			json["words"].append(words_append)
			if (label[6] != "0") and (label[6] != "_") and (label[7] != "ROOT"):
				arcs_append = {
					"start": (int(label[0]) - 1) if (int(label[0]) < int(label[6])) else (int(label[6]) - 1), 
					"end": (int(label[6]) - 1) if (int(label[0]) < int(label[6])) else (int(label[0]) - 1), 
					"label": label[7],
					"dir": "right" if (int(label[0]) > int(label[6])) else "left"
				}
				json["arcs"].append(arcs_append)
	return json

def saveSentenceInConllu(sentence, urlSave):
	# download models if not installed
	# stanza.download('id')
	nlp = stanza.Pipeline(lang='id', processors='tokenize,mwt,pos')
	doc = nlp(sentence)
	result = ''
	for sent in doc.sentences:
		for word in sent.words:
			result += f'{word.id}\t{word.text}\t{word.lemma}\t{word.upos}\t{word.xpos}\t_\t_\t_\t_\t_\n'

	fout = open(urlSave, 'w', encoding="utf-8")
	fout.write(result)
	
def parse(urlInput, parser):
	urlOutput = urlInput + '_parsed.conllu'
	if (parser == 'stanza'):
		os.system('python ' + STANZA_PARSER_URL + ' --data_dir ' + STANZA_PARSER_URL + '/model' + ' --eval_file ./' + urlInput + ' --output_file ' + urlOutput + ' --mode predict --lang id --no_pretrain --save_name default_setting --save_dir parser/stanza/model')
	elif (parser == 'spacy'):
		urlInputJSON = 'static/spacy_result'
		os.system('python -m spacy convert ' + urlInput + ' ' + urlInputJSON)
		os.system('python -m spacy evaluate ' + SPACY_PARSER_MODEL_URL + " " + urlInputJSON)