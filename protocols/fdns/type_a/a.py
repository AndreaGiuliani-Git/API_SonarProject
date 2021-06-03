#Module to analyze a-type of fdns dataset
import protocols.fdns.fdns as fdns_module

def get_df_a(path):
    """
    Get a dataframe fdns records a-type.
        
        :param path: string contains the fdns database a-type path
        :return df_a: Dataframe_a object
    """
    df = fdns_module.hand_module.get_df(path, None, ['Date', 'Domain', 'Type', 'Value'], ',')
    df_a = get_df_values_cleaned(df)
    df_a = fdns_module.hand_module.get_df_attribute_renamed(df_a, 'Value', 'Ip')
    df_a = fdns_module.hand_module.get_df_chars_replaced(df_a, 'Ip', 'Ip', ["\"value\":\"", "}"])
    df_a.drop(df_a[(df_a.Type != 'a')].index, inplace=True)
    df_a.drop(['Type'], axis=1, inplace = True)
    df_a.reset_index()
    df_a = fdns_module.hand_module.get_df_invalid_ip_removed(df_a, 'Ip')
    return df_a


def get_df_values_cleaned(df_txt):
    """
    Get a dataframe without unnecessary characters.
    
        :param df_txt: Dataframe_a object
        :return df_a: Dataframe_a object
    """
    df_txt.dropna()
    df_a = fdns_module.hand_module.get_df_chars_replaced(df_txt, 'Date', 'Date', ['{\"timestamp\":\"', '\"'])
    df_a = fdns_module.hand_module.get_df_timestamp_changed(df_a, 'Date')
    df_a = fdns_module.hand_module.get_df_chars_replaced(df_a, 'Domain', 'Domain', ['name:', '\"'])
    df_a = fdns_module.hand_module.get_df_chars_replaced(df_a, 'Type', 'Type', ['type:', ';', '\"'])
    df_a = fdns_module.hand_module.get_df_chars_replaced(df_a, 'Value', 'Value', ['value:', '\"'])
    return df_a


def get_df_ip_freq_grouped_by_country(df, df_ip_loc):
    """
    Get a dataframe which contains grouped rows by country and counted ip frequency.

        :param df: DataFrame object
        :param df_ip_loc: Dataframe_ip_loc object
        :return df_complete_group: Dataframe_complete object
    """
    df_complete = fdns_module.hand_module.get_df_attributes_merged(df, df_ip_loc, 'Ip', 'Ip', 'inner')
    df_complete_group = fdns_module.hand_module.get_df_attributes_grouped_by(df_complete, ['Country'], 'Ip', 'Ip')
    return df_complete_group


def get_df_subdomain_freq_grouped_by_ip(df, df_ip_loc):
    """
    Get a dataframe which contains grouped rows by ip-address and counted subdomains frequency.

        :param df: DataFrame object
        :param df_ip_loc: Dataframe_ip_loc object
        :return df_complete_group: Dataframe_complete object
    """
    df_complete = fdns_module.hand_module.get_df_attributes_merged(df, df_ip_loc, 'Ip', 'Ip', 'inner')
    df_complete_group = fdns_module.hand_module.get_df_attributes_grouped_by(df_complete, ['Ip'], 'Domain', 'Domain')
    return df_complete_group


def get_df_ip_freq_grouped_by_subdivisions(df, df_ip_loc):
    """
    Get a dataframe which contains grouped rows by ip-address and counted subdomains frequency.

        :param df: DataFrame object
        :param df_ip_loc: Dataframe_ip_loc object
        :return df_complete_group: Dataframe_complete object
    """
    df_complete = fdns_module.hand_module.get_df_attributes_merged(df, df_ip_loc, 'Ip', 'Ip', 'inner')
    df_complete_group = fdns_module.hand_module.get_df_attributes_grouped_by(df_complete, ['Subdivisions'], 'Ip', 'Ip')
    return df_complete_group


def get_df_ip_selected(df, ip_address_list):
    """
    Get a dataframe which contains all ip-address matched in "Ip" attribute in the dataframe.
    
        :param df: Dataframe object
        :param ip_address_list: string list contains the ip-address to search
        :return df_final: DataFrame object 
    """
    df_final = hand_module.pd.DataFrame()
    for i in ip_address_list:   
        df_ip_searched = hand_module.get_df_rows_filtered(df, 'Ip', i, False, 0)
        df_final = df_final.append(df_ip_searched, ignore_index = True)
    return df_final


def obtain_common_subdomain(subdomain_list):
    """
    Obtain a most common subdomain list.

        :param subdomain_list: string list which contains most common subdomains
        :return most_com_sub: list of most common subdomain names
    """
    list_container = []
    counter_list = []
    count = 0
    most_com_sub = []
    for i in subdomain_list:
        list_container.append(i.split("."))    
    for i in list_container:
        not_in = 0
        for j in i:
            if count == 0:
                t = [j, 0]
                counter_list.append(t)
            else:
                for counter in counter_list:
                    if j == counter[0]:
                        counter[1] += 1
                        not_in += 1
                if not_in == 0:
                    t = [j, 0]
                    counter_list.append(t)
        count += 1
    max_times = counter_list[0][1]
    for i in counter_list:
        if i[1] > max_times:
            max_times = i[1]
        elif i[1] == max_times:
            most_com_sub.append(i[0])
    return most_com_sub