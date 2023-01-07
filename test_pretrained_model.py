def phish(url):
	# Basic libraries
	import os
	import io
	import sys
	import math
	import time
	import random
	import requests
	import collections
	import numpy as np
	from os import walk
	import pandas as pd
	from joblib import dump, load
	from langdetect import detect
	from tokenizers import ByteLevelBPETokenizer

	tokenizerFolder = 'pretrained_models'
	savedModelDirectory = 'pretrained_models'
	websiteToTest = url
	threshold = 0.5
	# tokenizerFolder = "pretrained_models"
	# savedModelDirectory = "pretrained-models"
	# websiteToTest = url
	# threshold = 0.5

	# Loading files
	# Load tokenization files
	tokenizer = ByteLevelBPETokenizer(
		tokenizerFolder + "/pretrained_Tokenizer-10000.tok-vocab.json",
		tokenizerFolder + "/pretrained_Tokenizer-10000.tok-merges.txt",
	)
	tokenizerVocabSize = tokenizer.get_vocab_size()
	print("Tokenizer files have been loaded and the vocab size is %d..." % tokenizerVocabSize)

	# Load saved model
	model = load(savedModelDirectory + "/pretrained-phishytics-model.joblib")
	print("Model loaded...")

	# Load document frequency dictionary
	docDict = np.load(savedModelDirectory + "/document-frequency-dictionary.npy", allow_pickle=True).item()
	print("Document frequency dictionary loaded...")

	# Testing
	print("Loading webpage...")
	try:
		request = requests.get(websiteToTest)
		webpageHtml = str(request.text)
		webpageHtml = webpageHtml.replace("\n", " ")

		# Convert text into feature vector
		output = tokenizer.encode(webpageHtml)
		outputDict = collections.Counter(output.ids)
	except Exception as e:
		print("**** Error loading the website ****")
		print(e)
		exit()

	# Apply tfidf weighting
	totalFilesUnderConsideration = 18500 # total number of documents/html files in our training data
	array = [0] * tokenizerVocabSize
	for item in outputDict:
		if len(docDict[item]) > 0:
			array[item] = (outputDict[item]) * (math.log10( totalFilesUnderConsideration / len(docDict[item] )))

	# Getting predictions
	predictionProbability = model.predict_proba([array])[0][1]
	# print("\n****************************\n--> Probability that the website is phishing: %.2f" % (predictionProbability * 100))

	prediction = "NOT PHISHING"
	if predictionProbability > threshold:
		prediction = "PHISHING"
	# print("--> Based on your threshold of %.2f, this website is +++'%s'+++" % (threshold, prediction))
	# print("****************************")
	return predictionProbability * 100, prediction, threshold

# print(phish("https://fb.com"))