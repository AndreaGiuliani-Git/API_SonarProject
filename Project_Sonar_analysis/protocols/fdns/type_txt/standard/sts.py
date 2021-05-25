#Module to analyze sts standard of txt-type records.
import protocols.fdns.type_txt.txt as txt_module

 
def get_df_sts(path):
    """
    Getting a dataframe fdns records txt-type with sts standard.
    
        :param path: string contains the FDNS-TXT database path
        :return df_sts: Dataframe_sts object
    """
    df_txt = txt_module.get_df_txt(path)
    df_sts = txt_module.fdns_module.hand_module.get_df_rows_filtered(df_txt, 'Value', 'STSv1', False, 1)
    df_sts = txt_module.fdns_module.hand_module.get_df_attribute_renamed(df_sts, 'Value', 'Id') 
    df_sts = txt_module.fdns_module.hand_module.get_df_string_extracted(df_sts, 'Id', 'Id', 'id=', '', 0)
    df_sts = txt_module.fdns_module.hand_module.get_df_chars_replaced(df_sts, 'Id', 'Id', [';', '}'])
    return df_sts