#Module to analyze dmarc standard of txt-type records.
import protocols.fdns.type_txt.txt as txt_module


def get_df_dmarc(path):
    """
    Getting a dataframe fdns records txt-type with dmarc standard.The meaning of new attributes is: ASPF = spf 
    identifier alignment mode, ADKIM = dkim identifier alignment mode, FO = character indicates failure reporting 
    options, P = policy to be followed after DMARC check, PCT = DMARC check rate on mail stream from domain, 
    RF = auth-failure report type, RI = interval requested between aggregate reports, RUA = addresses to which 
    report is to be sent, RUF = addresses to which message failure information is to be sent, SP = requested 
    mail receiver policy for all subdomains. More informations at the link: https://tools.ietf.org/html/rfc7489#page-17.
    
        :param path: string contains the FDNS-TXT database path
        :return df_marc: Dataframe_marc object
    """
    NEW_ATTRIBUTE_LST = ['ASPF', 'ADKIM', 'FO', 'P', 'PCT', 'RF', 'RI', 'RUA', 'RUF', 'SP']
    df_txt = txt_module.get_df_txt(path)
    df_dmarc = txt_module.fdns_module.hand_module.get_df_rows_filtered(df_txt, 'Value', 'v=DMARC1', False, 1)
    df_dmarc = txt_module.fdns_module.hand_module.get_df_attributes_added(df_dmarc, NEW_ATTRIBUTE_LST , str)
    for index, item in enumerate(df_dmarc['Value']):
        tmp_value_aspf = txt_module.fdns_module.hand_module.re.search(r'(?<=aspf=).*?(?=[;}])', item)
        tmp_value_adkim = txt_module.fdns_module.hand_module.re.search(r'(?<=adkim=).*?(?=[;}])', item)
        tmp_value_fo = txt_module.fdns_module.hand_module.re.search(r'(?<=fo=).*?(?=[;}])', item)
        tmp_value_p = txt_module.fdns_module.hand_module.re.search(r'(?<=p=).*?(?=[;}])', item)
        tmp_value_pct = txt_module.fdns_module.hand_module.re.search(r'(?<=pct=).*?(?=[;}])', item)
        tmp_value_rf = txt_module.fdns_module.hand_module.re.search(r'(?<=rf=).*?(?=[;}])', item)
        tmp_value_ri = txt_module.fdns_module.hand_module.re.search(r'(?<=ri=).*?(?=[;}])', item)
        tmp_value_rua = txt_module.fdns_module.hand_module.re.search(r'(?<=rua=).*?(?=[;}])', item)
        tmp_value_ruf = txt_module.fdns_module.hand_module.re.search(r'(?<=ruf=).*?(?=[;}])', item)
        tmp_value_sp = txt_module.fdns_module.hand_module.re.search(r'(?<=sp=).*?(?=[;}])', item)
        if not tmp_value_aspf:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('ASPF')] = 'r'
        else:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('ASPF')] = tmp_value_aspf.group(0)
        if not tmp_value_adkim:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('ADKIM')] = 'r'
        else:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('ADKIM')] = tmp_value_adkim.group(0)
        if not tmp_value_fo:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('FO')] = '0'
        else:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('FO')] = tmp_value_fo.group(0)
        if tmp_value_p:
             df_dmarc.iat[index, df_dmarc.columns.get_loc('P')] = tmp_value_p.group(0)
        if not tmp_value_pct:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('PCT')] = '100'
        else:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('PCT')] = tmp_value_pct.group(0)
        if not tmp_value_rf:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('RF')] = 'afrf'
        else:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('RF')] = tmp_value_rf.group(0)
        if not tmp_value_ri:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('RI')] = '86400'
        else:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('RI')] = tmp_value_ri.group(0)
        if tmp_value_rua:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('RUA')] = tmp_value_rua.group(0)
        if tmp_value_ruf:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('RUF')] = tmp_value_ruf.group(0)
        if tmp_value_sp:
            df_dmarc.iat[index, df_dmarc.columns.get_loc('SP')] = tmp_value_sp.group(0)  
    df_dmarc.drop(['Value'], axis = 1, inplace = True)
    return df_dmarc
