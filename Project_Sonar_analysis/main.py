#Analyze standard security mail and tcp ports 21, 22 and 23 of one host in the network.
import protocols.tcp.tcp as tcp_module
import protocols.fdns.type_txt.standard.dkim as dkim_module
import protocols.fdns.type_txt.standard.dmarc as dmarc_module
import protocols.fdns.type_txt.standard.sts as sts_module
import protocols.fdns.type_txt.standard.spf as spf_module
import protocols.fdns.type_a.a as a_module


#Create necessary dataframe.

df_dkim = dkim_module.get_df_dkim('./data/project_sonar/2021-04-23-1619217645-fdns_txt.json.gz')
df_dkim.head(20)
