#Module to manage ip-addresses
import ipaddress
import pandas as pd

def find_ip_in_network(ip_list, network):
    """
    Find all ip-address inside the specified network in ip_list.
    
        :param ip_list: string list contains ip-addresses
        :param network: string contains the network address
        :return boolean_list: List object
    """ 
    boolean_list = []
    for i in ip_list:
        if i in ipaddress.ip_network(network):
            boolean_list.append(True)
        else:
            boolean_list.append(False)
    return boolean_list
    
    
def get_df_ip_info_collected(ip_list):
    """
    Get a dataframe with some information about ip-addresses. More information at 
    the link: https://docs.python.org/3/library/ipaddress.html.
    
        :param ip_list: string list contains ip-addresses
        :return df_ip_info: DataFrame object
    """
    df_ip_info = pd.DataFrame( columns = ['Ip', 'Multicast', 'Private', 'Global', 'Reserved', 'Loopback', 'Link_local'])
    df_ip_info['Ip'] = ip_list
    for index, item in enumerate(df_ip_info['Ip']):
            df_ip_info.iat[index, df_ip_info.columns.get_loc('Multicast')] = ipaddress.is_multicast(item)
            df_ip_info.iat[index, df_ip_info.columns.get_loc('Private')] = ipaddress.is_private(item)
            df_ip_info.iat[index, df_ip_info.columns.get_loc('Global')] = ipaddress.is_global(item)
            df_ip_info.iat[index, df_ip_info.columns.get_loc('Reserved')] = ipaddress.is_reserved(item)
            df_ip_info.iat[index, df_ip_info.columns.get_loc('Loopback')] = ipaddress.is_loopback(item)
            df_ip_info.iat[index, df_ip_info.columns.get_loc('Link_local')] = ipaddress.is_link_local(item)
    return df_ip_info