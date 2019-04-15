import pandas as pd
import math
import copy
import json
import io
import sys
import nltk

def get_best_possible_ans(possible_ans):
	default_ans = ""
	for i in possible_ans["src1"]:
		default_ans = i[0] + ":" + i[1] # can be improved by taking max vote

		for j in possible_ans["src2"]:
			if abs(int(i[0]) - int(j[0])) < 3:
				# print ("similar", i, j, i[0], i[1])
				return i[0] + ":" + i[1]

	# print ("default_ans", default_ans, possible_ans["src1"])
	return default_ans

def read_newsqa(start, end):
	# vocab = open("vocab.txt", "r").readlines()
	data = pd.read_csv("./data/newsQA/combined-newsqa-data-v1.csv")
	data = data.values
	data_id = 1
	
	output = {
		"version": "1.1",
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
	start_pct = start
	end_pct = end
	start_read = int(start_pct * len(data))
	end_read = int(end_pct * len(data))
	# data_size = 0.9
	# train_data = int(data_size * len(data))
	country_city_names = []
	
	for i in range(start_read, end_read):
		
		# ALTERNATIVE 1 - USE THIS TO COMPARE answer from crowdsourcer and validators
		# if (isinstance(data[i][k["validated_answers"]], float)): continue
		# possible_ans = {"src1": [], "src2": []}
		# val_ans = json.loads(data[i][k["validated_answers"]])
		# for j in val_ans:
		# 	splt_validated = j.split(":")
		# 	if (len(splt_validated) == 1): continue

		# 	possible_ans["src1"].append(splt_validated)

		# if len(possible_ans["src1"]) == 0: continue

		# test = data[i][k["answer_char_ranges"]].split("|")
		# for kt in test:
		# 	test2 = kt.split(",")
		# 	for ktt in test2:
		# 		splt_answer = ktt.split(":")
		# 		if (len(splt_answer) == 1): continue

		# 		possible_ans["src2"].append(splt_answer)

		# answer_idx = get_best_possible_ans(possible_ans)

		# ALTERNATIVE 2 - USE THIS TO GENERATE test.json FROM test.csv
		# is it possible that the multiple answer matters during prediction?
		answer_idxx = data[i][k["answer_char_ranges"]].split("|")[0]
		answer_idx = answer_idxx.split(",")[0]

		key_id = str(data[i][k["story_id"]]) 

		data[i][k["story_text"]] = data[i][k["story_text"]].replace('\r',' ')
		data[i][k["story_text"]] = data[i][k["story_text"]].replace('\n',' ')
		data[i][k["story_text"]] = data[i][k["story_text"]].replace('\'',"'")
		data[i][k["story_text"]] = data[i][k["story_text"]].replace('\"','"')
		data[i][k["story_text"]] = data[i][k["story_text"]].replace('\t',' ')
		data[i][k["story_text"]] = data[i][k["story_text"]].strip()

		if (answer_idx == "None"):
			continue
			# qas = {
			# 	"plausible_answers": [],
			# 	"question": str(data[i][k["question"]]),
			# 	"id": str(i),
			# 	"answers": [],
			# 	"is_impossible": True
			# }
		elif (	data[i][k["is_question_bad"]].isnumeric() and 
				float(data[i][k["is_answer_absent"]]) >= 0.0 and 
				float(data[i][k["is_question_bad"]]) >= 0.0 ):
			continue
			# qas = {
			# 	"plausible_answers": [],
			# 	"question": str(data[i][k["question"]]),
			# 	"id": str(i),
			# 	"answers": [],
			# 	"is_impossible": True
			# }
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

		if (not key_id in story_id_map):
			# print ("new: " + key_id)
			story_id_map[key_id] = {
				"title": key_id,
				"paragraphs": [{
					"qas": [ qas ],
					"context": data[i][k["story_text"]]
				}]
			}
		else:
			story_id_map[key_id]["paragraphs"][0]["qas"].append(qas)

		# # verify
		# validate_answer = answer_text.split(' ')
		# for j in validate_answer:
		# 	if not (j + "\n") in vocab: 
		# 		print (j)

	for item in story_id_map:
		output["data"].append(story_id_map[item])

	print ("LEN", len(output["data"]))

	filename = './data/newsQA/validated/newsqa_validated_' + str(int(start_pct * 100.0)) + "_" + str(int(end_pct * 100.0)) + '.json'
	with open(filename, "w") as fp:
		json.dump(output , fp) 
	
if __name__ == "__main__":
    read_start = int(sys.argv[1])/100
    read_end = int(sys.argv[2])/100
    read_newsqa(read_start, read_end)

