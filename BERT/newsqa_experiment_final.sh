


python run_squad.py \
  --bert_model experiment/192_32_0.0005_3_0.2_15_newsqa_validated_0_50 \
  --do_predict \
  --do_lower_case \
  --predict_file data/newsqa/test_100.json \
  --output_dir experiment/192_32_0.0005_3_0.2_15_newsqa_validated_0_50/
python evaluate-v1.1.py data/newsqa/test_100.json experiment/192_32_0.0005_3_0.2_15_newsqa_validated_0_50/predictions.json experiment/192_32_0.0005_3_0.2_15_newsqa_validated_0_50/eval_result
# {"exact_match": 36.708558321785254, "f1": 52.0992179208182}


# {"exact_match": 35.31980174651876, "f1": 50.9544175081756}

# BEST
# {'exact_match': 38.11659192825112, 'f1': 52.04609109253138}
# 192_32_0.0005_1_0.2_15_newsqa_singleSynonymQuestions_0.5
# {'exact_match': 37.14892612697663, 'f1': 52.24470131966855}
# 192_32_0.0005_3_0.1_15_newsqa_validated_0_50

python run_squad.py \
	--bert_model experiment/192_32_0.0005_1_0.2_15_newsqa_singleSynonymQuestions_0.5/ \
	--do_train \
	--do_lower_case \
	--train_file data/newsqa/newsqa_validated_0_50.json \
	--learning_rate 0.0005 \
	--vocab_file data/newsqa/vocab.txt \
	--num_train_epochs 3 \
	--max_seq_length 192 \
	--max_query_length 32 \
	--warmup_proportion 0.1 \
	--max_answer_length 15 \
	--output_dir experiment/bert-base-uncased-squad-newsqa-twice-model-v1.1/ \
	--verbose_logging 

python run_squad.py --bert_model experiment/bert-base-uncased-squad-newsqa-twice-model-v1.1 \
 --do_predict --do_lower_case --predict_file data/newsqa/test.json \
 --output_dir experiment/bert-base-uncased-squad-newsqa-twice-model-v1.1

python evaluate-v1.1.py data/newsqa/test.json experiment/bert-base-uncased-squad-newsqa-twice-model-v1.1/predictions.json experiment/bert-base-uncased-squad-newsqa-twice-model-v1.1/eval_result


# newsqa_singleSynonymQuestions_0.5.json
# 192_32_0.0005_1_0.2_15_newsqa_singleSynonymQuestions_0.5

# RUN NEWSQA SYNONYM 
python run_squad.py --bert_model experiment/bert-base-uncased-squad-model-v1.1/ \
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

# RUN NEWSQA SYNONYM + NMT
python run_squad.py --bert_model experiment/squad_newsqa_synonym_0.5/ \
--do_train \
--do_lower_case \
--train_file data/newsqa/newsqa_pure_nmt_90.json \
--learning_rate 0.0005 \
--vocab_file data/newsqa/vocab.txt \
--num_train_epochs 1 \
--max_seq_length 192 \
--max_query_length 32 \
--warmup_proportion 0.2 \
--max_answer_length 15 \
--train_batch_size 128 \
--output_dir experiment/squad_newsqa_synonym_nmt_0.5

python run_squad.py --bert_model experiment/squad_newsqa_synonym_nmt_0.5 \
 --do_predict --do_lower_case --predict_file data/newsqa/test.json \
 --output_dir experiment/squad_newsqa_synonym_nmt_0.5

python evaluate-v1.1.py data/newsqa/test.json experiment/squad_newsqa_synonym_nmt_0.5/predictions.json experiment/squad_newsqa_synonym_nmt_0.5/eval_result



# filtered newsqa (48k annotations) without squad, + synonym 
python run_squad.py \
--bert_model bert-base-uncased \
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
--train_batch_size 100 \
--output_dir experiment/squad_synonym_0.5

python run_squad.py --bert_model experiment/squad_synonym_0.5 \
 --do_predict --do_lower_case --predict_file data/newsqa/test.json \
 --output_dir experiment/squad_synonym_0.5

python evaluate-v1.1.py data/newsqa/test.json experiment/squad_synonym_0.5/predictions.json experiment/squad_synonym_0.5/eval_result
# {"exact_match": 19.51852725985367, "f1": 32.39225200019528}

# Reason: loss log has not decrease to 0.x, still 1.x for most of them. Running them more would help
python run_squad.py \
--bert_model bert-base-uncased \
--do_train \
--do_lower_case \
--train_file data/newsqa/newsqa_singleSynonymQuestions_0.5.json \
--learning_rate 0.0005 \
--vocab_file data/newsqa/vocab.txt \
--num_train_epochs 2 \
--max_seq_length 192 \
--max_query_length 32 \
--warmup_proportion 0.2 \
--max_answer_length 15 \
--train_batch_size 100 \
--output_dir experiment/squad_synonym_0.5_2epoch

python run_squad.py --bert_model experiment/squad_synonym_0.5_2epoch \
 --do_predict --do_lower_case --predict_file data/newsqa/test.json \
 --output_dir experiment/squad_synonym_0.5_2epoch

python evaluate-v1.1.py data/newsqa/test.json experiment/squad_synonym_0.5_2epoch/predictions.json experiment/squad_synonym_0.5_2epoch/eval_result
# {"exact_match": 27.11824404059476, "f1": 40.56818679118003}

# filtered newsqa (48k annotations) without squad, + nmt 
python run_squad.py \
--bert_model bert-base-uncased \
--do_train \
--do_lower_case \
--train_file data/newsqa/newsqa_pure_nmt_90.json \
--learning_rate 0.0005 \
--vocab_file data/newsqa/vocab.txt \
--num_train_epochs 2 \
--max_seq_length 192 \
--max_query_length 32 \
--warmup_proportion 0.2 \
--max_answer_length 15 \
--train_batch_size 100 \
--output_dir experiment/squad_nmt_0.9

python run_squad.py --bert_model experiment/squad_nmt_0.9 \
 --do_predict --do_lower_case --predict_file data/newsqa/test.json \
 --output_dir experiment/squad_nmt_0.9

python evaluate-v1.1.py data/newsqa/test.json experiment/squad_nmt_0.9/predictions.json experiment/squad_nmt_0.9/eval_result
# {"exact_match": 13.747934859570451, "f1": 26.4738689673313}

# filtered newsqa (48k annotations) without squad, + synonym and nmt
python run_squad.py \
--bert_model experiment/squad_synonym_0.5_2epoch \
--do_train \
--do_lower_case \
--train_file data/newsqa/newsqa_pure_nmt_90.json \
--learning_rate 0.0005 \
--vocab_file data/newsqa/vocab.txt \
--num_train_epochs 1 \
--max_seq_length 192 \
--max_query_length 32 \
--warmup_proportion 0.2 \
--max_answer_length 15 \
--train_batch_size 100 \
--output_dir experiment/squad_synonym_nmt_0.5_0.9



