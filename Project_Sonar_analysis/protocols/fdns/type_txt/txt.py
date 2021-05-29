#Module to analyze txt-type of fdns dataset.
import protocols.fdns.fdns as fdns_module


def get_df_txt(path):
    """
    Getting a dataframe fdns records txt-type.
    
        :param path: string contains the fdns database txt-type path
        :return df_txt: Dataframe_txt object
    """
    df = fdns_module.hand_module.get_df(path, None, ['Date', 'Domain', 'Type', 'Value'], ',')
    df_txt = get_df_values_cleaned(df)
    df_txt.drop(df_txt[(df_txt.Type != 'txt')].index, axis=0, inplace=True)
    df_txt.drop(['Type'], axis=1, inplace=True)
    return df_txt


def get_df_values_cleaned(df_txt):
    """
    Getting a dataframe without unnecessary characters.
    
        :param df_txt: Dataframe_txt object
        :return df_txt: Dataframe_txt object
    """
    df_txt.dropna()
    df_txt = fdns_module.hand_module.get_df_chars_replaced(df_txt, 'Date', 'Date', ['{\"timestamp\":\"', '\"'])
    df_txt = fdns_module.hand_module.get_df_timestamp_changed(df_txt, 'Date')
    df_txt = fdns_module.hand_module.get_df_chars_replaced(df_txt, 'Domain', 'Domain', ['name:', '\"'])
    df_txt = fdns_module.hand_module.get_df_chars_replaced(df_txt, 'Type', 'Type', ['type:', ';', '\"'])
    df_txt = fdns_module.hand_module.get_df_chars_replaced(df_txt, 'Value', 'Value', ['value:', '\"'])
    return df_txt


def obtain_domain_expired(df_txt):
    """
    Obtaining string contains expired domains.
    
        :param df_txt: Dataframe_txt object
        :return str_dom: string contains domains
    """
    df_txt.loc[df_txt['Value'].str.contains('expired', flags=re.IGNORECASE)]  
    str_dom = df_txt['Domain'].to_string()
    return str_dom


def obtain_domain_with_mta_sts(df_txt):
    """
    Obtaining string contains domains that use standard MTA-STS.
    
        :param df_txt: Dataframe_txt object
        :return str_dom: string contains domains
    """
    df_txt.loc[df_txt['Domain'].str.contains('_mta-sts', flags=re.IGNORECASE)]  
    str_dom = df_txt['Domain'].to_string()
    return str_dom