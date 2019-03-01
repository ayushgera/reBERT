# Converting from newsQA to SQuAD
import csv
import os as os
import pandas as pd

filePathDataset = os.path.abspath("../../Masters Projects/Dataset/newsqa-data-v1/newsqa-data-v1Copy.csv")
filePathStories = os.path.abspath("../../Masters Projects/Dataset/cnn_stories/cnn_stories/cnn/stories")

# Initializing
dataFrameDataSet = pd.read_csv(filePathDataset)

squadWrapper = {}
dataElement = {}
data = dict()
data["data"] = [] # Array of objects
dataObject = {}
dataElement["answers"] = [] # Array of objects
answerElement = {}
qasElement = {}
dataElement["paragraphs"] = [] # Array of objects
paragraphElement = {}
dataElement["qas"] = [] # Array of objects
# skip question if no answer

dataElement["title"] = "someDummyTitle"

# Construction of JSON data
# Stories Path
dataFrameDataSet


dataElement["context"] = "fsdfsdfsdgfdgiojaguiohtuhrtwerhrhwearj"
answerElement["answer_start"] = 654
answerElement["text"] = "some answer"

dataElement["question"] = "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?"
dataElement["id"] = "SomeUniqueId"

# Building up of objects
dataElement["answers"].append(answerElement)

qasElement["answers"] = dataElement["answers"]
qasElement["question"] = dataElement["question"]
qasElement["id"] = dataElement["id"]
dataElement["qas"].append(qasElement)

paragraphElement["context"] = dataElement["context"]
paragraphElement["qas"] = dataElement["qas"]
dataElement["paragraphs"].append(paragraphElement)

dataObject["title"] = dataElement["title"]
dataObject["paragraphs"] = dataElement["paragraphs"]
data["data"].append(dataObject)

squadWrapper["data"] = data["data"]
squadWrapper["version"] = "1.1"
print(squadWrapper)