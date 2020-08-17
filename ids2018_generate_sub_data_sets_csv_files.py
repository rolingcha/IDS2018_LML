# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 18:12:36 2020

@author: Rolando Inglés
"""

import re
import ids2018_utils as idsutils

RETURN_NOT_OK=-1
RETURN_OK=0


global_processing_tags = ('5K', '10K', '25K', '50K', '100K')   

##
# NOTE:
# apart of the filename TYPO, Thuesday-20-02-2018_TrafficForML_CICFlowMeter
# constains more the 80 columns, namely:
#                                       Flow ID,Src IP,Src Port,Dst IP,
# they were removed in order to normalize the file in order to contains
# the same columns than the others CSV files; hence, the following file
# was created and it won't be found on the data-set repository:
#
# Thuesday-20-02-2018_TrafficForML_CICFlowMeter.80cols.csv
#


global_input_files_dict = {
    '00': r'Friday-02-03-2018_TrafficForML_CICFlowMeter.csv',
    '01': r'Friday-16-02-2018_TrafficForML_CICFlowMeter.csv',
    '02': r'Friday-23-02-2018_TrafficForML_CICFlowMeter.csv',
    '03': r'Thuesday-20-02-2018_TrafficForML_CICFlowMeter.80cols.csv',
    '04': r'Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv',
    '05': r'Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv',
    '06': r'Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv',
    '07': r'Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv',
    '08': r'Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv',
    '09': r'Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv'
}

global_labels_dict = {
    '00': {'Benign': {'5K': 235, '10K': 470, '25K': 1174, '50K': 2348, '100K': 4697},
           'Bot': {'5K': 88, '10K': 176, '25K': 441, '50K': 882, '100K': 1763}},
    '01': {'Benign': {'5K': 238, '10K': 375, '25K': 688, '50K': 1376, '100K': 2752},
           'DoS attacks-Hulk': {'5K': 142, '10K': 285, '25K': 711, '50K': 1423, '100K': 2846},
           'DoS attacks-SlowHTTPTest': {'5K': 43, '10K': 86, '25K': 215, '50K': 431, '100K': 862}},
    '02': {'Benign': {'5K': 323, '10K': 646, '25K': 1614, '50K': 3228, '100K': 6456},
           'Brute Force -Web': {'5K': 25, '10K': 50, '25K': 100, '50K': 150, '100K': 200},
           'Brute Force -XSS': {'5K': 10, '10K': 25, '25K': 50, '50K': 75, '100K': 100},
           'SQL Injection': {'5K': 5, '10K': 10, '25K': 20, '50K': 30, '100K': 40}},
    '03': {'Benign': {'5K': 2271, '10K': 4542, '25K': 11354, '50K': 22709, '100K': 45417},
           'DDoS attacks-LOIC-HTTP': {'5K': 177, '10K': 355, '25K': 887, '50K': 1775, '100K': 3550}},
    '04': {'Benign': {'5K': 73, '10K': 147, '25K': 367, '50K': 733, '100K': 1466},
           'Infilteration': {'5K': 29, '10K': 57, '25K': 143, '50K': 287, '100K': 573}},
    '05': {'Benign': {'5K': 307, '10K': 614, '25K': 1534, '50K': 3068, '100K': 6136},
           'DoS attacks-GoldenEye': {'5K': 50, '10K': 100, '25K': 200, '50K': 300, '100K': 400},
           'DoS attacks-Slowloris': {'5K': 25, '10K': 50, '25K': 100, '50K': 150, '100K': 200}},
    '06': {'Benign': {'5K': 323, '10K': 646, '25K': 1614, '50K': 3229, '100K': 6457},
           'Brute Force -Web': {'5K': 25, '10K': 50, '25K': 75, '50K': 100, '100K': 125},
           'Brute Force -XSS': {'5K': 10, '10K': 20, '25K': 30, '50K': 40, '100K': 50},
           'SQL Injection': {'5K': 5, '10K': 10, '25K': 15, '50K': 20, '100K': 25}},
    '07': {'Benign': {'5K': 206, '10K': 411, '25K': 1028, '50K': 2056, '100K': 4113},
           'FTP-BruteForce': {'5K': 60, '10K': 119, '25K': 298, '50K': 596, '100K': 1191},
           'SSH-Bruteforce': {'5K': 58, '10K': 116, '25K': 289, '50K': 578, '100K': 1156}},
    '08': {'Benign': {'5K': 500, '10K': 1000, '25K': 2000, '50K': 3000, '100K': 5000},
           'DDOS attack-HOIC': {'5K': 211, '10K': 423, '25K': 1057, '50K': 2113, '100K': 4226},
           'DDOS attack-LOIC-UDP': {'5K': 25, '10K': 50, '25K': 100, '50K': 150, '100K': 200}},
    '09': {'Benign': {'5K': 168, '10K': 335, '25K': 838, '50K': 1676, '100K': 3352},
           'Infilteration': {'5K': 50, '10K': 100, '25K': 200, '50K': 300, '100K': 424}}
}

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
    
    if not '00' in global_input_files_dict:
        print('key 00 not found on input file dictionary')
        return RETURN_NOT_OK

    # _ric_tmp_input_filename = list(global_processing_dict.keys())[0]
    
    input_filename = global_input_files_dict['00']
    
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
    
    for file_key, file_val in global_input_files_dict.items():
        task_input_tsv_filename = file_val
        
        if not file_key in global_labels_dict:
            continue
        
        processing_labels_dict = global_labels_dict[file_key]
        
        for label_key, label_val in processing_labels_dict.items():
            processing_tags_dict = label_val
            
            if not output_file_tag in processing_tags_dict:
                continue
            
            n_lines_to_cp = processing_tags_dict[output_file_tag]

            n_sent_lines =  cp_lines_by_label(task_output_filename,
                                               task_input_tsv_filename,
                                               label_key,
                                               n_lines_to_cp)
            
            if n_sent_lines == n_lines_to_cp:
                print('OK')
            else:
                print('ERROR: %d != %d, file_key=%s, label_key=%s, label_val=%s'
                      % (n_sent_lines, n_lines_to_cp, file_key, label_key, label_val))
                return RETURN_NOT_OK
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

