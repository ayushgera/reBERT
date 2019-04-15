###### Load and clean synonyms #######

synonym_mapping = {}
with open('synonyms.txt') as fp:
    for line in fp:
        if len(line.split()) > 3:  #Exist at least one synonym            
            word = line.split()[2].strip("[]")
            synonyms = set(map(str.strip, line[line.rfind("]")+1:].strip().split(",")))  #Extract all syn, separated by comma
            synonym_mapping[word] = synonyms

with open('stopwords.txt') as fp:
    for word in fp:
            del synonym_mapping[word] #Remove stop words
            
######## Load questions and output json with all reformulations ########
            
import pandas as pd
import math
import copy
import json
import io
import numpy as np

data = pd.read_csv("combined-newsqa-data-v1.csv")

data = data.values

data_id = 1

output = {
    "version": "v2.0",
    "data": []
}

# story_id,question,answer_char_ranges,is_answer_absent,is_question_bad,validated_answers,story_text
k = {
    "story_id": 0,
    "question": 1,
    "answer_char_ranges": 2,
    "is_answer_absent": 3,
    "is_question_bad": 4,
    "validated_answers": 5,
    "story_text": 6
}

story_id_map = {}
lens = []  #Keep track of how many Q's are created from synonyms
part = 0.5
for i in range(int(len(data) * part)):
    
    data[i][k["story_text"]] = data[i][k["story_text"]].replace('\r',' ')
    data[i][k["story_text"]] = data[i][k["story_text"]].replace('\n',' ')
    data[i][k["story_text"]] = data[i][k["story_text"]].replace('\'',"'")
    data[i][k["story_text"]] = data[i][k["story_text"]].replace('\"','"')
    data[i][k["story_text"]] = data[i][k["story_text"]].replace('\t',' ')
    
    org_question = str(data[i][k["question"]])
    
    questions = []
    questions.append(org_question)
    
    Q_words = org_question.split()
    
    for ind, word in enumerate(Q_words):
        if word in synonym_mapping:  #The word can be replaced!
            for synonym in synonym_mapping[word]:
                Q_words_new = Q_words.copy()
                Q_words_new[ind] = synonym
                questions.append(' '.join(w for w in Q_words_new))
    lens.append(len(questions)-1)
    
    j=0
    for Q in questions:
        answer_idxx = data[i][k["answer_char_ranges"]].split("|")[0]
        answer_idx = answer_idxx.split(",")[0]
        
        if (answer_idx == "None"):
            qas = {
                "plausible_answers": [],
                "question": Q,
                "id": str(j),
                "answers": [],
                "is_impossible": True
            }

        elif (data[i][k["is_question_bad"]].isnumeric() and float(data[i][k["is_answer_absent"]]) >= 0.5 and float(data[i][k["is_question_bad"]]) >= 0.5):
            qas = {
                "plausible_answers": [],
                "question": Q,
                "id": str(j),
                "answers": [],
                "is_impossible": True
            }

        else:
            answer_start, answer_end = answer_idx.split(":")
            answer_start = int(answer_start)
            answer_end = int(answer_end)

            answer_text = copy.copy(data[i][k["story_text"]][answer_start:answer_end])
            answer_text = answer_text.strip()

            qas = {
                "question": Q,
                "id": str(j),
                "answers": [{
                    "text": answer_text,
                    "answer_start": answer_start
                }],
                "is_impossible": False
            }

        if (not data[i][k["story_id"]] in story_id_map):
            story_id_map[data[i][k["story_id"]]] = {
                "title": str(i),
                "paragraphs": [{
                "qas": [ qas ],
                "context": data[i][k["story_text"]]
                }]
            }
        else:
            story_id_map[data[i][k["story_id"]]]["paragraphs"][0]["qas"].append(qas)
        j+=1 #New Q found!
        
#Write dictionary to file
for item in story_id_map:
    output["data"].append(story_id_map[item])

filename = 'newsqa_' + "singleSynonymQuestions_"+str(part) + '.json'
with open(filename, "w") as fp:
    json.dump(output , fp)