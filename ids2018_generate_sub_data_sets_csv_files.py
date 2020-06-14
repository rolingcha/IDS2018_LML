# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:51:28 2020

@author: Rolando Inglés
"""

import re
import ids2018_utils as idsutils

RETURN_NOT_OK=-1
RETURN_OK=0

_ric_global_processing_dict = {
	'rolingcha.csv' : 
        {'5K': {'Benign': 2, 'DoS attacks-Hulk': 2, 
                'DoS attacks-SlowHTTPTest': 2}},
}

global_processing_tags = ('5K', '10K')   

global_processing_dict = {
    'Friday-02-03-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 235,
                'Bot': 88},
         '10K': {'Benign': 470,
                 'Bot': 176}},
	'Friday-16-02-2018_TrafficForML_CICFlowMeter.csv' : 
        {'5K': {'Benign': 238, 
                'DoS attacks-Hulk': 142, 
                'DoS attacks-SlowHTTPTest': 43},
         '10K': {'Benign': 375,
                 'DoS attacks-Hulk': 285,
                 'DoS attacks-SlowHTTPTest': 86}},
	'Friday-23-02-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 323,
                'Brute Force -Web': 25, 
                'Brute Force -XSS': 10 ,
                'SQL Injection': 5},
         '10K': {'Benign': 646,
                 'Brute Force -Web': 50,
                 'Brute Force -XSS': 25 ,
                 'SQL Injection': 10}},
	'Thuesday-20-02-2018_TrafficForML_CICFlowMeter.80cols.csv' :
        {'5K': {'Benign': 2271,
                'DDoS attacks-LOIC-HTTP': 177},
         '10K': {'Benign': 4542,
                'DDoS attacks-LOIC-HTTP': 355}},
	'Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 73,
                'Infilteration': 29},
         '10K': {'Benign': 147,
                'Infilteration': 57}},
	'Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 307, 
                'DoS attacks-GoldenEye': 50,
                'DoS attacks-Slowloris': 25},
         '10K': {'Benign': 614, 
                'DoS attacks-GoldenEye': 100,
                'DoS attacks-Slowloris': 50}},
	'Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 323, 
                'Brute Force -Web': 25,
                'Brute Force -XSS': 10,
                'SQL Injection': 5},
         '10K': {'Benign': 646, 
                'Brute Force -Web': 50,
                'Brute Force -XSS': 20,
                'SQL Injection': 10}},
	'Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 206, 
                'FTP-BruteForce': 60,
                'SSH-Bruteforce': 58},
         '10K': {'Benign': 411, 
                'FTP-BruteForce': 119,
                'SSH-Bruteforce': 116}},
	'Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 500, 
                'DDOS attack-HOIC': 211,
                'DDOS attack-LOIC-UDP': 25},
         '10K': {'Benign': 1000, 
                'DDOS attack-HOIC': 423,
                'DDOS attack-LOIC-UDP': 50}},
	'Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv' :
        {'5K': {'Benign': 168,
                'Infilteration': 50},
         '10K': {'Benign': 335,
                'Infilteration': 100}},
    }

##
# @name clean_output_files
#
# Objective: cleaning up all the file previously generated
#
# params: None
#
def clean_output_files():
    # to be done
    print("to be done")


##
# @name get_rows_by_label_into_output_file
#
# Objective: cleaning up all the file previously generated
#
# Parameters: None
#
# Returns:
#
def cp_lines_by_label(output_filename="output.csv",
                      input_filename='input.csv', 
                      label_to_get='nolabel',
                      n_lines_to_cp=0):
    print('copying %d %s\'s lines into %s' % 
          (n_lines_to_cp, label_to_get, output_filename))

    line_cnt = 0
                # e.g. ,Benign$
    
    reg_expr =  ','+label_to_get.replace(' ', r'\s')+'$'
    #reg_expr = reg_expr.replace(' ', r'\s')
 
    with open(output_filename, 'a') as csv_output_file:
        with open(input_filename) as csv_input_file:
            for input_line in csv_input_file:
                if re.search(reg_expr, input_line):
                    csv_output_file.write(input_line)
                    line_cnt += 1
                    if line_cnt == n_lines_to_cp:
                        return line_cnt

    return line_cnt

##
# @name generate_train_test_sets
#
# Objective: cleaning up all the file previously generated
#
# Parameters: None
#
# Returns:
#
def copy_header_into_output_csv(output_filename="nofilename"):
    # taking the features names (HEADER) from the very first
    # input file declared in the processing dictionary
    
    input_filename = list(global_processing_dict.keys())[0]
    
    with open(output_filename, 'w') as csv_output_file:
        with open(input_filename, 'r') as csv_input_file:
            csv_output_file.write(csv_input_file.readline())

    return RETURN_OK
    
##
# @name generate_train_test_sets
#
# Objective: cleaning up all the file previously generated
#
# Parameters: None
#
# Returns:
#
def generate_train_test_sets(output_file_tag="notag"):
    
    task_output_filename = idsutils.get_ids2018_output_filename(output_file_tag)
    
    # creating or truncating file by copying the features header
    if copy_header_into_output_csv(task_output_filename) == RETURN_NOT_OK:
        return RETURN_NOT_OK

    # samples    
    for global_processing_task in global_processing_dict.items():
        task_input_csv_filename = global_processing_task[0]
        
        if not output_file_tag in global_processing_task[1]:
            continue
            
        processing_task_dict = global_processing_task[1][output_file_tag]
        
        print('Processing:', task_input_csv_filename)
        for curr_task_tuple in processing_task_dict.items():
            label_to_get = curr_task_tuple[0]
            n_lines_to_cp = curr_task_tuple[1]
            n_sent_lines =  cp_lines_by_label(task_output_filename,
                                               task_input_csv_filename,
                                               label_to_get,
                                               n_lines_to_cp)
            
            if n_sent_lines == n_lines_to_cp:
                print('OK')
            else:
                print('ERROR')
                return RETURN_NOT_OK()
    
    return RETURN_OK            
            
##
# @name clean_output_files
#
# Objective: cleaning up all the file previously generated
#
# Parameters: None
#
# Returns:
#
def main():
    for output_file_tag in global_processing_tags:
        if RETURN_OK == generate_train_test_sets(output_file_tag):
            print('done!')
                
if __name__ == "__main__":
    main()

