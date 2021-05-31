#Module to analyze dkim standard of txt-type records.
import protocols.fdns.type_txt.txt as txt_module


def get_df_dkim(path):
    """
    Getting a dataframe fdns records txt-type with dkim standard. The meaning of new attributes is: HASH_ALG = hash
    algorithm accepted by domain to encrypte, KEY_TYPE = key type accepted by domain, TAG = optional tags,
    PUBL_KEY = public key to verify mails, SERVICE = service type, NOTE = human expressions. More informations at
    the link: https://tools.ietf.org/html/rfc6376#page-26.
    
        :param path: string contains the FDNS-TXT database path
        :return df_dkim: Dataframe_dkim object
    """
    NEW_ATTRIBUTE_LST = ['HASH_ALG', 'KEY_TYPE', 'TAG', 'PUBL_KEY', 'SERVICE', 'NOTE']
    df_txt = txt_module.get_df_txt(path)
    df_dkim = txt_module.fdns_module.hand_module.get_df_rows_filtered(df_txt, 'Value', 'v=DKIM1', False, 1)
    df_dkim = txt_module.fdns_module.hand_module.get_df_attributes_added(df_dkim, NEW_ATTRIBUTE_LST , str)
    for index, item in enumerate(df_dkim['Value']):
        tmp_hash_alg = txt_module.fdns_module.hand_module.re.search(r'(?<=h=).*?(?=;)', item)
        tmp_key_type = txt_module.fdns_module.hand_module.re.search(r'(?<=k=).*?(?=;)', item)
        tmp_tag = txt_module.fdns_module.hand_module.re.search(r'(?<=t=).*?(?=;)', item)
        tmp_publ_key = txt_module.fdns_module.hand_module.re.search(r'(?<=p=).*?(?=[;}])', item)
        tmp_service = txt_module.fdns_module.hand_module.re.search(r'(?<=s=).*?(?=;)', item)
        tmp_note = txt_module.fdns_module.hand_module.re.search(r'(?<=[ ;]n=).*?(?=;)', item)
        if not tmp_hash_alg:
            df_dkim.iat[index, df_dkim.columns.get_loc('HASH_ALG')] = '*'
        else:
            df_dkim.iat[index, df_dkim.columns.get_loc('HASH_ALG')] = tmp_hash_alg.group(0)
        if not tmp_key_type:
            df_dkim.iat[index, df_dkim.columns.get_loc('KEY_TYPE')] = 'rsa'
        else:
            df_dkim.iat[index, df_dkim.columns.get_loc('KEY_TYPE')] = tmp_key_type.group(0)
        if tmp_tag:
            df_dkim.iat[index, df_dkim.columns.get_loc('TAG')] = tmp_tag.group(0)
        if not tmp_publ_key:
             df_dkim.iat[index, df_dkim.columns.get_loc('PUBL_KEY')] = 'KEY-REVOKE'
        else:
            df_dkim.iat[index, df_dkim.columns.get_loc('PUBL_KEY')] = tmp_publ_key.group(0)
        if not tmp_service:
            df_dkim.iat[index, df_dkim.columns.get_loc('SERVICE')] = '*'
        else:
            df_dkim.iat[index, df_dkim.columns.get_loc('SERVICE')] = tmp_service.group(0)
        if tmp_note:
            df_dkim.iat[index, df_dkim.columns.get_loc('NOTE')] = tmp_note.group(0)
    df_dkim.drop(['Value'], axis = 1, inplace = True)  
    return df_dkim
