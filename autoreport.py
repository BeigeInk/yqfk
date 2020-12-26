import requests
import json
import time,datetime
import pandas as pd
import yagmail


def automatic(username,password):
    r = requests.session()
    r.headers = {
        "Referer": "https://app.upc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.upc.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    r.get("https://app.upc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.upc.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex")
    
    a=eval(r.post("https://app.upc.edu.cn/uc/wap/login/check", data={"username": username, "password": password}).text)

    if(len(a['m'])!=4 ):
        return "login error"
    
        
    t = None
    t = r.get("https://app.upc.edu.cn/ncov/wap/default/index").json()

    i = t['d']['oldInfo']
    # print( t['d'])
    i['date'] = t['d']['info']['date']
    i['id'] = t['d']['info']['id']
    i['created'] = t['d']['info']['created']
    #print(i)
    its=r.post("https://app.upc.edu.cn/ncov/wap/default/save",data=i).json()
    return its["m"]

yag = yagmail.SMTP(
    host='smtp.163.com', 
    user='你的邮箱地址',
    password='你的授权码'
)

user_info=pd.read_csv("data_info.csv")
for i in range(len(user_info)):
    report_user=automatic(user_info['username'][i],user_info['password'][i])
    print(str(user_info["username"][i])+str(report_user))
    email_user=user_info["emailadress"][i]
    if(user_info["needtoreport"][i]==1):
        yag.send(email_user,"daily report"+str(datetime.date.today()),str(user_info["username"][i])+report_user)
    time.sleep(10)
