from nara_crowler import nara
from coupang_crowler import coupang

nara_instance = nara()
coupang_ins = coupang()
print("main1")
coupang_ins.excute(coupang_ins.URL,coupang_ins.header)
print("main2")