import json
import sys
import os
import math


def build_missed_vocab():
    partial_vocab_miss_main= set()
    
    with open(os.path.abspath("./debug/partial_vocab_miss"), 'r') as partial_vocab_miss:
        data= json.load(partial_vocab_miss)
        for sub_tokn in data:
            partial_vocab_miss_main.add(sub_tokn)
        partial_vocab_miss.close()

    print(len(partial_vocab_miss_main))
    # Create new JSON File
    with open("partial_vocab_miss_main", 'w') as f:
        json.dump(list(partial_vocab_miss_main), f, ensure_ascii=False, indent=4)
        f.close()

if __name__ == "__main__":
    build_missed_vocab()
