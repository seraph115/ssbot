#!/usr/bin/python
#coding:UTF-8

import slackweb
import subprocess
import pytz
from datetime import datetime


slack = slackweb.Slack(url="https://hooks.slack.com/services/XXX")

sslocal_jp_start = "sslocal -c /etc/shadowsocks-config/shadowsocks-jp.json -d start"
sslocal_uk_start = "sslocal -c /etc/shadowsocks-config/shadowsocks-uk.json -d start"

sslocal_stop = "sslocal -d stop"

check_jp = "curl -s --socks5 127.0.0.1:8388 ip.gs |grep -c 'Tokyo'"
check_uk = "curl -s --socks5 127.0.0.1:8388 ip.gs |grep -c 'London'"

def ss_service_check(cmd_ss_start, cmd_ss_check, ss_location):

  process = subprocess.Popen(cmd_ss_start, shell=True, stdout=subprocess.PIPE)
  process.wait()
  output, err = process.communicate()

  process = subprocess.Popen(cmd_ss_check, shell=True, stdout=subprocess.PIPE)
  process.wait()
  output, err = process.communicate()
  # print "@" + output + "@"

  if output == "0\n":
    shanghai = pytz.timezone('Asia/Shanghai')
    now = datetime.now(shanghai).strftime('%Y-%m-%d %H:%M:%S')
    slack.notify(text=now + " > " + ss_location + " is dead!")

  process = subprocess.Popen(sslocal_stop, shell=True, stdout=subprocess.PIPE)
  process.wait()
  output, err = process.communicate()

def main():

  ss_service_check(sslocal_jp_start, check_jp, "Tokyo")
  ss_service_check(sslocal_uk_start, check_uk, "London")

if __name__ == '__main__':
    main()
