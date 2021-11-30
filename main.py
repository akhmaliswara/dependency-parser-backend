import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import util

UPLOAD_FOLDER = 'static'
UPLOAD_GOLD = 'static/gold'
ALLOWED_EXTENSIONS = {'txt', 'conll', 'conllu', 'conllx'}
app = Flask(__name__)

def allowedFile(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods = ['GET'])
def test():
  data = request.form
  print(data)
  return jsonify(data='Hello World!')


@app.route("/visualize", methods = ['POST'])
def visualize():
  inputFile = request.files['input_file']
  if inputFile and allowedFile(inputFile.filename):
    filename = secure_filename(inputFile.filename)
    urlname = os.path.join(UPLOAD_FOLDER, filename)
    inputFile.save(urlname)
    
    try:
      request.form['id']
    except:
      sentences = util.getAllSentence(urlname)
      parsedSentences = []
      for sent in sentences:
        parsedSentences.append(util.sentenceToDep(sent))
    else:
      sentence = util.getSentenceWithID(int(request.form['id']), urlname)
      parsedSentences = util.sentenceToDep(sentence)
  return jsonify(parsedSentences)


@app.route("/evaluate", methods = ['POST'])
def evaluate():
  goldFile = request.files['gold_file']
  inputFile = request.files['input_file']
  filterLabel = request.form['filter_label']
  isAllowed = allowedFile(goldFile.filename) and allowedFile(inputFile.filename)
  if isAllowed:
    goldFilename = secure_filename(goldFile.filename)
    inputFilename = secure_filename(inputFile.filename)
    urlGold = os.path.join(UPLOAD_GOLD, goldFilename)
    urlInput = os.path.join(UPLOAD_FOLDER, inputFilename)
    goldFile.save(urlGold)
    inputFile.save(urlInput)

    # if (filterLabel != ""):
    #   urlOldGold = urlGold
    #   urlGold = os.path.join(UPLOAD_GOLD, \
    #     goldFilename + "_" + filterLabel.replace(":", "") + ".conllu")
    #   util.filterGold(urlOldGold, urlGold, filterLabel)
    #   urlOldInput = urlInput
    #   urlInput = urlOldInput + "_" + urlGold.split("_")[2]
    #   util.filterFile(urlOldInput, urlGold, urlInput)

    # result = util.evaluate(urlGold, urlInput)
    result = util.evaluate(urlGold, urlInput, filterLabel)
    print(result)
  return jsonify(result)


@app.route("/compare", methods = ['POST'])
def compare():
  goldFile = request.files['gold_file']
  inputFile = request.files['input_file']
  comparedFile = request.files['compared_file']
  filterLabel = request.form['filter_label']
  isAllowed = allowedFile(goldFile.filename) and allowedFile(inputFile.filename) and allowedFile(comparedFile.filename)
  if isAllowed:
    goldFilename = secure_filename(goldFile.filename)
    inputFilename = secure_filename(inputFile.filename)
    comparedFilename = secure_filename(comparedFile.filename)
    urlGold = os.path.join(UPLOAD_GOLD, goldFilename)
    urlInput = os.path.join(UPLOAD_FOLDER, inputFilename)
    urlCompared = os.path.join(UPLOAD_FOLDER, comparedFilename)
    goldFile.save(urlGold)
    inputFile.save(urlInput)
    comparedFile.save(urlCompared)

    result = util.compare(urlGold, urlInput, urlCompared, 'label', filterLabel)

  return jsonify(result)


@app.route("/parse", methods = ['POST'])
def parse():
  sentence = request.json['sentence']
  parser = request.json['parser']
  urlSentence = os.path.join(UPLOAD_FOLDER, 'sentence.conllu')
  util.saveSentenceInConllu(sentence, urlSentence)
  util.parse(urlSentence, 'spacy')
  # condition if spacy
  parsedSentence = []
  sentence = util.getSentenceWithID(1, 'result.txt')
  parsedSentence.append(util.sentenceToDep(sentence))
  print(parsedSentence)
  return jsonify(parsedSentence)


if __name__=="__main__":
  app.run(debug=True, port = 5000, host = 'localhost')