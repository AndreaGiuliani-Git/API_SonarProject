#Module to analyze dmarc standard of txt-type records.
import protocols.fdns.type_txt.txt as txt_module


def get_df_dmarc(path):
    """
    Get a dataframe fdns records txt-type with dmarc standard.The meaning of new attributes is: ASPF = spf 
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
    dictionary = {
        'ASPF' : 'r',
        'ADKIM' : 'r',
        'FO' : '0',
        'P' :  txt_module.fdns_module.hand_module.math.nan,
        'PCT' : '100',
        'RF' : 'afrf',
        'RI' : '86400',
        'RUA' :  txt_module.fdns_module.hand_module.math.nan,
        'RUF' :  txt_module.fdns_module.hand_module.math.nan,
        'SP' :  txt_module.fdns_module.hand_module.math.nan
    }
    for index, item in enumerate(df_dmarc['Value']):
        aspf = txt_module.fdns_module.hand_module.re.search(r'(?<=aspf=).*?(?=[;}])', item)
        adkim = txt_module.fdns_module.hand_module.re.search(r'(?<=adkim=).*?(?=[;}])', item)
        fo = txt_module.fdns_module.hand_module.re.search(r'(?<=fo=).*?(?=[;}])', item)
        p = txt_module.fdns_module.hand_module.re.search(r'(?<=p=).*?(?=[;}])', item)
        pct = txt_module.fdns_module.hand_module.re.search(r'(?<=pct=).*?(?=[;}])', item)
        rf = txt_module.fdns_module.hand_module.re.search(r'(?<=rf=).*?(?=[;}])', item)
        ri = txt_module.fdns_module.hand_module.re.search(r'(?<=ri=).*?(?=[;}])', item)
        rua = txt_module.fdns_module.hand_module.re.search(r'(?<=rua=).*?(?=[;}])', item)
        ruf = txt_module.fdns_module.hand_module.re.search(r'(?<=ruf=).*?(?=[;}])', item)
        sp = txt_module.fdns_module.hand_module.re.search(r'(?<=sp=).*?(?=[;}])', item)
        value_lst = [aspf, adkim, fo, p, pct, rf, ri, rua, ruf, sp]
        df_dmarc = txt_module.get_df_new_values_assigned(df_dmarc, index, value_lst, dictionary)
    df_dmarc.drop(['Value'], axis = 1, inplace = True)
    return df_dmarc
