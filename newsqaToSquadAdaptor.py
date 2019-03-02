# Converting from newsQA to SQuAD
import csv
import os as os
import pandas as pd
import re as regex
import json

filePathDataset = os.path.abspath("./data/newsqa-data-v1/newsqa-data-v1.csv")
filePathStories = os.path.abspath("./data/")
REPLACE_WITH_NO_SPACE = \
    regex.compile("(\()|(\,)|(\")|(\))|(\–)|(\;)|(\!)|(\-)|(<br />)|@highlight|(cnn)|(\:)|(\“)|(\’)|(\‘)|(\”)|(\')|(\\n)")

# Function does first-level data cleaning
def getStoryPreProcessedContent(storyContent):
    content = regex.sub(REPLACE_WITH_NO_SPACE, "", storyContent).lower()
    return content

# Returns un-preprocessed escaped story
def getEscapedStory(story):
    return story.replace("\n", "\\n")

# Returns un-preprocessed story
def getStory(story):
    content = ""
    for line in story:
        content = content + line
    return content

# Function determines if at all an answer is present
def isAnswerPresent(answerArray):
    for i in range(0,len(answerArray)):
        if answerArray[i].lower().strip() != "none":
            return answerArray[i]

    return False

def getAnswersAsText(answerArray, story):
    answersList=[]
    for i in range(0,len(answerArray)):
        if answerArray[i].lower().strip() != "none":
            answerElement= {}
            rangeSplit = answerArray[i].split(":")
            # remove below filter once multi-range line answers are handled
            if rangeSplit[0].find(",") ==-1 and rangeSplit[1].find(",") ==-1:
                answer= story[int(rangeSplit[0]):int(rangeSplit[1])]
                answerElement["answer_start"] = int(rangeSplit[0])
                answerElement["text"] = answer.strip()
                answersList.append(answerElement)
    return answersList

# Function returns the answer of the question
def getAnswerGivenCharRange(ansCharRange,story):
    rangeSplit = ansCharRange.split(":")
    return story[int(rangeSplit[0]):int(rangeSplit[1])]

def getStartAnswerCharIndex(ansCharRange):
    rangeSplit = ansCharRange.split(":")
    return int(rangeSplit[0])

def createNewQuestion(question, answerArray, unprocessedStory):
    # Building up of objects
    qaElement= {}
    qaElement["answers"] = getAnswersAsText(answerArray, getEscapedStory(unprocessedStory))
    qaElement["question"] = question
    qaElement["id"] = id
    return qaElement

# Initializing
dataFrameDataSet = pd.read_csv(filePathDataset)
dataFrameDataSet.dropna(how="all", inplace=True) 

squadWrapper = {}
data = dict()
data["data"] = []
storiesId = {}

# Construction of JSON data
for i in range(0, len(dataFrameDataSet)):
    # Skip if no answer present
    answerArray = (dataFrameDataSet["answer_char_ranges"][i]).split("|")
    answerPresence = isAnswerPresent(answerArray)

    if not answerPresence:
        # No answer present - don't add question/para to dataset
        continue

    id = dataFrameDataSet["story_id"][i]
    storiesPath = os.path.abspath("./data/" + id)
    if not os.path.isfile(storiesPath):
        raise TypeError(storiesPath + " is not present")

    story = open(storiesPath, encoding="utf-8")
    unprocessedStory = getStory(story)

    if id in storiesId:
        # paragraph already present, question has been added
        # print("Story already present")
        for storyElement in data["data"]:
            if storyElement["title"] == id:
                print("Adding for id: ",storyElement["title"])
                currentQuestions= storyElement["paragraphs"]["qas"]
                currentQuestions.append(
                    createNewQuestion(
                        dataFrameDataSet["question"][i], 
                        answerArray, 
                        unprocessedStory))
                storyElement["paragraphs"]["qas"]= currentQuestions
    else:
        # new paragraph added
        storiesId[id] = True
        
        firstQuestion= []
        firstQuestion.append(createNewQuestion(dataFrameDataSet["question"][i], answerArray, unprocessedStory))
        
        paragraphElement = {}
        paragraphElement["context"] = getStoryPreProcessedContent(unprocessedStory)
        paragraphElement["qas"] = firstQuestion
        paragraphElement["storyId"] = id

        dataObject = {}
        dataObject["title"] = id
        dataObject["paragraphs"] = paragraphElement
        data["data"].append(dataObject)

squadWrapper["data"] = data["data"]
squadWrapper["version"] = "1.1"


# Create new JSON File
with open('newsQaJSONSquadFormat.json', 'w') as f:
  json.dump(squadWrapper, f, ensure_ascii=False)

