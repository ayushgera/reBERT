import pandas as pd
import math
import copy
import json
import io

# vocab = open("vocab.txt", "r").readlines() 
# or download from here "https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-cased-vocab.txt"
# or download from here "https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-vocab.txt"

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
data_size = 0.01
train_data = int(data_size * len(data))
for i in range(0, train_data):
	data[i][k["story_text"]] = data[i][k["story_text"]].replace('\r',' ')
	data[i][k["story_text"]] = data[i][k["story_text"]].replace('\n',' ')
	data[i][k["story_text"]] = data[i][k["story_text"]].replace('\'',"'")
	data[i][k["story_text"]] = data[i][k["story_text"]].replace('\"','"')
	data[i][k["story_text"]] = data[i][k["story_text"]].replace('\t',' ')

	answer_idxx = data[i][k["answer_char_ranges"]].split("|")[0]
	answer_idx = answer_idxx.split(",")[0]

	if (answer_idx == "None"):
		qas = {
			"plausible_answers": [],
			"question": str(data[i][k["question"]]),
			"id": str(i),
			"answers": [],
			"is_impossible": True
		}
	elif (	data[i][k["is_question_bad"]].isnumeric() and 
			float(data[i][k["is_answer_absent"]]) >= 0.5 and 
			float(data[i][k["is_question_bad"]]) >= 0.5 ):
		qas = {
			"plausible_answers": [],
			"question": str(data[i][k["question"]]),
			"id": str(i),
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
			"question": str(data[i][k["question"]]),
			"id": str(i),
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

	# # verify
	# validate_answer = answer_text.split(' ')
	# for j in validate_answer:
	# 	if not (j + "\n") in vocab: 
	# 		print (j)

for item in story_id_map:
	output["data"].append(story_id_map[item])

filename = 'newsqa_' + str(int(data_size * 100)) + '.json'
with open(filename, "w") as fp:
    json.dump(output , fp) 

