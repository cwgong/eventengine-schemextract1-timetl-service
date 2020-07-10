# -*- coding: utf-8 -*-

from threading import Timer
import time_utils
import download_data
from get_docfeature import get_doc_abstract
from event import Event_Supervision
from cluster import Cluster
from save_result import save_schema_result_to_api
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('main')

def doing_job():
    
    logging.info('doing_job() ...')
    '''
    # -------------------------------------------------- #
    # step 1
    # get increment by compare
    # -------------------------------------------------- #
    compare_gap = 3 # Params
    start_time = time_utils.n_days_ago(compare_gap)
    end_time = time_utils.current_time()

    logger.info("compare_gap: {}".format(compare_gap))
    logger.info("start_time: {}".format(start_time))
    logger.info("end_time: {}".format(end_time))
    
    original_data_file = './logs/original_data_file.txt'
    extradata_file = './logs/extradata_file.txt'
    
    # 获取增量数据
    data_file, temp_data = download_data.get_extradata_from_api(start_time, end_time, original_data_file, extradata_file)

    # -------------------------------------------------- #
    # step 2
    # doc 聚类所需特征抽取 increment = data_file
    # doc ——> abstract
    # -------------------------------------------------- #
    data_file_ = './logs/abstract_file.txt'
    data_file_ = get_doc_abstract(data_file, data_file_)
    
    # 太少的“有效”数据不做聚类
    data_size = download_data.count_data_size(data_file_)
    logging.info("data_size: {}".format(data_size))   
    if data_size < 50:
        logger.info("data size <  {}".format(data_size))
        return
    # 覆盖掉 original_data_file
    download_data.update_original_data_file(temp_data, original_data_file)    
    temp_data = [] # 清空
    '''
    
    # -------------------------------------------------- #
    # step 3
    # event type judge ——> use doc features（label、abstract）
    # schema extract
    # -------------------------------------------------- #
    data_file_ = './logs/abstract_file.txt'
    event_supervision = Event_Supervision()
    schemas = event_supervision.get_event_schema(data_file_)
    # print(schemas)
    save_schema_result_to_api(schemas)
    event_supervision.release()
    # -------------------------------------------------- #
    # step 4
    # load ori_clusters & clustering
    # -------------------------------------------------- #
    '''
    ori_clusters = []
    cluster = Cluster()
    ori_clusters = cluster.clustering(ori_clusters, schemas)

    ori_clusters = cluster.sort(ori_clusters)
    for x in ori_clusters[0:20]:
        print(x)
    '''
    # -------------------------------------------------- #
    # step 4
    # save local & api
    # -------------------------------------------------- #
    
    
    logging.info('doing_job() over!')



def excute_timing(): 
    
    global t
    
    try:
        doing_job()
    except Exception as e:
        logger.exception(e) 
        
    time_gap = int((4)*60*60*1000) # 间隔 n 小时（由于执行时间较长，可能为45分钟左右）
    t = Timer(time_gap/1000, excute_timing)
    t.start()
    
    
    
if __name__ == '__main__':
    
    doing_job()
    '''
    try:
        time_gap = int((1/3600)*60*60*1000) 
        t = Timer(time_gap/1000, excute_timing)
        t.start()
    except Exception as e:
        logger.exception(e) 
    '''
    