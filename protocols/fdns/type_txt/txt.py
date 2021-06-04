#Module to analyze txt-type of fdns dataset.
import protocols.fdns.fdns as fdns

def get_df_txt(path):
    """
    Get a dataframe fdns records txt-type.
    
        :param path: string contains the fdns database txt-type path
        :return df_txt: Dataframe_txt object
    """
    df = fdns.handle.get_df(path, None, ['Date', 'Domain', 'Type', 'Value'], ',')
    df_txt = get_df_values_cleaned(df)
    df_txt.drop(df_txt[(df_txt.Type != 'txt')].index, axis = 0, inplace = True)
    df_txt.drop(['Type'], axis = 1, inplace = True)
    return df_txt


def get_df_values_cleaned(df_txt):
    """
    Get a dataframe without unnecessary characters.
    
        :param df_txt: Dataframe_txt object
        :return df_txt: Dataframe_txt object
    """
    df_txt.dropna()
    df_txt = fdns.handle.get_df_chars_replaced(df_txt, 'Date', 'Date', ['{\"timestamp\":\"', '\"'])
    df_txt = fdns.handle.get_df_timestamp_changed(df_txt, 'Date')
    df_txt = fdns.handle.get_df_chars_replaced(df_txt, 'Domain', 'Domain', ['name:', '\"'])
    df_txt = fdns.handle.get_df_chars_replaced(df_txt, 'Type', 'Type', ['type:', ';', '\"'])
    df_txt = fdns.handle.get_df_chars_replaced(df_txt, 'Value', 'Value', ['value:', '\"'])
    return df_txt


def obtain_domain_expired(df_txt):
    """
    Obtain string contains expired domains.
    
        :param df_txt: Dataframe_txt object
        :return str_dom: string contains domains
    """
    df_txt.loc[df_txt['Value'].str.contains('expired', flags = re.IGNORECASE)]  
    str_dom = df_txt['Domain'].to_string()
    return str_dom


def obtain_server_mail_domain_with_sts_standard(df_txt):
    """
    Obtain string contains mail server domains that use STS standard.
    
        :param df_txt: Dataframe_txt object
        :return str_dom: string contains domains
    """
    df_txt.loc[df_txt['Domain'].str.contains('_mta-sts', flags = re.IGNORECASE)]  
    str_dom = df_txt['Domain'].to_string()
    return str_dom


def get_df_new_values_assigned(df_txt, df_txt_index, value_lst, dictionary):
    """
    Get a dataframe with inserted new value into new attributes dataframe.
    
        :param df_txt: Dataframe_txt object
        :param df_txt_index: int value to get index of dataframe
        :param value_lst: object list which contains value to insert in dataframe
        :param dictionary: dict object which contains default values for each attribute
        :return df_txt: Dataframe_txt object
    """
    key_list = list(dictionary)
    for index, item in enumerate(key_list):
        if not value_lst[index]:
            df_txt.at[df_txt_index, item] = dictionary[item]
        if type(value_lst[index]) != list:
            if value_lst[index]:
                df_txt.at[df_txt_index, item] = value_lst[index].group(0)
            else:
                df_txt.at[df_txt_index, item] = value_lst[index]
    return df_txt