# -*- encoding:utf8 -*-

import json
import logging.config
import codecs
import requests

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('main')


def save_cluster_result_to_file(cluster_result, origin_cluster_file_path):
    
    fout = codecs.open(origin_cluster_file_path, 'w', encoding='utf-8')
    for item in cluster_result:
        strObj = json.dumps(item, ensure_ascii=False)
        fout.write(strObj+'\n')

        # schema_cluster_id = item['id']
        # info_id = item['info_id']
        # schema_ids = item['schema_ids']
        # info_ids = item['info_ids']
        # schema = item['schema']
        # extractScope = item['extractScope']
        # schemaType = item['schemaType']
        # ners = item['ners']
        # publishAt = item['publishAt']
        #
        # if len(info_ids) > 1:
        #     logger.info('cluster_id: '+str(cluster_id))
        #     logger.info('hot: '+str(len(info_ids)))
        #     logger.info('score: '+str(score))
        #     logger.info('title: '+str(title))
        #     logger.info('keywords: '+str(keywords))
        #     logger.info('all_titles: '+str(all_titles))
        #     logger.info('title_keywords_dic: '+str(title_keywords_dic))
        #     logger.info('content_keywords: '+str(content_keywords))
        #     logger.info('publish_time: '+str(publish_time))
        #     logger.info('min_publishtime: '+str(min_publishtime))
        #     logger.info('max_publishtime: '+str(max_publishtime))
        #     logger.info('info_ids: '+str(info_ids))
        #     logger.info('--------------------------')

        content = item['content']
        creatAt = item['creatAt']
        deleteFlag = "0"
        extractScope = item['extractScope']
        humanFlag = item['humanFlag']
        id = item['id']
        infoId = item['infoId'] #每一篇资讯的id
        ners = item['ners']
        occurAt = item['occurAt']
        paragraph = item['paragraph']
        publishAt = item['publishAt']
        schema = item['schema']
        schemaType = item['schemaType']

        # if len()
        
    fout.close()
    
# def save_cluster_result_to_api()

def save_schema_result_to_file(schema_result,schema_result_file_path):
    fout = codecs.open(schema_result_file_path, 'w', encoding='utf-8')
    for item in schema_result:
        strObj = json.dumps(item, ensure_ascii=False)
        fout.write(strObj + '\n')

        content = item['s']
        creatAt = item['creatAt']
        deleteFlag = item['deleteFlag']
        extractScope = item['extractScope']
        humanFlag = item['humanFlag']
        id = item['id']
        infoId = item['info_id']  # 每一个句子的id
        ners = item['ners']
        occurAt = item['occurAt']
        paragraph = item['p']
        publishAt = item['publishAt']
        schema = item['schema']
        schemaType = item['schemaType']

        if content != '':
            logger.info('content: ' + str(content))
            logger.info('creatAt: '+str(creatAt))
            logger.info('deleteFlag: '+str(deleteFlag))
            logger.info('extractScope: '+str(extractScope))
            logger.info('humanFlag: '+str(humanFlag))
            logger.info('id: '+str(id))
            logger.info('infoId: '+str(infoId))
            logger.info('ners: '+str(ners))
            logger.info('occurAt: '+str(occurAt))
            logger.info('paragraph: '+str(paragraph))
            logger.info('publishAt: '+str(publishAt))
            logger.info('schema: '+str(schema))
            logger.info('schemaType: ' + str(schemaType))
            logger.info('--------------------------')


def save_schema_result_to_api(schema_result):
    save_schema_url = 'http://eventengine-persistent-operator:31001/schema'

    for item in schema_result:

        content = item['s']
        createAt = item['createAt']
        deleteFlag = item['deleteFlag']
        extractScope = item['extractScope']
        humanFlag = item['humanFlag']
        id = item['id']
        infoId = item['info_id']  # 每一个句子的id
        ners = item['ners']
        occurAt = item['occurAt']
        paragraph = item['p']
        publishAt = item['publishAt']
        schema = item['schema']
        schemaType = item['schemaType']

        schema_key = [{
            "content":content,
            "createAt": createAt,
            "deleteFlag": deleteFlag,
            "extractScope": extractScope,
            "humanFlag": humanFlag,
            "id": id,
            "infoId": infoId,
            "ners": ners,
            "occurAt": occurAt,
            "paragraph": paragraph,
            "publishAt": publishAt,
            "schema": schema,
            "schemaType": schemaType,
        }]

        json_schema = json.dumps(schema_key).encode("UTF-8")
        if content != '':
            try:
                requests.post(url=save_schema_url,data=json_schema,headers={'Connection': 'close'})
            except Exception as e:
                logger.exception("Exception: {}".format(e))
                logger.exception("POST json data error")


if __name__ == '__main__':
    
    print('save_cluster_result...')
