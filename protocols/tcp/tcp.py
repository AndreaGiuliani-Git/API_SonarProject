#Module to handle tcp dataset.
import protocols.handling as hand_module

def get_df_tcp(path):
    """
    Get a dataframe tcp records.
    
        :param path: string contains the tcp database path
        :return df_tcp: Dataframe_tcp object
    """
    #df = hand_module.get_df(path, 'gzip', ['Date', 'S_address', 'S_port', 'D_address', 'D_port', 'I_pid', 'Time_to_live'], ',')
    df = hand_module.get_df(path, None, ['Date', 'S_address', 'S_port', 'D_address', 'D_port', 'I_pid', 'Time_to_live'], ',')
    df_tcp = hand_module.get_df_invalid_ip_removed(df, 'S_address')
    df_tcp = hand_module.get_df_invalid_ip_removed(df_tcp, 'D_address')
    df_tcp = hand_module.get_df_timestamp_changed(df_tcp, 'Date')
    return df_tcp
   
    
def get_df_ip_selected(df, ip_attr, ip_address_list, result_type):
    """
    Get a dataframe which contains all ip-address matched in "Ip" attribute in the dataframe.
    The "result_type" value must be 0 or 1.
    0 = getting dataframe with all attributes from df_tcp.
    1 = getting dataframe with only "S_address" and "S_port" attributes from df_tcp.
    
        :param df: Dataframe object
        :param ip_attr: string contains the attribute name 
        :param ip_address_list: string list contains the ip-address to search
        :param result_type: int value to choose output
        :return df_final: DataFrame object 
    """
    df_final = hand_module.pd.DataFrame()
    for i in ip_address_list:
        df_ip_searched = hand_module.get_df_rows_filtered(df, ip_attr, i, False, 0)
        df_final = df_final.append(df_ip_searched, ignore_index = True)
    if result_type:
        df_final.drop(['Date', 'D_address', 'D_port', 'I_pid', 'Time_to_live'], axis = 1, inplace = True)        
    return df_final

    