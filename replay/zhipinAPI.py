
from replay import *

import requests
from bs4 import BeautifulSoup
import urllib
import json
import time
import re
from replay.utils import log

headers ={
        'Cookie': 'sid=sem_pz_bdpc_dasou_title; JSESSIONID=""; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1536223709; __g=sem_pz_bdpc_dasou_title; lastCity=101040100; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Djava%26scity%3D101040100%26industry%3D%26position%3D; __c=1536223771; __l=r=https%3A%2F%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Djava%26scity%3D101040100%26industry%3D%26position%3D&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_ti; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1536223776; __a=10166106.1536223705.1536223705.1536223771.3.2.2.3',
        'Referer': 'https://www.zhipin.com/job_detail/?query=java&scity=101040100&industry=&position=',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

class ZhipinAPI(object):

    @classmethod
    def search(cls):
        jobs = []
        for i in range(1, 11):
            time.sleep(1)
            page = i
            url = "https://www.zhipin.com/c101040100/h_101040100/?query=java&page={page}&ka=page-{page}".format(
                page=page)
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                text = response.text
                # 搜索，拿到页面url
                urls=cls.parser_page(text)
                for url in urls:
                    try:
                        # 解析页面详细信息
                        job = cls.parser_detail(url)
                        jobs.append(job)
                    except Exception as e:
                        print(e)

            else:
                print("获取页面失败, 错误代码:" + str(response.status_code))

        return jobs


    # 解析页面中的job列表
    @classmethod
    def parser_page(text):
        host = 'https://www.zhipin.com'
        urls = []

        # <a href="/job_detail/7c599b93587deb5c1XR-2d68FFI~.html" data-jid="7c599b93587deb5c1
        pattern = re.compile(r'<a href="(/job_detail/[^"]*html)"')
        results = pattern.findall(text)

        for i in results:
            i = host + i
            urls.append(i)
        return urls

    @classmethod
    def parser_detail(url):
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            text = response.text
        else:
            print("获取详细页面失败")
            return None

        soup = BeautifulSoup(text, 'lxml')
        companyShortName = soup.select('.info-company .name')[0].get_text()
        companyFullName = soup.select('.job-sec .name')[0].get_text()
        financeStage = soup.select('.info-company p')[0].next_element
        workYear = soup.select('.job-primary .info-primary p')[0].contents[2][3:]
        createTime = soup.select('.job-primary .job-author')[0].get_text()[3:]
        positionLables = ' '.join(list(map(lambda x: x.get_text(), soup.select('.info-primary .job-tags span'))))
        salary = soup.select('.job-banner .badge')[0].get_text().strip().replace(' ', '').replace('\n', '')
        city = soup.select('.job-primary .info-primary p')[0].contents[0][3:]
        positionName = soup.select('.job-primary .name h1')[0].get_text()
        companyLabelList = soup.select('.job-detail .job-sec .job-tags')[0].get_text().replace('\n', ' ') if len(
            soup.select('.job-detail .job-sec .job-tags')) > 0 else ''
        companySize = soup.select('.info-company p')[0].contents[2]
        industryField = soup.select('.info-company p a[ka="job-detail-brandindustry"]')[0].get_text()
        education = soup.select('.job-primary .info-primary p')[0].contents[4][3:]
        addr = soup.select('.job-sec .job-location .location-address')[0]
        compURL = url

        d = dict(
            companyShortName=companyShortName,
            financeStage=financeStage,
            workYear=workYear,
            createTime=createTime,
            positionLables=positionLables,
            salary=salary,
            businessZones='',
            city=city,
            positionName=positionName,
            district='',
            companyLabelList=companyLabelList,
            positionAdvantage=companyLabelList,
            jobNature='全职',
            companySize=companySize,
            industryField=industryField,
            formatCreateTime='',
            education=education,
            companyFullName=companyFullName,
            companyLogo='',
            positionId='',
            companyId='',
            addr=addr,
            compURL=compURL,
            source='Boss直聘',
        )
        return d