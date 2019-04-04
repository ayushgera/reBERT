import json
import sys
import math
import os
import re

def question_type_split():
    
    with open(os.path.abspath("./debug2/newsqa_validated_0_100.json"), 'r') as input_json_file:
        input_json= json.load(input_json_file)['data']
        for entry in input_json:
            entry["paragraphs"][0]["qas"][:] = \
                [qa for qa in entry["paragraphs"][0]["qas"] \
                    if qa["question"].lower().startswith("who") is True \
                        or qa["question"].lower().startswith("what") is True \
                        or qa["question"].lower().startswith("when") is True]

        input_json[:] = [entry for entry in input_json \
            if len(entry["paragraphs"][0]["qas"])>0]

        # print("--------")
        # for entry in input_json:
        #     for qa in entry["paragraphs"][0]["qas"]:
        #         print(qa["question"])
        # input_json_file.close()

    with open('question_type_split_0_100.json',
            'w') as question_type_split:
        output = {}
        output['data'] = input_json
        json.dump(output, question_type_split, ensure_ascii=False)
        question_type_split.close()
    
    with open('question_type_split_0_100_info.txt',
            'w') as info_file:
        info = {}
        who = 0
        what = 0
        when = 0
        for entry in input_json:
            for qa in entry["paragraphs"][0]["qas"]:
                if qa["question"].lower().startswith("who"):
                    who+=1
                elif qa["question"].lower().startswith("what"):
                    what+=1
                elif qa["question"].lower().startswith("when"):
                    when+=1
        info['who'] = who
        info['what'] = what
        info['when'] = when
        info['contexts'] = len(input_json)
        json.dump(info, info_file, ensure_ascii=False)
        question_type_split.close()

if __name__ == "__main__":
    #training_set_size = sys.argv[1]
    question_type_split()
