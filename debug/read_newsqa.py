
from __future__ import absolute_import, division, print_function

import argparse
import collections
import json
import math
import os
import random
import sys
sys.path.append('../..')

from io import open

class SquadExample(object):
    """
    A single training/test example for the Squad dataset.
    For examples without an answer, the start and end position are -1.
    """

    def __init__(self,
                 qas_id,
                 question_text,
                 doc_tokens,
                 orig_answer_text=None,
                 start_position=None,
                 end_position=None,
                 is_impossible=None):
        self.qas_id = qas_id
        self.question_text = question_text
        self.doc_tokens = doc_tokens
        self.orig_answer_text = orig_answer_text
        self.start_position = start_position
        self.end_position = end_position
        self.is_impossible = is_impossible

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = ""
        s += "qas_id: %s" % (self.qas_id)
        s += ", question_text: %s" % (
            self.question_text)
        s += ", doc_tokens: [%s]" % (" ".join(self.doc_tokens))
        if self.start_position:
            s += ", start_position: %d" % (self.start_position)
        if self.start_position:
            s += ", end_position: %d" % (self.end_position)
        if self.start_position:
            s += ", is_impossible: %r" % (self.is_impossible)
        return s

def read_squad_examples(input_file, is_training, version_2_with_negative):

    #Uncomment to manually validate the generated vs guessed answers
    clean_word_indexed_answers = open('./clean_word_indexed_answers', 'w+')
    unclean_char_indexed_answers_from_input = open('./unclean_char_indexed_answers_from_input', 'w+')

    """Read a SQuAD json file into a list of SquadExample."""
    with open(input_file, "r", encoding='utf-8') as reader:
        input_data = json.load(reader)["data"]

    def is_whitespace(c):
        if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
            return True
        return False

    examples = []
    for entry in input_data:
        for paragraph in entry["paragraphs"]:
            # print (paragraph)
            paragraph_text = paragraph["context"]
            paragraph_text= paragraph_text.replace("\n", "  ")
            doc_tokens = []
            char_to_word_offset = []
            prev_is_whitespace = True
            for c in paragraph_text:
                if is_whitespace(c):
                    prev_is_whitespace = True
                else:
                    if prev_is_whitespace:
                        doc_tokens.append(c)
                    else:
                        doc_tokens[-1] += c
                    prev_is_whitespace = False
                char_to_word_offset.append(len(doc_tokens) - 1)

            for qa in paragraph["qas"]:
                qas_id = qa["id"]
                question_text = qa["question"]
                start_position = None
                end_position = None
                orig_answer_text = None
                is_impossible = False
                if is_training:
                    if version_2_with_negative:
                        is_impossible = qa["is_impossible"]
                    if (len(qa["answers"]) != 1) and (not is_impossible):
                        raise ValueError(
                            "For training, each question should have exactly 1 answer.")
                    if not is_impossible:
                        answer = qa["answers"][0]
                        orig_answer_text = answer["text"]
                        answer_offset = answer["answer_start"]
                        answer_length = len(orig_answer_text)
                        start_position = char_to_word_offset[answer_offset]
                        end_position = char_to_word_offset[answer_offset + answer_length - 1]

                        cleaned_word_indexed_text = " ".join(doc_tokens[start_position:(end_position + 1)])

                        #To manually validate the generated vs guessed answers
                        clean_word_indexed_answers.write(cleaned_word_indexed_text+"\n")
                        unclean_char_indexed_answers_from_input.write(orig_answer_text+"\n")

                        # Following is not valid for NewsQA, since:
                        # - indexing is a bit off for most questions,
                        # actual_text.find(cleaned_answer_text) == -1 will thus fail in most even
                        # with no "weird Unicode stuff"
                        # - the encoding is pretty much handled properly in the tokens already
                        # --- Only applicable for SQuAD ----
                        # Only add answers where the text can be exactly recovered from the
                        # document. If this CAN'T happen it's likely due to weird Unicode
                        # stuff so we will just skip the example.
                        #
                        # Note that this means for training mode, every example is NOT
                        # guaranteed to be preserved.
                        #if actual_text.find(cleaned_answer_text) == -1:
                        #    print("WARNING: Indexing seems a bit off for question:", question_text)
                        #    print("Our guess : ", actual_text," vs. actual answer ", cleaned_answer_text)
                        #    continue
                        # --------------END-------------------
                    else:
                        start_position = -1
                        end_position = -1
                        actual_text = ""
                        cleaned_word_indexed_text = ""

                # we use actual_text instead of orig_answer_text for NewsQA, since the
                # indexing of character is not perfect.
                # actual_text gives tokens while retaning the word indexing
                # verified through manual comparison of the answers generated
                example = SquadExample(
                    qas_id=qas_id,
                    question_text=question_text,
                    doc_tokens=doc_tokens,
                    orig_answer_text=cleaned_word_indexed_text,
                    start_position=start_position,
                    end_position=end_position,
                    is_impossible=is_impossible)
                examples.append(example)
    print ("OK", len(examples))

    # Uncomment to manually validate the generated vs guessed answers
    unclean_char_indexed_answers_from_input.close()
    clean_word_indexed_answers.close()
    return examples

# SQuAD training dataset
#read_squad_examples("train-v2.0.json", True, True)

# NewsQA training dataset
# read_squad_examples("../output/newsQaJSONSquadFormat.json", True, True)
read_squad_examples("../output/splitData/<PASS_FILENAME>.json", True, True)
