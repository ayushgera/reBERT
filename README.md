# pyTorch_NN

**NewsQA to SQuAD adaptor**:
  - This reads the NewsQA dataset (consisting of dataset with story IDs, and zipped CNN stories)
  using pandas dataframes, and converts that into SQuAD's JSON format. This makes it easier to be 
  used as input for BERT, the boilerplate code for which accepts SQuAD format.
  - Some special characters are filtered from the tokens (check regex : REPLACE_WITH_NO_SPACE)
  - Output files (compressed): 
    newsQaJSONSquadFormat.json --> generated from complete dataset (not tested yet, might be corrupt- CHECK!)
    newsQaJSONSquadFormat_5000.json --> generated from first 5000 entries in the NewsQA csv.
  
