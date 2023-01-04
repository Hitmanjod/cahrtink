import requests
from bs4 import BeautifulSoup
import pandas as pd

Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'

#You need to copy paste condition in below mentioned Condition variable

Condition = "( {57960} ( 1 day ago ema ( close,3 ) > 1 day ago ema ( close,8 ) and 2 day ago  ema ( close,3 )<= 2 day ago  ema ( close,8 ) and 1 day ago \"close - 1 candle ago close / 1 candle ago close * 100\" >= 2 and 1 day ago volume >= 100000 and latest close > 1 day ago close ) ) "

def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
    return df

data = GetDataFromChartink(Condition)

if (len(data)==0):
    print("The data is empty")
else:
    data = data.sort_values(by='per_chg', ascending=False)

print(data)

data.to_csv("Chartink_result.csv")


TelegramBotCredential = '5963732843:AAGhk6iUG_r5-AsN7m16RSbm7SOK_JUepMc'
ReceiverTelegramID = '882232390' #my personal id


def SendMessageToTelegram(Message):
    try:
        Url = "https://api.telegram.org/bot" + str(TelegramBotCredential) +  "/sendMessage?chat_id=" + str(ReceiverTelegramID)
        
        textdata ={ "text":Message}
        response = requests.request("POST",Url,params=textdata)
    except Exception as e:
        Message = str(e) + ": Exception occur in SendMessageToTelegram"
        print(Message)  
		
		
def SendTelegramFile(FileName):
    Documentfile={'document':open(FileName,'rb')}
    
    Fileurl = "https://api.telegram.org/bot" + str(TelegramBotCredential) +  "/sendDocument?chat_id=" + str(ReceiverTelegramID)
      
    response = requests.request("POST",Fileurl,files=Documentfile)
	

#SendMessageToTelegram("HI test message")
SendMessageToTelegram(data)
SendTelegramFile("Chartink_result.csv")