# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:50:59 2020

@author: Rolando Inglés

"""
import numpy as np
import pandas as pd

import ids2018_utils as idsutils

# %% definitions
IDS2018_selected_columns = ['Dst Port',
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
                                      'Label']


def get_data_set(data_set_tag='notag'):
    data_set_input_filename = idsutils.get_ids2018_output_filename(data_set_tag)
    
    # NOTE: 80 features are loaded
    raw_data_set_df = pd.read_csv(data_set_input_filename)
    processing_df = raw_data_set_df.filter(items=IDS2018_selected_columns)
    
# =============================================================================
#    _ric_just_checking_
#     proba_np_arr = data_set_df.iloc[:,1:-1].to_numpy()
#     i_j_NaN_coords_tuple = np.where(np.isnan(proba_np_arr))
#     print(i_j_NaN_coords_tuple[0].shape)
#     proba_np_arr_no_nan = np.delete(proba_np_arr, i_j_NaN_coords_tuple[0], axis=0)
# 
# =============================================================================
    # Cleaning >>> inf <<<
    processing_df = processing_df.replace([np.inf, -np.inf], np.nan)
    
    # Cleaning >>> Infinity <<<
    processing_df = processing_df[~processing_df.isin(['Infinity'])]
    processing_df = processing_df.dropna()

    #i_j_max_floats_coords = np.where(X.values >= np.finfo(np.float64).max)
    #X.drop(index=i_j_max_floats_coords[0])
    
    return processing_df        

# %% __main__
if __name__ == '__main__':
    print("it's a library, just for importing")

