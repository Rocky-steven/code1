#!/usr/bin/python3
#coding=utf-8
import sys
import json
import requests

class iciba:
    # chushihua
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid'].strip()
        self.appsecret = wechat_config['appsecret'].strip()
        self.template_id = wechat_config['template_id'].strip()
        self.access_token = ''

    #cuowucode 
    def get_error_info(self, errcode):
        return {
            40013:'No formal ID, please engineer check AppID ture or false',
            40125:'ignore ID',
            41001:'append Id characset',
	    40003:'No formal Id ,please engineerr check (Usered) ture or false care mp.wechat',
	    40037:'ignore templateID',
        }.get(errcode,'unknown error')

    #printdairy
    def print_log(self, data, openid=''):
        errcode = data['errcode']
        errmsg = data['errmsg']
        if errcode == 0:
            print(' [INFO] send to %s is success' % openid)
        else:
            print(' [ERROR] (%s) %s - %s' % (errcode, errmsg, self.get_error_info(errcode)))
            if openid is not '':
                print(' [ERROR] send to %s is error' % openid)
            sys.exit(1)

    # accept access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            self.access_token = data['access_token']

    #accept userlist
	
    def	get_user_list(self):
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % self.access_token
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            openids = data['data']['openid']
            return openids

    #send massage
    def send_msg(self, openid, template_id, iciba_everyday):
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': iciba_everyday['fenxiang_img'],
            'data': {
                'content': {
                    'value': iciba_everyday['content'],
                    'color': '#0000CD'
                    },
                'note': {
                    'value': iciba_everyday['note'],
                },
                'translation': {
                    'value': iciba_everyday['translation'],
                }
            }
        }
        json_data = json.dumps(msg)
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % self.access_token
        r = requests.post(url, json_data)
        return json.loads(r.text)

    #accept ciba everyday 
    def get_iciba_everyday(self):
        url = 'http://open.iciba.com/dsapi/'
        r = requests.get(url)
        return json.loads(r.text)

    #for user set everyday words
    def send_everyday_words(self, openids):
        everyday_words = self.get_iciba_everyday()
        for openid in openids:
            openid = openid.strip()
            result = self.send_msg(openid, self.template_id, everyday_words)
            self.print_log(result, openid)

    #run
    def run(self, openids=[]):
        if openids == []:
	    #if openids is none , chrome user list
            openids = self.get_user_list()
	#if openids for user to send massage
        self.send_everyday_words(openids)
