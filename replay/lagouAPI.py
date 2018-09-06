
from replay import *

import requests
from bs4 import BeautifulSoup
import urllib
import json
import time
from replay.utils import log

headers = {
            'Referer': 'https://www.lagou.com/jobs/list_java?city=%E9%87%8D%E5%BA%86&cl=false&fromSearch=true&labelWords=&suginput=',
            'Cookie': 'JSESSIONID=ABAAABAAAIAACBIA0721D936211900A529FDB971434CA42; _ga=GA1.2.1693037819.1536205773; _gid=GA1.2.1271136408.1536205773; user_trace_token=20180906114930-dc35d194-b187-11e8-b620-5254005c3644; LGUID=20180906114930-dc35d622-b187-11e8-b620-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536205773,1536215016; LGSID=20180906142333-6179488e-b19d-11e8-8bd1-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIwSlwqpoWZkz-jHHLIcrYe23o1a8gwKgi7UssCA50pm%26ck%3D4208.1.94.270.146.252.141.263%26shh%3Dwww.baidu.com%26sht%3Dbaiduhome_pg%26wd%3D%26eqid%3Dbf542d3200025f69000000055b90c7e1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _gat=1; LGRID=20180906144656-a5858364-b1a0-11e8-8bd4-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536216419; SEARCH_ID=a3fd224b819b450ca2de1dbdc3a026a5',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        }

class LagouAPI(object):
    LAGOU_GATEWAY = 'https://www.lagou.com/jobs/positionAjax.json?'
    sess = requests.Session()

    @classmethod
    def search(cls, kd, **kwargs):
        # print(kwargs)
        # https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false
        """
        first:true
        pn:1
        kd:python
        """

        # 拼接url
        # urllib库里面有个urlencode函数，可以把key-value这样的键值对转换成我们想要的格式，返回的是a=1&b=2这样的字符串
        url_encoded = urllib.parse.urlencode(kwargs)
        jl_url = cls.LAGOU_GATEWAY + url_encoded
        print(jl_url)

        page = 1
        page_max = None
        while True:
            payload = {
                'pn': page,
                'kd':kd,
                'first': False,
            }
            print(payload)
            json_result = cls._db_h(jl_url, payload)
            log(json_result)
            if page_max is None:
                # 获得页数
                page_max = json_result['content']['positionResult']['totalCount']
                # # 119 
                # if page_max > 10:
                #     page_max = 10
                print(page_max)
            # 用生成器返回得到的结果
            result = json_result['content']['positionResult']['result']
            for j in result:
                yield j
                # cls.geo_info(j)
            if page >= page_max:
                break
            page += 1


    @classmethod
    def get_location_by_pos_id(cls, pos_id):
        r = cls.sess.get('https://www.lagou.com/jobs/{}.html'.format(pos_id), headers=headers, verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        # log(soup)
        corp_info = soup.select('.work_addr')[0].get_text()
        corp_info = corp_info.strip().replace(' ','').replace('\n','')
        return corp_info

    @classmethod
    def _db_h(cls, jl_url, payload):
        """
        获取网络信息
        """
        print("db ", payload)
        r = cls.sess.post(jl_url, headers=headers, data=payload, verify=False)
        return r.json()

        # url = 'px=default&city={}&needAddtionalResult=false'.format(kwargs.get('city'))
        # cls.jl_url = cls.LAGOU_GATEWAY + url

        # wb_data = requests.post(cls.jl_url, data=payload).text
        # print(wb_data)
        # print(json_result)
    @classmethod
    def geo_info(cls, j):
        print('jj', j)
        busine = j['businessZones']
        comp = j['companyLabelList']
        positions = j['positionLables']
        d = dict(
            companyShortName = j['companyShortName'],
            # ctime = j['ctime']
            financeStage = j['financeStage'],
            workYear = j['workYear'],
            createTime = j['createTime'],
            positionLables = ' '.join(positions if positions is not None else ''),
            salary = j['salary'],
            businessZones = ' '.join(busine if busine is not None else ''),
            city = j['city'],
            positionName = j['positionName'],
            district = j['district'],
            companyLabelList = ' '.join(comp if comp is not None else ''),
            positionAdvantage = j['positionAdvantage'],
            jobNature = j['jobNature'],
            companySize = j['companySize'],
            industryField = j['industryField'],
            formatCreateTime = j['formatCreateTime'],
            education = j['education'],
            companyFullName = j['companyFullName'],
            companyLogo = j['companyLogo'],
            positionId = j['positionId'],
            companyId = j['positionId'],
            source = '拉勾',
        )
        compURL = 'https://www.lagou.com/jobs/{}.html'.format(d['companyId'])
        addr = cls.get_location_by_pos_id(d['positionId'])
        d['addr'] = addr
        d['compURL'] = compURL
        time.sleep(0.5)
        # print(addr, companyFullName, salary)
        return d