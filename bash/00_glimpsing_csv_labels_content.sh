#!/bin/bash

arr_pos_label_col=(80 80 80 84 80 80 80 80 80 80)

arr_csv_files_list=(
	'Friday-02-03-2018_TrafficForML_CICFlowMeter.csv'
	'Friday-16-02-2018_TrafficForML_CICFlowMeter.csv'
	'Friday-23-02-2018_TrafficForML_CICFlowMeter.csv'
	'Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv'
	'Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv'
	'Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv'
	'Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv'
	'Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv'
	'Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv'
	'Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv'
)


function f_count_label () {
	for csv_file in ${arr_csv_files_list[@]}; do
		if [ 0 -eq ${1} ]; then
			n_benign=`grep -U $",Benign" ${csv_file} | wc`
			echo "${csv_file} has ${n_benign} benign samples"
		else
			n_attacks=`grep -U -v $",Benign" ${csv_file} | wc`
			echo "${csv_file} has ${n_attacks} attacks samples"
		fi
		#grep -U $",Benign" ${csv_file} | wc
	done
}

function f_show_attacks () {
	i_lab_col_pos=0	
	for csv_file in ${arr_csv_files_list[@]}; do
		pos_label_col=${arr_pos_label_col[${i_lab_col_pos}]}
		echo "attacks list in ${csv_file}:"
		grep -U -v $",Benign" ${csv_file} | cut -d, -f${pos_label_col} | sort -u
		i_lab_col_pos=$(( ${i_lab_col_pos} + 1 ))
	done
}

# f_count_label 0
# f_count_label 1

f_show_attacks
