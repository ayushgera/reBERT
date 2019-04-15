# reBERT

**Introduction**
This project presents reBERT, a novel architecturefor the task of domain-specific question answering(QA) that integrates query reformulation into bidi-rectional encoder representations from transform-ers (BERT) (Devlin et al., 2018). We build on ex-isting research on the NewsQA dataset with fourcontributions: (1) we evaluate the performance ofBERT, (2) attempt transfer learning with the Stan-ford  Question  Answering  Dataset  (SQuAD),  (3)perform data augmentation with SQuAD, and (4)reformulate  queries  using  single  pass  synonym-based  word  replacement  and  multilingual  neu-ral machine translation.   Our results suggest thatBERT alone performs poorly on NewsQA (F1 =25.7). Transfer learning is found to be more usefulwhen  applied  in  conjunction  with  data  augmen-tation,  providing a 26.5 increase inF1from theplain BERT model.  reBERT does not further im-proveF1when transfer learning and data augmen-tation are used.

**read.py**:
  - This reads the NewsQA dataset (consisting of dataset with story IDs, and zipped CNN stories)
  using pandas dataframes, and converts that into SQuAD's JSON format. This makes it easier to be 
  used as input for BERT, the boilerplate code for which accepts SQuAD format.
  - Some special characters are filtered from the tokens (check regex : REPLACE_WITH_NO_SPACE)
  - Output files (compressed): JSON files are stored in data/newsQA/validated

**reBERT**:
  - Run reBERT with following commands:  
  
  ****Train****  
    python run_reBERT.py --bert_model bert-base-uncased \  
    --do_train \  
    --do_lower_case \  
    --train_file data/newsqa/newsqa_validated_90_91.json \  
    --learning_rate 0.0005 \  
    --num_train_epochs 1 \  
    --max_seq_length 192 \  
    --max_query_length 32 \  
    --warmup_proportion 0.2 \  
    --max_answer_length 15 \  
    --train_batch_size 64 \  
    --output_dir experiment/reBERT  
  
  ****Predict****  
     python run_reBERT.py --bert_model bert-base-uncased \  
     --do_predict --do_lower_case --predict_file data/newsqa/test.json \  
     --output_dir experiment/reBERT  

   ****Evaluate****  
    python evaluate-reBERT.py \  
    data/newsqa/test.json \  
    experiment/reBERT/predictions.json \  
    experiment/reBERT/eval_result  
