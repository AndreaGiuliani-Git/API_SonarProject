#Module to handle fdns dataset.
import protocols.handling as handle

def get_df_hostname_specified(df, host_name):
    """
    Get a dataframe with only rows which domains end with host_name in the dataframe.
    
        :param df: Dataframe object
        :param host_name: string contains the complete host name
        :return df_final: Dataframe object
    """
    df_final = handle.pd.DataFrame()
    df_final = df[df['Domain'].str.endswith(host_name)]
    return df_final