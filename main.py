#!/usr/bin/python3
#coding=utf-8
import Iciba

if __name__ == '__main__':
    #
    wechat_config = {
        'appid': 'wx079d4a8cd3854493', #
        'appsecret': '7c439e49b7f15445e6d7526fa6067946', #
        'template_id': 'D0cP7B99F6KetjrZO5HVjwW5NW37GtZXqhGgU-WNSF4' #
    }
    
    #
    openids = [
        'od46bxGAufIN1KZlHCyB1P867kvY',
        'od46bxFvSXJpsPskFV27dHXu8Dt0',#
        #
    ]

    #
    icb = Iciba.iciba(wechat_config)

    '''
    run()
    '''
    icb.run()
