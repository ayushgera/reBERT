python run_reBERT.py --bert_model experiment/squad_newsqa_synonym_0.5/ \
--do_train \
--do_lower_case \
--train_file data/newsqa/newsqa_singleSynonymQuestions_0.5.json \
--learning_rate 0.0005 \
--vocab_file data/newsqa/vocab.txt \
--num_train_epochs 1 \
--max_seq_length 192 \
--max_query_length 32 \
--warmup_proportion 0.2 \
--max_answer_length 15 \
--train_batch_size 64 \
--output_dir experiment/squad_newsqa_synonym_0.5

python run_reBERT.py --bert_model experiment/squad_newsqa_synonym_0.5 \
 --do_predict --do_lower_case --predict_file data/newsqa/test.json \
 --output_dir experiment/squad_newsqa_synonym_0.5

python evaluate-reBERT.py \
data/newsqa/test.json \
experiment/squad_newsqa_synonym_0.5/predictions.json \
experiment/squad_newsqa_synonym_0.5/eval_result

