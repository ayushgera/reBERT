import json
import sys
import math

global training_json_data
global dev_json_data
global test_json_data
global total_training_length

def split_data(training_set_size,
        dev_set_size,
        test_set_size):

    base_input_path = './output/complete/'
    base_output_path = './output/splitData/'
    
    training_input_filename = 'newsQaJSONSquadFormat_oneanswer_uniqueID.json'
    test_input_filename = 'newsQaJSONSquadFormat_multipleAnswers_uniqueID.json'
    
    training_output_filename = 'training_'+training_set_size+'.json'
    dev_output_filename = 'dev_'+dev_set_size+'.json'
    test_output_filename = 'test_'+test_set_size+'.json'

    training_set_size = int(training_set_size)
    dev_set_size = int(dev_set_size)
    test_set_size = int(test_set_size)

    global training_json_data
    global dev_json_data
    global test_json_data

    # load training data
    # according to read_newsqa.py script
    # training/dev data can not have multiple answers
    # use newsQaJSONSquadFormat_complete_oneanswer
    with open(base_input_path + training_input_filename,
            'r') as training_input_json:
        global total_training_length
        training_data= json.load(training_input_json)['data']
        data_length = len(training_data)
        total_training_length = math.floor(data_length * (training_set_size + dev_set_size) / 100)
        training_data_length = math.floor(data_length * (training_set_size)/100)
        dev_data_length = math.floor(data_length * (dev_set_size) / 100)

        global training_json_data
        global dev_json_data

        training_json_data = training_data[:training_data_length]
        dev_json_data = training_data[training_data_length:training_data_length+dev_data_length-1]
        print("training data length: ",len(training_json_data))
        print("dev data length: ",len(dev_json_data))
        training_input_json.close()

    # load test data
    # according to read_newsqa.py script
    # test data is allowed to have multiple answers
    # use newsQaJSONSquadFormat_complete_multipleAnswers
    with open(base_input_path + test_input_filename,
            'r') as test_input_json:

        test_json_data = json.load(test_input_json)['data'][total_training_length:]
        print("test data length: ",len(test_json_data))
        test_input_json.close()

    # Create new JSON File
    with open(base_output_path + training_output_filename,
            'w') as f:
        training = {}
        training['data'] = training_json_data
        json.dump(training, f, ensure_ascii=False)
        f.close()
    # Create new JSON File
    with open(base_output_path + dev_output_filename,
            'w') as f:
        dev = {}
        dev['data'] = dev_json_data
        json.dump(dev, f, ensure_ascii=False)
        f.close()
    # Create new JSON File
    with open(base_output_path + test_output_filename,
            'w') as f:
        test = {}
        test['data'] = test_json_data
        json.dump(test, f, ensure_ascii=False)
        f.close()

if __name__ == "__main__":
    # make no changes here
    training_set_size = sys.argv[1]
    dev_set_size = sys.argv[2]
    test_set_size = sys.argv[3]
    split_data(training_set_size, dev_set_size, test_set_size)
