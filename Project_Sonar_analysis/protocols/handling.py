#Module to handle Project Sonar dataset.
import pandas as pd
import math
import re
import json
import ipaddress
import maxminddb as mx
from ipyleaflet import Map, Marker, basemaps, FullScreenControl, MeasureControl
pd.options.mode.chained_assignment = None

def get_df(path, type_compression, str_arr, sepa):
    """
    Getting dataframe from dataset through its path.

        :param path: string contains the path of the dataset
        :param type_compression: string contains the compression type
        :param str_arr: strings array contains the columns name
        :param sepa: character contains attributes separator
        :return df: DataFrame object
    """
    df = pd.read_csv(path, compression = type_compression, header = None, names = str_arr, sep = sepa)
    return df


def get_df_chars_replaced(df, attr1, attr2, str_arr):
    """
    Getting a dataframe with a target attribute obtained from replacing specific characters by a source attribute.
    
        :param df: DataFrame object
        :param attr1: string contains the source attribute 
        :param attr2: string contains the target attribute
        :param str_arr: strings array contains expressions to delete
        :return df: DataFrame object
    """
    df[attr2] = df[attr1].replace(str_arr, '', regex = True)
    return df


def get_df_string_extracted(df, attr1, attr2, prev_str, next_str, flag):
    """
    Getting a dataframe with a target attribute obtained by extracting specific string in a source attribute.The flag
    value must be 0 or 1.
    0 = extract with previous string
    1 = extract with previous and next string
    
        :param df: DataFrame object
        :param attr1: string contains the source attribute 
        :param attr2: string contains the target attribute
        :param prev_str: string contains the preceding expressions to the substring to extract
        :param next_str: string contains the next expressions to the substring to extract
        :param flag: int value to indicate one of two extraction mode
        :return df: DataFrame object
    """
    if not flag:
        df[attr2] = df[attr1].str.extract(prev_str + "(\S+)")
    else:
        df[attr2] = df[attr1].str.extract("(?<=" + prev_str + ")" + "(.*?)" + "(?=" + next_str + ")")
    return df


def find_string(pattern, string):
    """
    Finding a pattern in a string.
    
        :param pattern: string to search for
        :param string: string where to search
        :return tmp: value 0 or 1
    """
    if pattern in string:
        tmp = 1
    else:
        tmp = 0
    return tmp


def get_df_attribute_renamed(df, old_name, new_name):
    """
    Getting a dataframe with a renaming specific attribute.
    
        :param df: DataFrame object
        :param old_name: string name
        :param new_name: string name
        :return df: DataFrame object 
    """
    df = df.rename(columns = {old_name : new_name})
    return df


def get_df_timestamp_changed(df, attr):
    """
    Getting dataframe with 'timestamp' attribute in date format.

        :param df: DataFrame object
        :param attr: string contains the attribute which contains timestamp value
        :return df: DataFrame object
    """
    df[attr] = pd.to_datetime(df['Date'], unit = 's')
    return df


def get_df_rows_filtered(df, attr, pattern, reg_ex, flag):
    """
    Getting a dataframe filtered.The flag value must be 0 or 1.
    0 = filter with equal operator
    1 = filter with contains function
    
        :param df: DataFrame object
        :param attr: string contains the attribute from which to compare value
        :param pattern: string to search for
        :param reg_ex: boolean value for regex
        :return df_filt: DataFrame object
    """
    if not flag:
        df_filt = df.loc[df[attr] == pattern]
    else:
        boolean_list = df[attr].str.contains(pattern, regex = reg_ex)
        df_filt = df.loc[boolean_list]
    return df_filt
    
    
def obtain_range_max_min_value(df, attr):
    """
    Obtaining the difference between the last and the first value in a specific attribute.

        :param df: DataFrame object
        :param attr: string contains the attribute which calculates the difference
        :return delta: difference value
    """
    delta = df[attr].max() - df[attr].min()
    return delta


def get_df_attributes_grouped_by(df, group_by_vect, attr1, attr2):
    """
    Getting a dataframe grouping by an attribute vector.

        :param df: DataFrame object
        :param group_by_vect: strings vector contains the attributes considered in the grouping
        :param attr1: string contains the attribute to sort
        :param attr2: string contains the attribute to sort by
        :return df_group: DataFrame object
    """
    df_group = df.groupby(group_by_vect).count()
    df_group = df_group[[attr1]].sort_values(by = attr2, ascending = False)
    return df_group


def get_df_attributes_added(df, attr_lst, lst_type):
    """
    Getting a dataframe with new specific type columns.The value "lst_type" must be object, str, float, double or int.
    
        :param df: DataFrame object
        :param attr_lst: string list contains attribute names
        :param lst_type: string contains the attribute type
    """
    for i in attr_lst:
        df[i] = pd.Series(dtype = lst_type)
    return df


