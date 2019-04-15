"""
nmt based query reformulation
"""

from googletrans import Translator
import csv


def google_translate_csv(questions, metadata, header, output, src, dst):
    print(questions[0:3])
    generated_questions = []
    translator = Translator()
    for question in questions:
        if len(question) < 15000:  # api limit: num of characters < 15k
            print('translating {}'.format(question))
            dst_obj = translator.translate(question, dest=dst, src=src)
            src_obj = translator.translate(dst_obj.text, dest=src, src=dst)
            generated_questions.append(src_obj.text)
    with open(output, 'w') as fout:
        fout.write(header)
        for q, m in zip(generated_questions, metadata):
            m.insert(1, q)
            fout.write(','.join(m) + '\n')


def google_translate_text(questions, output, src, dst):
    translator = Translator()
    with open(output, 'w') as fout:
        for question in questions:
            if len(question) < 15000:  # api limit: num of characters < 15k
                print('translating {}'.format(question))
                dst_obj = translator.translate(question, dest=dst, src=src)
                src_obj = translator.translate(dst_obj.text, dest=src, src=dst)
                fout.write(src_obj.text + '\n')


def extract_questions_csv(csv_file):
    with open(csv_file, 'r') as fin:
        questions = []
        metadata = []
        header = []
        reader = csv.reader(fin, delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:
                header = row
            else:
                question = row.pop(1)
                questions.append(question)
                metadata.append(row)
        return questions, metadata, header


def extract_questions_text(txt):
    questions = []
    with open(txt, 'r') as fin:
        for line in fin:
            questions.append(line.strip())
    return questions


def run_csv():
    csv_newsqa = 'newsqa-data-v1.csv'
    csv_output = 'zhcn-newsqa-data-v1.csv'
    questions, metadata, header = extract_questions_csv(csv_newsqa)
    google_translate_csv(questions, metadata, header, csv_output, 'en', 'zh-CN')


def run_text():
    text_newsqa = 'question_090.txt'
    text_output = 'zhcn-question_090.txt'
    questions = extract_questions_text(text_newsqa)
    google_translate_text(questions, text_output, 'en', 'zh-CN')


def clean(questions, metadata):
    startwords = ['what', 'who', 'when', 'how', 'why', 'where']
    clean_questions = []
    clean_metadata = []
    for i, question in enumerate(questions):
        question = question.lower()
        words = question.split()
        if words[0] in startwords and words[-1][-1] == '?':
            clean_questions.append(question)
            clean_metadata.append(metadata[i])
    return clean_questions, clean_metadata


def main():
    run_text()
    # run_csv()


if __name__ == "__main__":
    main()

