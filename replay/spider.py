

from models.job import JobModel
from replay.lagouAPI import LagouAPI
from replay.zhipinAPI import ZhipinAPI
import queue
import threading
import requests
import traceback

# from lagouAPI import LagouAPI


def get_job():
    pass

# 拉勾
def lagou_spider():
    try:
        jd = LagouAPI.search('Java',city='重庆')
        for j in jd:
            info = LagouAPI.geo_info(j)
            print(info) 
            job = JobModel(info)
            job.save()
    except Exception as e:
        print(e)

# todo 猎聘
def liepin_spider():
    try:
        jd = LagouAPI.search('Java',city='重庆')
        for j in jd:
            info = LagouAPI.geo_info(j)
            print(info)
            job = JobModel(info)
            job.save()
    except Exception as e:
        print(e)

# Boss 直聘
def zhipin_spider():
    try:
        job_dicts = ZhipinAPI.search()
        for job_dict in job_dicts:
            print(job_dict)
            job = JobModel(job_dict)
            job.save()
    except Exception as e:
        print(e)




if __name__ == '__main__':
    lagou_spider()
    # zhipin_spider()

