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

# Returns un-preprocessed story
def getStory(story):
    content = ""
    for line in story:
        content = content + line.replace("\n", "\\n")

    return content


# Function determines if at all an answer is present
def isAnswerPresent(answerArray):
    for i in range(0,len(answerArray)-1):
        if answerArray[i].lower().strip() != "none":
            return answerArray[i]

    return False

# Function returns the answer of the question
def getAnswerGivenCharRange(ansCharRange,story):
    rangeSplit = ansCharRange.split(":")
    return story[int(rangeSplit[0]):int(rangeSplit[1])]

def getStartAnswerCharIndex(ansCharRange):
    rangeSplit = ansCharRange.split(":")
    return int(rangeSplit[0])


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

# Construction of JSON data

for i in range(0,len(dataFrameDataSet)-1):
    # Skip if no answer present
    answerArray = (dataFrameDataSet["answer_char_ranges"][i]).split("|")
    answerPresence = isAnswerPresent(answerArray)

    if not answerPresence:
        # No answer present - don't add question/para to dataset
        continue

    id = dataFrameDataSet["story_id"][i]
    storiesPath = os.path.abspath(filePathStories + id)
    if not os.path.isfile(storiesPath):
        raise TypeError(storiesPath + " is not present")

    story = open(storiesPath, encoding="utf-8")
    # Get answer
    answer = getAnswerGivenCharRange(answerPresence,getStory(story))

    if id in storiesId:
        # paragraph already present, question has been added
        print("Story already present")
    else:
        # new paragraph added
        storiesId[id] = True
        dataElement["title"] = "someDummyTitle"
        # paragraph
        dataElement["context"] = getStoryPreProcessedContent(getStory(story))

        # answer
        answerElement["answer_start"] = getStartAnswerCharIndex(answerPresence)
        answerElement["text"] = answer

        # question
        dataElement["question"] = dataFrameDataSet["answer"][i]
        dataElement["id"] = id

    # Building up of objects
    dataElement["answers"].append(answerElement)

    qasElement["answers"] = dataElement["answers"]
    qasElement["question"] = dataElement["question"]
    qasElement["id"] = dataElement["id"]
    dataElement["qas"].append(qasElement)

    paragraphElement["context"] = dataElement["context"]
    paragraphElement["qas"] = dataElement["qas"]
    paragraphElement["storyId"] = id
    dataElement["paragraphs"].append(paragraphElement)

    dataObject["title"] = dataElement["title"]
    dataObject["paragraphs"] = dataElement["paragraphs"]
    data["data"].append(dataObject)

squadWrapper["data"] = data["data"]
squadWrapper["version"] = "1.1"

