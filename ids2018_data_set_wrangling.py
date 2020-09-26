# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 22:12:06 2020

@author: Rolando Inglés
"""
import pandas as pd

# UNSW-NB15 specific imports
import ids2018_utils as idsutils

##
# features descriptions:
# https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/NUSW-NB15_features.csv
#
ids2018_all_columns = [
    'Dst Port',
    'Protocol',
    'Flow Duration',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts',
    'TotLen Fwd Pkts',
    'TotLen Bwd Pkts',
    'Flow Byts/s',
    'Flow Pkts/s',
    'Fwd PSH Flags',
    'Bwd PSH Flags',
    'Fwd URG Flags',
    'Bwd URG Flags',
    'Fwd Header Len',
    'Bwd Header Len',
    'Fwd Pkts/s',
    'Bwd Pkts/s',
    'FIN Flag Cnt',
    'SYN Flag Cnt',
    'RST Flag Cnt',
    'PSH Flag Cnt',
    'ACK Flag Cnt',
    'URG Flag Cnt',
    'CWE Flag Count',
    'ECE Flag Cnt',
    'Down/Up Ratio',
    'Init Fwd Win Byts',
    'Init Bwd Win Byts',
    'Fwd Act Data Pkts',
    'Fwd Seg Size Min',
    'Label'
]

ids2018_X_selected_columns = [
    'Dst Port',
    'Protocol',
    'Flow Duration',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts',
    'TotLen Fwd Pkts',
    'TotLen Bwd Pkts',
    'Flow Byts/s',
    'Flow Pkts/s',
    'Fwd PSH Flags',
    'Bwd PSH Flags',
    'Fwd URG Flags',
    'Bwd URG Flags',
    'Fwd Header Len',
    'Bwd Header Len',
    'Fwd Pkts/s',
    'Bwd Pkts/s',
    'FIN Flag Cnt',
    'SYN Flag Cnt',
    'RST Flag Cnt',
    'PSH Flag Cnt',
    'ACK Flag Cnt',
    'URG Flag Cnt',
    'CWE Flag Count',
    'ECE Flag Cnt',
    'Down/Up Ratio',
    'Init Fwd Win Byts',
    'Init Bwd Win Byts',
    'Fwd Act Data Pkts',
    'Fwd Seg Size Min'
]

ids2018_y_selected_columns = [
    'Label'
]

iot_23_X_selected_scalars_columns = [
    'Flow Duration',
    'Tot Fwd Pkts',
    'Tot Bwd Pkts',
    'TotLen Fwd Pkts',
    'TotLen Bwd Pkts',
    'Flow Byts/s',
    'Flow Pkts/s',
    'Fwd PSH Flags',
    'Bwd PSH Flags',
    'Fwd URG Flags',
    'Bwd URG Flags',
    'Fwd Header Len',
    'Bwd Header Len',
    'Fwd Pkts/s',
    'Bwd Pkts/s',
    'FIN Flag Cnt',
    'SYN Flag Cnt',
    'RST Flag Cnt',
    'PSH Flag Cnt',
    'ACK Flag Cnt',
    'URG Flag Cnt',
    'CWE Flag Count',
    'ECE Flag Cnt',
    'Down/Up Ratio',
    'Init Fwd Win Byts',
    'Init Bwd Win Byts',
    'Fwd Act Data Pkts',
    'Fwd Seg Size Min'
]

##
# @name get_data_set
#
# Objective: open CSV file based on the tag and return a dataframe object
#
# Parameters: The tag: 5K 10K 25K 50K 100K 
#
# Returns: raw_X    dataframe to be used as X_train
#           raw_y   dataframe to be used as y_train 
#   
def get_X_raw_y_raw(data_set_tag='notag'):
    data_set_input_filename = idsutils.get_ids2018_output_filename(data_set_tag)
    
    # NOTE: 80 features are loaded
    raw_data_set_df = pd.read_csv(data_set_input_filename)
    
    raw_X = raw_data_set_df.filter(items=ids2018_X_selected_columns)
    raw_y = raw_data_set_df.filter(items=ids2018_y_selected_columns)
    
    return raw_X, raw_y

##
# @name get_wrangled_scalars
#
# Objective:    Munging columns with scalar content from the passed UNSW-NB15 
#               raw data frame
#
# Parameters:
#               raw_df - the dataframe containing the raw column data
#                           to be wrangled
#
# Returns:      scalars_df - the dataframe containing the wrangled
#                               'scalars' columns data
#                               
def get_wrangled_scalars(raw_df=None): 
    scalars_df = raw_df.filter(items=iot_23_X_selected_scalars_columns)
    
    return scalars_df
    
##
# @name get_wrangled_Dst Port
#
# Objective:    Munging the 'Dst Port' column from the passed UNSW_NB15 
#               raw data frame
#
# Parameters:
#               raw_df - the dataframe containing the raw column data
#                           to be wrangled
#
# Returns:      Dst_Port_df - the dataframe containing the wrangled
#                               'Dst Port' column data
#                   
def get_ohe_from_Dst_Port(raw_df=None):
    #
    # based on: https://tools.ietf.org/html/rfc1340
    
    Dst_Port_df = raw_df[['Dst Port']].copy()
    
    Dst_Port_df.loc[:, '_Dst_Port_'] = Dst_Port_df.loc[:, 'Dst Port']
    
    # RFC1340: The Registered Ports are in the range 1024-65535
    Dst_Port_df.loc[:, ('Dst Port')] = 'gt_65535'
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ < 65536, 'Dst Port'] = '1024_65535'
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ < 1024, 'Dst Port'] = 'lt_1024'
    
    # reserved
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 0, 'Dst Port'] = 'reserved'
    
    # ssh
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 22, 'Dst Port'] = 'ssh'
    
    # telnet
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 23, 'Dst Port'] = 'telnet'
    
    # smtp
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 25, 'Dst Port'] = 'smtp'
    
    # Message Processing Module [recv]
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 45, 'Dst Port'] = 'mpm'
    
    # Domain Name Server
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 53, 'Dst Port'] = 'dns'
    
    # World Wide Web HTTP 
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 80, 'Dst Port'] = 'http_80'
    
    # sunrpc
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 111, 'Dst Port'] = 'sunrpc'
    
    # ntp
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 123, 'Dst Port'] = 'ntp'
    
    # imap2
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 143, 'Dst Port'] = 'imap2'
    
    # bgp
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 179, 'Dst Port'] = 'bgp'
    
     # https
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 443, 'Dst Port'] = 'https'
    
     # mdqs
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 666, 'Dst Port'] = 'mdqs'
    
    # messenger
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 5190, 'Dst Port'] = 'messenger'
    
    # bittorrent
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 6881, 'Dst Port'] = 'bittorrent'
    
    # World Wide Web HTTP 
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 8080, 'Dst Port'] = 'http_8080'
    
    # World Wide Web HTTP 
    Dst_Port_df.loc[Dst_Port_df._Dst_Port_ == 8081, 'Dst Port'] = 'http_8081'
    
    Dst_Port_df = pd.concat([Dst_Port_df, pd.get_dummies(Dst_Port_df['Dst Port'], prefix='Dst Port')], axis=1)
    Dst_Port_df.drop(['Dst Port'], axis=1, inplace=True)
    Dst_Port_df.drop(['_Dst_Port_'], axis=1, inplace=True)
    
    return Dst_Port_df

##
# @name get_wrangled_proto
#
# Objective:    Munging the 'proto' column from the passed UNSW-NB15 
#               raw data frame
#
# Parameters:
#               raw_df - the dataframe containing the raw column data
#                           to be wrangled
#
# Returns:      proto_df - the dataframe containing the wrangled
#                               'proto' column data
#                               
def get_ohe_from_protocol(raw_df=None):
    
    # 
    # based on: https://tools.ietf.org/html/rfc1340
    
    protocol_df = raw_df[['Protocol']].copy()
    
    protocol_df.loc[:, '_protocol_'] = 'other'
    
    # 0                 Reserved
    protocol_df.loc[protocol_df.Protocol == 0, '_protocol_'] = 'reserved'
    
    # 6     TCP         Transmission Control
    protocol_df.loc[protocol_df.Protocol == 6, '_protocol_'] = 'tcp'
    
    # 17     UDP         User Datagram 
    protocol_df.loc[protocol_df.Protocol == 17, '_protocol_'] = 'udp'
    
    protocol_df = pd.get_dummies(protocol_df['_protocol_'], prefix='protocol')
    
    return protocol_df

##
# @name get_wrangled_column
#
# Objective: having opened the data set source file, filtering the column
#               base on the column_name parameter, then the munging process
#               is performed over the filtered column data 
#
# Parameters: 
#               raw_df - dataframe containing the raw column data from where
#                        the munging data will be performed
#               column_name - the name of the column  
#
# Returns: dataframe 
#   
def get_wrangled_column(raw_df=None, column_name='__no_name__'):
    if 'scalars' == column_name:
        return get_wrangled_scalars(raw_df)
    elif 'Dst Port' == column_name:
         return get_ohe_from_Dst_Port(raw_df)
    elif 'Protocol' == column_name:
         return get_ohe_from_protocol(raw_df)
   
    print('{} is an unrecognized value for column_name parameter'.format(column_name))
    return None

##
#  __main__
if __name__ == '__main__':
    print("it's a library, please use it by importing")