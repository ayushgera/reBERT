# Converting from newsQA to SQuAD
import csv
import os as os
import pandas as pd
import re as regex

filePathDataset = os.path.abspath("../../Masters Projects/Dataset/newsqa-data-v1/newsqa-data-v1Copy.csv")
filePathStories = os.path.abspath("../../Masters Projects/Dataset/cnn_stories/cnn_stories")
REPLACE_WITH_NO_SPACE = \
    regex.compile("(\()|(\,)|(\")|(\))|(\–)|(\.)|(\;)|(\!)|(\-)|(<br />)|@highlight|(cnn)|(\:)|(\“)|(\’)|(\‘)|(\”)|(\')")

# Function does first-level data cleaning
def getStoryPreProcessedContent(storyContent):
    content = ""
    for line in storyContent:
        content = content + (regex.sub(REPLACE_WITH_NO_SPACE, "", line).lower()).strip()

    return content

# Function determines if at all an answer is present
def isAnswerPresent(answerArray):
    for i in len(answerArray):
        if answerArray[i].lower().strip() != "none":
            return answerArray[i]

    return False

# Function returns the answer of the question
def getAnswerGivenCharRange(ansCharRange):


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

storiesId = {}
# skip question if no answer


# Construction of JSON data


for i in len(dataFrameDataSet):
    # Skip if no answer present
    answerArray = (dataFrameDataSet["answer_char_ranges"][i]).split("|")
    answerPresence = isAnswerPresent(answerArray)

    if not answerPresence:
        # No answer present
        continue

    # Get answer
    answer = getAnswerGivenCharRange(answerPresence)

    storyId = dataFrameDataSet["story_id"][i]


    if(storiesId[storyId]):
        # paragraph already present, question has been added
    else:
        # new paragraph added
        storiesId[storyId] = True
        dataElement["title"] = "someDummyTitle"

        # Stories Path
        storiesPath = os.path.abspath(filePathStories + dataFrameDataSet["story_id"][0])
        if not os.path.isfile(storiesPath):
            raise TypeError(storiesPath + " is not present")

        story = open(storiesPath, encoding="utf-8")



        dataElement["context"] = getStoryPreProcessedContent(story)

print(dataFrameDataSet["story_id"][0])


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

