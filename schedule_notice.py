import requests
import calendar
import datetime
import pytz
import pandas as pd
import schedule
import time

#send a message to your talkroom
#get your token at <https://notify-bot.line.me/ja/>
#if you want get more information, please read this page; <https://qiita.com/iitenkida7/items/576a8226ba6584864d95>

def send_line(message):
    url = 'https://notify-api.line.me/api/notify'
    access_token = '(your-token)' #LINE Notifyで取得したトークンを代入
    headers = {'Authorization': 'Bearer' + ' ' + access_token}
    payload = {'message': message}
    r = requests.post(url, headers=headers, data=payload)
    print(r)
    
#get nth day-of-week
def get_nth_week(day):
    return (day - 1) // 7 + 1
def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)
    
#get tomorrow`s data
def tomorrow():
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    tomorrow = today + datetime.timedelta(days=1)
    tom_nth_dow = get_nth_dow(tomorrow.year, tomorrow.month, tomorrow.day)
    return tom_nth_dow
    
#garbage-schedule(show example below)
def garbage_schedule():
    schedule = pd.DataFrame([
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        ['燃えるごみ', '資源ごみ', '', '燃えるごみ', '空き缶', '', ''],
        ['燃えるごみ', '', '空き瓶', '燃えるごみ', '', '', ''],
        ['燃えるごみ', '資源ごみ', '', '燃えるごみ', '空き缶', '', ''],
        ['燃えるごみ', '', '燃やさないごみ', '燃えるごみ', '', '', ''],
        ['燃えるごみ', '資源ごみ', '', '燃えるごみ', '空き缶', '', ''],
    ])
    return schedule
    
#make a message to tell you the garbage-schedule
def tom_gar_info():
    date_jp = ['月', '火', '水', '木', '金', '土', '日']
    date_check = garbage_schedule().iat[tomorrow()]
    text1 = '明日は第'+str(tomorrow()[0])+date_jp[tomorrow()[1]]+'曜日'
    if date_check == '':
        text2 = 'ごみの回収はありません'
    else:
        text2 = date_check+'回収の日です'
    return '\n' + text1 + '\n' + text2
    
#send the message you made
#autorun when am6:00 & pm21:00
def action():
    send_line(tom_gar_info())

schedule.every().days.at("21:00").do(action)
schedule.every().days.at("06:00").do(action)

#supervise the execution of task(action)
while True:
    schedule.run_pending() 
    time.sleep(1)
