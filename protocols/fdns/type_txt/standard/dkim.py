#Module to analyze dkim standard of txt-type records.
import protocols.fdns.type_txt.txt as txt

def get_df_dkim(path):
    """
    Get a dataframe fdns records txt-type with dkim standard. The meaning of new attributes is: HASH_ALG = hash
    algorithm accepted by domain to encrypte, KEY_TYPE = key type accepted by domain, TAG = optional tags,
    PUBL_KEY = public key to verify mails, SERVICE = service type, NOTE = human expressions. More informations at
    the link: https://tools.ietf.org/html/rfc6376#page-26.
    
        :param path: string contains the FDNS-TXT database path
        :return df_dkim: Dataframe_dkim object
    """
    NEW_ATTRIBUTE_LST = ['HASH_ALG', 'KEY_TYPE', 'TAG', 'PUBL_KEY', 'SERVICE', 'NOTE']
    NAN = txt.fdns.handle.math.nan
    df_txt = txt.get_df_txt(path)
    df_dkim = txt.fdns.handle.get_df_rows_filtered(df_txt, 'Value', 'v=DKIM1', False, 1)
    df_dkim = txt.fdns.handle.get_df_attributes_added(df_dkim, NEW_ATTRIBUTE_LST , str)
    attr_default_value = {'HASH_ALG' : '*', 'KEY_TYPE' : 'rsa', 'TAG' : NAN, 'PUBL_KEY' : 'KEY_REVOKE', 'SERVICE' : '*',
                          'NOTE' : NAN}
    for index, item in enumerate(df_dkim['Value']):
        hash_alg = txt.fdns.handle.re.search(r'(?<=h=).*?(?=;)', item)
        key_type = txt.fdns.handle.re.search(r'(?<=k=).*?(?=;)', item)
        tag = txt.fdns.handle.re.search(r'(?<=t=).*?(?=;)', item)
        publ_key = txt.fdns.handle.re.search(r'(?<=p=).*?(?=[;}])', item)
        service = txt.fdns.handle.re.search(r'(?<=s=).*?(?=;)', item)
        note = txt.fdns.handle.re.search(r'(?<=[ ;]n=).*?(?=;)', item)
        attr_value_lst = [hash_alg, key_type, tag, publ_key, service, note]
        df_dkim = txt.get_df_new_values_assigned(df_dkim, index, attr_value_lst, attr_default_value)
    df_dkim.drop(['Value'], axis = 1, inplace = True)
    return df_dkim