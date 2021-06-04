#Module to analyze dmarc standard of txt-type records.
import protocols.fdns.type_txt.txt as txt

def get_df_dmarc(path):
    """
    Get a dataframe fdns records txt-type with dmarc standard.The meaning of new attributes is: ASPF = spf 
    identifier alignment mode, ADKIM = dkim identifier alignment mode, FO = character indicates failure reporting 
    options, P = policy to be followed after DMARC check, PCT = DMARC check rate on mail stream from domain, 
    RF = auth-failure report type, RI = interval requested between aggregate reports, RUA = addresses to which 
    report is to be sent, RUF = addresses to which message failure information is to be sent, SP = requested 
    mail receiver policy for all subdomains. More informations at the link: https://tools.ietf.org/html/rfc7489#page-17.
    
        :param path: string contains the FDNS-TXT database path
        :return df_dmarc: Dataframe_dmarc object
    """
    NEW_ATTRIBUTE_LST = ['ASPF', 'ADKIM', 'FO', 'P', 'PCT', 'RF', 'RI', 'RUA', 'RUF', 'SP']
    NAN = txt.fdns.handle.math.nan
    attr_default_value = {'ASPF' : 'r', 'ADKIM' : 'r', 'FO' : '0', 'P' :  NAN, 'PCT' : '100', 'RF' : 'afrf', 'RI' : '86400',
                          'RUA' :  NAN, 'RUF' :  NAN, 'SP' :  NAN}
    df_txt = txt.get_df_txt(path)
    df_dmarc = txt.fdns.handle.get_df_rows_filtered(df_txt, 'Value', 'v=DMARC1', False, 1)
    df_dmarc = txt.fdns.handle.get_df_attributes_added(df_dmarc, NEW_ATTRIBUTE_LST , str)
    for index, item in enumerate(df_dmarc['Value']):
        aspf = txt.fdns.handle.re.search(r'(?<=aspf=).*?(?=[;}])', item)
        adkim = txt.fdns.handle.re.search(r'(?<=adkim=).*?(?=[;}])', item)
        fo = txt.fdns.handle.re.search(r'(?<=fo=).*?(?=[;}])', item)
        p = txt.fdns.handle.re.search(r'(?<=p=).*?(?=[;}])', item)
        pct = txt.fdns.handle.re.search(r'(?<=pct=).*?(?=[;}])', item)
        rf = txt.fdns.handle.re.search(r'(?<=rf=).*?(?=[;}])', item)
        ri = txt.fdns.handle.re.search(r'(?<=ri=).*?(?=[;}])', item)
        rua = txt.fdns.handle.re.search(r'(?<=rua=).*?(?=[;}])', item)
        ruf = txt.fdns.handle.re.search(r'(?<=ruf=).*?(?=[;}])', item)
        sp = txt.fdns.handle.re.search(r'(?<=sp=).*?(?=[;}])', item)
        attr_value_lst = [aspf, adkim, fo, p, pct, rf, ri, rua, ruf, sp]
        df_dmarc = txt.get_df_new_values_assigned(df_dmarc, index, attr_value_lst, attr_default_value)
    df_dmarc.drop(['Value'], axis = 1, inplace = True)
    return df_dmarc
