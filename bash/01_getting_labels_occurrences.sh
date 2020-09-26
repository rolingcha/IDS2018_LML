#!/bin/bash

arr_has_CRNL=( 1 0 0 1 0 0 0 0 0 0 )
arr_label_col_pos=( 80 80 80 84 80 80 80 80 80 80 )

arr_csv_list=(
        Friday-02-03-2018_TrafficForML_CICFlowMeter.csv
        Friday-16-02-2018_TrafficForML_CICFlowMeter.csv
        Friday-23-02-2018_TrafficForML_CICFlowMeter.csv
        Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv
        Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv
        Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv
        Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv
        Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv
        Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv
        Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv
    )

i_csv_list=0
for curr_csv_file in "${arr_csv_list[@]}"
do
    echo "processing,${curr_csv_file}"
    n_total=`cat ${curr_csv_file} | wc -l`
    echo "total rows,${n_total}"
    cut -d, -f ${arr_label_col_pos[$i_csv_list]} ${curr_csv_file} > /tmp/cut.output
    if [ "1" -eq "${arr_has_CRNL[$i_csv_list]}" ]
    then
        sed -i 's/\r$//g' /tmp/cut.output
    fi
    while read -r curr_label
    do
        n_label_occurrences=`grep "${curr_label}" /tmp/cut.output | wc -l`
        echo ${curr_label},${n_label_occurrences}
    done < <(sort -u /tmp/cut.output)
    i_csv_list=$((i_csv_list+1))
done
