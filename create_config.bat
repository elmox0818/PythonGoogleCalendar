@echo off

REM configファイル更新バッチ
REM 呼び出しバッチから日付設定を受け取り、configファイルへと反映させる

echo 開始日:%1日後
echo 終了日:%2日後
echo 開始日時:%3

SET S_STRING=DELTA_START=%1
SET E_STRING=DELTA_END=%2
SET START_DATE=START_DATE=%3

REM Create now...
del .\config\myconf.conf /Q
set OUTPUT_FILE=.\config\myconf.conf

echo [Proxy] >> %OUTPUT_FILE%
echo HTTP_PROXY=http://proxy-xxxx.co.jp:8888 >> %OUTPUT_FILE%
echo HTTPS_PROXY=http://proxy-xxxx.co.jp:8888 >> %OUTPUT_FILE%
echo [Conf] >> %OUTPUT_FILE%
echo LOG_PATH=./log/logger.log >> %OUTPUT_FILE%
echo DAYS=10 >> %OUTPUT_FILE%
echo EVENT_NUM=500 >> %OUTPUT_FILE%
echo OUTPUT_FILENAME=output >> %OUTPUT_FILE%
echo %S_STRING% >> %OUTPUT_FILE%
echo %E_STRING% >> %OUTPUT_FILE%
echo %START_DATE% >> %OUTPUT_FILE%