def get_df_attributes_merged(df_1, df_2, df_1_attribute, df_2_attribute, merge_type):
    """
    Getting a dataframe obtained by merging two dataframe. The value "merge_type" must be inner, left, right, outer or cross
    and the default value is inner.
    
        :param df_1: Dataframe object
        :param df_2: Dataframe object
        :param df_1_attribute: string contains the attribute name in the df_1
        :param df_2_attribute: string contains the attribute name in the df_2
        :param merge_type: string contains the merge type
        :return df_final: Dataframe object
    """
    if df1_attribute != df_2_attribute:
        df_2 = get_df_attribute_renamed(df_2, df_2_attribute, df_1_attribute)
    df_final = df_1.merge(df_2, on = df_1_attribute, how = merge_type)
    return df_final


def get_df_invalid_ip_removed(df, attr):
    """
    Getting a dataframe without invalid ip-address from a dataframe which contains an ip-address attribute.
    
        :param df: DataFrame object
        :param attr: string contains the attribute name which contains ip values
        :return df: DataFrame object
    """
    for index, item in enumerate(df[attr]):
        try:
            ipaddress.ip_address(item)
        except ValueError:
            df.drop([index], inplace = True)
    return df


def get_df_ip_geolocated(mm_db, ip_list):
    """
    Getting a dataframe from maxminddb which contains some location ip informations.
    
        :param mm_db: Database object from maxmind project (GEOLITE2-CITY)
        :param ip_list: strings list contains ip address
        :return df_ip_loc: Dataframe_ip_loc object   
    """
    NEW_ATTRIBUTE_LST = ['Ip', 'City', 'Continent', 'Country', 'Location', 'Postal', 'Reg_country', 'Subdivisions']
    df_from_maxminddb = mx.open_database(mm_db)
    df_ip_loc = hand_module.pd.DataFrame()
    df_ip_loc = hand_module.get_df_attributes_added(df_ip_loc, NEW_ATTRIBUTE_LST, str)
    df_ip_loc['Ip'] = ip_list
    for index, item in enumerate(df_ip_loc['Ip']):
        df_single_ip = df_from_maxminddb.get(item)
        str_from_df = json.dumps(df_single_ip, ensure_ascii=False)
        ip_information_arr = str_from_df.split('},')
        for j in ip_information_arr:
            if 'city' in j:
                df_ip_loc['City'][index] = j
            elif 'continent' in j:
                df_ip_loc['Continent'][index] = j
            elif "\"country\"" in j:
                df_ip_loc['Country'][index] = j
            elif 'location' in j:
                df_ip_loc['Location'][index] = j
            elif 'postal' in j:
                df_ip_loc['Postal'][index] = j
            elif 'registered_country' in j:
                df_ip_loc['Reg_country'][index] = j
            elif 'subdivisions' in j:
                df_ip_loc['Subdivisions'][index] = j
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'City', 'City', "\"en\": \"", "\",", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Continent', 'Continent', "\"en\": \"", "\",", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Country', 'Country', "\"en\": \"", "\",", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Location', 'Long', "\"longitude\": \"", ",", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Location', 'Lat', "\"latitude\": \"", ",", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Postal', 'Postal', "{\"code\": \"", "\"", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Reg_country', 'Reg_country', "\"en\": \"", "\",", 1)
    df_ip_loc = hand_module.get_df_string_extracted(df_ip_loc, 'Subdivisions', 'Subdivisions', "\"en\": \"", "\",", 1)
    df_ip_loc.drop(['Location'], axis=1)
    return df_ip_loc


def obtain_map_ip_localized(mm_db, ip_list):
    """
    Obtaining a localize map of ip-addresses in the ip_list.

        :param mm_db: Database objectfrom maxminddb project (GEOLITE2-CITY)
        :param ip_list: string list which contains ip-addresses to localize
        :return ip_map: Map object 
    """
    df_ip_loc = get_dfgeolocation_ip(mm_db, ip_list) 
    ip_map = Map(basemap = basemaps.Esri.WorldStreetMap, zoom = 2, min_zoom = 2)
    control = FullScreenControl()
    measure = MeasureControl(position = 'topleft', active_color = 'red', primary_length_unit = 'miles')
    for index, item in enumerate(ip_list):
        if item in df_ip_loc['Ip']:
            lat = df_ip_loc.at[index, 'Lat']
            lng = df_ip_loc.lat[index, 'Long']
            ip = df_ip_loc.at[index, 'Ip']
            city_name = df_ip_loc.at[index, 'City']
            country_name = df_ip_loc.at[index, 'Country']
            marker = Marker(location = [lat.iat[0], lng.iat[0]], title = f"{ip}, {city_name}, {country_name}")
            ip_map.add_layer(marker)
    ip_map.add_control(control)
    ip_map.add_control(measure)
    measure.completed_color = 'red'
    return ip_map