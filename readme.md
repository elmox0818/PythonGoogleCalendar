# Google カレンダーからの予定抽出

## 仕様

https://qiita.com/lobmto/items/c1a220a12ec9c1fad560#3%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AE%E5%AE%9F%E8%A1%8C
ここを参考に API を利用して、カレンダーの情報を抽出。csv ファイルを作成する。
社内での他システム連携のため実装した。

## フォルダ説明

- output/
  抽出した情報から作成した csv ファイルはここに出力される。
- config/
  設定ファイルが入っている

## ファイル説明

- get_schedule.py
  python の実行ファイル
- create_config.bat
  config内の設定ファイル編集バッチ。ユーザがWebページで入力した値に沿って引数を与えて実行して書き換える。
  そのあとにpythonスクリプトを実行する。

## 設定値変更

### config/myconf.conf を編集する

- [Proxy]は proxy 情報
- [Conf]は実行条件設定
  - EVENT_NUM:取得する予定の数
  - OUTPUT_FILENAME:出力ファイル名
  - DELTA_START:開始日の今日からの差分
  - DELTA_END:開始日の今日からの差分
  - START_DATE:開始日
