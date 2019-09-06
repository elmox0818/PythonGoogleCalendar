from __future__ import print_function
from tqdm import tqdm
from pytz import timezone
from dateutil import parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import datetime
import pickle
import os
import openpyxl
import configparser

# 本ソースコードを置く場所
SRC_PATH = "./"

# 設定ファイルのパスから設定情報を取得
CONF_FILEPATH = SRC_PATH + "config/myconf.conf"
config = configparser.ConfigParser()
config.read(CONF_FILEPATH, 'Shift-jis')

# Proxy関連
config_proxy = config['Proxy']
HTTP_PROXY = config_proxy['HTTP_PROXY']
HTTPS_PROXY = config_proxy['HTTPS_PROXY']

# その他設定関連
config_others = config['Conf']
# 取得するイベントの数
EVENT_NUM = config_others['EVENT_NUM']
# 出力するcsvファイルの名前
OUTPUT_FILENAME = config_others['OUTPUT_FILENAME']
# 取得開始日時、今日からの差分
DELTA_START = config_others['DELTA_START']
# 取得終了日時、今日からの差分
DELTA_END = config_others['DELTA_END']

# proxyの設定
os.environ["http_proxy"] = HTTP_PROXY
os.environ["https_proxy"] = HTTPS_PROXY

# csv形式で出力するためのevent格納用
event_list = []

# 曜日
yobi = ["月", "火", "水", "木", "金", "土", "日",
        "月", "火", "水", "木", "金", "土", "日"]

# 引用部分
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# 曜日取得関数
def getWeekDay(dateinfo):
    yobi = ["月", "火", "水", "木", "金", "土", "日"]
    try:
        a = datetime.datetime.strptime(dateinfo, '%Y/%m/%d')
        return yobi[a.weekday()]
    except ValueError:
        return "error"


# 日付情報フォーマット整理関数
def getDate(dateinfo):
    return dateinfo.split("T")[0].replace("-", "/")


# 時間情報フォーマット整理関数
def getTime(dateinfo):
    t = dateinfo.split("T")[1].split("+")[0].split(":")
    return t[0]+":"+t[1]


# メイン関数 Googleカレンダーへアクセスして予定を抽出する
# 参考URL
# https://qiita.com/lobmto/items/c1a220a12ec9c1fad560#3%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AE%E5%AE%9F%E8%A1%8C
def main():
    # ここから引用部分
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(SRC_PATH+'token.pickle'):
        with open(SRC_PATH+'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SRC_PATH+'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(SRC_PATH+'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # 引用部分 終了

    # ここからカスタマイズ部分
    now = datetime.datetime.utcnow()

    # 取得期間指定部分
    start = now + datetime.timedelta(days=int(DELTA_START))
    start = start.isoformat() + 'Z'
    end = now + datetime.timedelta(days=int(DELTA_END))
    end = end.isoformat() + 'Z'
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # 今日から指定した期日までにあるイベントを取得
    print('Getting the upcoming '+EVENT_NUM+' events')
    events_result = service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                          maxResults=EVENT_NUM, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    event_list.append(["年", "日付", "曜日", "開始時間", "終了時間", "イベント"])
    print("\n############################")
    print("##### Search Events... #####")
    print("############################\n")
    for event in tqdm(events):
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        # 特殊な条件つきイベントの分類
        # Tがあるものはタイムゾーンが取得できたもの
        if "T" in start:
            # 文字列にTが含まれることを考慮して、
            # Tで分割した左が時間の文字列の長さならばという条件を入れる。
            if len(start.split("T")[0]) == 10:
                event_list.append([getDate(start).split("/")[0],
                                   getDate(start).split(
                                       "/")[1]+"月"+getDate(start).split("/")[2]+"日",
                                   getWeekDay(getDate(start)),
                                   getTime(start),
                                   getTime(end),
                                   event['summary'], ]
                                  )
    with open(SRC_PATH+"output/"+OUTPUT_FILENAME+".csv", "w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(event_list)
    # カスタマイズ部分終了

if __name__ == '__main__':
    main()
