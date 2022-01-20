# 导入类文件
import requests,base64,json,hashlib
from Crypto.Cipher import AES
#开始解密网易云加密密码
def encrypt(key, text):
    cryptor = AES.new(key.encode('utf8'), AES.MODE_CBC, b'0102030405060708')
    length = 16                    
    count = len(text.encode('utf-8'))     
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 16             
    pad = chr(add)
    text1 = text + (pad * add)    
    ciphertext = cryptor.encrypt(text1.encode('utf8'))          
    cryptedStr = str(base64.b64encode(ciphertext),encoding='utf-8')
    return cryptedStr
def md5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()
def protect(text):
    return {"params":encrypt('TA3YiYCfY2dDJQgg',encrypt('0CoJUm6Qyw8W8jud',text)),"encSecKey":"84ca47bca10bad09a6b04c5c927ef077d9b9f1e37098aa3eac6ea70eb59df0aa28b691b7e75e4f1f9831754919ea784c8f74fbfadf2898b0be17849fd656060162857830e241aba44991601f137624094c114ea8d17bce815b0cd4e5b8e2fbaba978c6d1d14dc3d1faf852bdd28818031ccdaaa13a6018e1024e2aae98844210"}
#解密结束
#向服务端发送请求
s=requests.Session()
header={}
url="https://music.163.com/weapi/login/cellphone"
url2="https://music.163.com/weapi/point/dailyTask"

logindata={
    "phone":input(),
    "countrycode":"86",
    "password":md5(input()),
    "rememberLogin":"true",
}
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        "Referer" : "http://music.163.com/",
        "Accept-Encoding" : "gzip, deflate",
        }
headers2 = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        "Referer" : "http://music.163.com/",
        "Accept-Encoding" : "gzip, deflate",
        "Cookie":"os=pc; osver=Microsoft-Windows-10-Professional-build-10586-64bit; appver=2.0.3.131777; channel=netease; __remember_me=true;"
        }
#请求发送结束
#开始登陆
res=s.post(url=url,data=protect(json.dumps(logindata)),headers=headers2)
tempcookie=res.cookies
object=json.loads(res.text)
if object['code']==200:
    print("登录成功！")
else:
    print("登录失败！请检查密码是否正确！"+str(object['code']))
    exit(object['code'])
#登录结束

#开始签到
res=s.post(url=url2,data=protect('{"type":0}'),headers=headers)
object=json.loads(res.text)
if object['code']!=200 and object['code']!=-2:
    print("签到时发生错误："+object['msg'])
else:
    if object['code']==200:
        print("签到成功，经验+"+str(object['point']))
    else:
        print("重复签到")
#签到结束

    exit
#程序结束
