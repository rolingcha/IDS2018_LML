#!/bin/bash

declare -a arr_attacks_list=(
	"Bot"
	"DoS attacks-Hulk"
	"DoS attacks-SlowHTTPTest"
	"Brute Force -Web"
	"Brute Force -XSS"
	"SQL Injection"
	"DDoS attacks-LOIC-HTTP"
	"Infilteration"
	"DoS attacks-GoldenEye"
	"DoS attacks-Slowloris"
	"Brute Force -Web"
	"Brute Force -XSS"
	"SQL Injection"
	"FTP-BruteForce"
	"SSH-Bruteforce"
	"DDOS attack-HOIC"
	"DDOS attack-LOIC-UDP"
	"Infilteration"
)

arr_csv_list=(
	Friday-02-03-2018_TrafficForML_CICFlowMeter.csv
	Friday-16-02-2018_TrafficForML_CICFlowMeter.csv
	Friday-16-02-2018_TrafficForML_CICFlowMeter.csv
 	Friday-23-02-2018_TrafficForML_CICFlowMeter.csv
 	Friday-23-02-2018_TrafficForML_CICFlowMeter.csv
 	Friday-23-02-2018_TrafficForML_CICFlowMeter.csv
 	Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv
 	Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv
	Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv
 	Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv
 	Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv
 	Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv
 	Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv
 	Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv
 	Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv
 	Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv
 	Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv
 	Wednesday-28-02-2018_TrafficForML_CICFlowMeter.csv
)

i_csv_list=0
for attack_label in "${arr_attacks_list[@]}"; do
	n_attack_samples=`grep -U $",$attack_label" ${arr_csv_list[$i_csv_list]} | wc -l`
	echo "there are ${n_attack_samples} of ${attack_label} attack in ${arr_csv_list[$i_csv_list]}"
	i_csv_list=$((i_csv_list+1))
done
