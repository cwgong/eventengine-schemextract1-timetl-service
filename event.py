# -*- coding: utf-8 -*-

import re
import io
import json
import requests
# from ltp_class import HIT_LTP
import model_loading as mdld
import uuid
from time_utils import timestamp_to_date,current_time
import fixativedomain_loading as fdld
import logging.config

logging.config.fileConfig("logging.conf")
logging = logging.getLogger('main')

class Event_Supervision():

    def __init__(self):
        # MODELDIR = 'ltp_data_v3.4.0'
        # self.hit_ltp = HIT_LTP(MODELDIR)
        self.ner_type = ['mg', 'gg', 'st', 'hy', 'bg', 'nr', 'nt', 'rw', 'fss', 'jj', 'hgzb', 'zczt', 'hylx', 'zqgs']
        self.neg_sub = ['公司', '该公司', '我省', '记者', '这']
        self.neg_v = ['获悉','截止','如下','显示','有','满','工作','共有','没','是','远离','称','说','表示','认为','指出','强调']
        logging.info("Event_Supervision initial ... ")

    # 从不同的接口获取 event schema
    def get_event_schema_(self,doc):
        # doc = json.loads(line)
        info_id = doc['id']
        publishAt = doc['publishAt']
        title = doc['title'].strip()
        abstract = doc['abstract'].strip()

        logging.info("title: {}".format(title))
        logging.info("abstract: {}".format(abstract))

        att_eventype_flag = 0
        # 考虑 event_type, scope, source 事件类型、（篇章级、句子级），（资讯、研报、公告）
        # 首先固定域篇章级

        # 篇章级过完再过句子级
        title_ = self.semantic_clean(title)
        title_ = title.replace(" ", "。").replace("\t", "。").replace("；", "。").replace(";", "。").replace("，",
                                                                                                        "。").replace(
            ",", "。").replace("  ", "。")
        abstract_ = self.semantic_clean(abstract)
        abstract_ = abstract_.replace(" ", "。").replace("\t", "。").replace("；", "。").replace(";", "。").replace("，",
                                                                                                               "。").replace(
            ",", "。").replace("  ", "。")
        s_list = abstract_.split("。") + title_.split("。")
        schemas = []
        # 先进行篇章级的抽取，篇章级无法抽取的再进一步进行句子级别或者开放域的抽取;该部分认为一篇文章可以有多个篇章级固定域类型
        schemas = fdld.extract_schema.get_schema_article(doc)

        if len(schemas) > 0:
            for item in schemas:
                # pass
                ners = []
                schema_info = {}
                schema_id = str(uuid.uuid1()).replace('-', '')
                createAt = current_time()
                schema_info['id'] = schema_id
                schema_info['infoId'] = info_id
                schema_info['content'] = abstract
                schema_info['paragraph'] = abstract
                schema_info['extractScope'] = "固定域篇章级"
                schema_info['schemaType'] = item[1]
                schema_info['sourceType'] = "资讯"
                schema_info['schema'] = item
                schema_info['ners'] = ners  # 此处ner怎么获取,或者也是用ltp包来获取ner,或者是对提取出来的schema进行ner识别
                schema_info['publishAt'] = publishAt
                schema_info['occurAt'] = publishAt
                # schema_info['createAt'] = createAt
                # schema_info['deleteFlag'] = "0"
                # schema_info['humanFlag'] = "0"

        if schemas != []:
            return schemas
        # 篇章级抽取的输入为整个文章信息，句子级别的抽取输入为某一个句子
        for s in s_list:

            TMP = self.get_standard_datetime(s, publishAt)

            if len(s.strip()) < 6:  # 太短的句子不做处理
                # continue
            # 固定域句子级抽取
            # 直接调用schema抽取的服务
            #     fixativedomain_url = ''
            #     schema_param = {}
            #     schema_param['s'] = s
            #     schema_param['publishAt'] = publishAt
            #     schema_param = json.dumps(schema_param).encode('UTF-8')
            #     response = requests.post(url=fixativedomain_url,data = schema_param)
            #     schema_response = response.json()
                schema_response = fdld.extract_schema.get_schema_sen(s,publishAt)

                # 得到返回的一句话所有的schema列表后，遍历得到每一个schema，然后给schema加上相对应的句子外部信息
                if len(schema_response) > 0:
                    for item in schema_response:
                        # pass
                        ners = []
                        schema_info = {}
                        schema_id = str(uuid.uuid1()).replace('-', '')
                        createAt = current_time()
                        schema_info['id'] = schema_id
                        schema_info['infoId'] = info_id
                        schema_info['content'] = s
                        schema_info['paragraph'] = abstract
                        schema_info['extractScope'] = "固定域句子级"
                        schema_info['schemaType'] = item[1]
                        schema_info['sourceType'] = "资讯"
                        schema_info['schema'] = item
                        schema_info['ners'] = ners  #此处ner怎么获取,或者也是用ltp包来获取ner,或者是对提取出来的schema进行ner识别
                        schema_info['publishAt'] = TMP
                        schema_info['occurAt'] = TMP
                        # schema_info['createAt'] = createAt
                        # schema_info['deleteFlag'] = "0"
                        # schema_info['humanFlag'] = "0"
                        schemas.append(schema_info)

                        att_eventype_flag += 1


                # 开放域句子级抽取（如果固定域不论篇章级还是句子级抽取过，则开放域都不抽取）
            if att_eventype_flag == 0:
                # 首先过滤掉句式复杂的或对于事件描述模糊的句子
                if not self.s_filter(s):
                    # 利用自己领域的分词 + ltp 的 parser
                    s_seg = self.split_sentence(s)
                    # 开放域抽取的前提是句子中必须出现 ner
                    ori_ner_info = [seg for seg in s_seg if seg['nature'] in ['ns', 'nt', 'nr'] or len(
                        set(seg['ner'].split(',')) & set(self.ner_type)) > 0]
                    if len(ori_ner_info) == 0:
                        continue
                    # print(222222222222222222222)
                    # TMP = self.get_standard_datetime(s, publishAt)
                    # print(3333333333333333333333333333)
                    s_seg = mdld.hit_ltp.std_seg_with_hanlp(s,
                                                            hanlp_terms=s_seg)  # 需要利用 hanlp 分词 +  ltp 词性 进行 dp parser
                    s_seg = self.special_entity_merge_segment(s, s_seg)  # 处理 《》、（）等语义完备的实体词
                    words = [term['word'] for term in s_seg]
                    postags = [term['nature'] for term in s_seg]
                    result = mdld.hit_ltp.get_parser_triple(s, words=words, postags=postags)
                    core_words_info = result['core_words_info']
                    triple_info = result['triple_info']
                    ner_info = result['ner_info']
                    core_words = [item['word'] for item in core_words_info]
                    for triple in triple_info:
                        if self.triple_filter(triple, ori_ner_info):  # triple 过滤条件
                            continue
                        if triple['triple'][1] in core_words:
                            schema_info = {}
                            schema = [{"name": triple['triple'][0],
                                       "oriName": triple['triple'][0],
                                       "necessary": 1,
                                       "spanStart": None,
                                       "type": "Sub"},
                                      {"name": triple['triple'][1],
                                       "oriName": triple['triple'][1],
                                       "necessary": 1,
                                       "spanStart": None,
                                       "type": "v"},
                                      {"name": triple['triple'][2],
                                       "oriName": triple['triple'][2],
                                       "necessary": 1,
                                       "spanStart": None,
                                       "type": "Obj"}]
                            # ners = ori_ner_info
                            ners = []
                            for item in ori_ner_info:
                                ner = {}
                                ner['name'] = item['word']
                                ner['type'] = item['nature']
                                ner['spanStart'] = item['offset']
                                ner['oriName'] = item['realName']
                                ner['necessary'] = 1
                                ners.append(ner)

                            schema_id = str(uuid.uuid1()).replace('-', '')
                            createAt = current_time()
                            schema_info['id'] = schema_id
                            schema_info['infoId'] = info_id
                            schema_info['content'] = s
                            schema_info['paragraph'] = abstract
                            schema_info['extractScope'] = "开放域句子级"
                            schema_info['schemaType'] = triple['triple'][1]
                            schema_info['sourceType'] = "资讯"
                            schema_info['schema'] = schema
                            schema_info['ners'] = ners
                            schema_info['publishAt'] = TMP
                            schema_info['occurAt'] = TMP
                            # schema_info['createAt'] = createAt
                            # schema_info['deleteFlag'] = "0"
                            # schema_info['humanFlag'] = "0"
                            schemas.append(schema_info)

                            logging.info(
                                "triple: 【{}】-【{}】-【{}】-sentene：{}".format(triple['triple'][0], triple['triple'][1],
                                                                           triple['triple'][2], s))
                            logging.info("ners: {}".format([x['name'] for x in ners]))
                            logging.info("TMP: {}".format(timestamp_to_date(int(TMP)).split(' ')[0]))

        return schemas


    # 因为之前调用已经是一篇文章一篇文章进行调用，所以此处希望对一篇文章的相关信息传入，然后进行相关的schema提取
    def get_event_schema(self, data_file_):
        c = 0
        schemas = []
        with io.open(data_file_, "r", encoding='utf-8') as f:
            while True:
                line = f.readline()
                if len(line) > 0 and c < 10:
                    c+=1
                    print(c)
                    schemas = self.get_event_schema_(line)

                else:
                    break
                
        print(len(schemas))
        return schemas
        
    def get_articlevel_eventype(self, title, abstract):
        
        return ''
        
        
    def get_senlevel_eventype(self, s):
        
        return ''
    
    def triple_filter(self, triple, ner_info):
        if triple['triple'][0] == "": # 主语缺失不为事件
            return 1
        if triple['triple'][0] in self.neg_sub:
            return 1
        if triple['triple'][1] in self.neg_v:
            return 1
        
        # 如果主语或宾语中不包含 ner，进行过滤
        condition = 0
        sub_obj = triple['triple'][0]+triple['triple'][1]
        ners = [x['word'] for x in ner_info]
        for ner in ners:
            if ner in sub_obj:
                condition += 1
                break
        if condition == 0:
            return 1
        return 0
        
    # 去 “电” 头、去括号、【】 等，用于事件抽取
    def semantic_clean(self, text):
        '''
        # 可能是开头，也可能是结尾，所以需要判断索引位置
        # 理论上一个新闻 text 中只会存在一个 “电头” 
        features = ['日电','日讯','日消息','日报道','网讯','网消息']
        for fea in features:
            if fea in text:
                fea_ids = text.index(fea)
                if fea_ids < int(1/2 * len(text)):
                    text = text[fea_ids+len(fea):]
                    break
        '''
        # 剔除掉 （）、() 中的 “不规范信息”
        special_signs = ["(", "（", "【", "[", '<']
        signs_infos_list = self.get_special_chunk(text)
        for item in signs_infos_list:
            if item['type'] in special_signs:
                text = text.replace(item['chunk_str'], '')
        return text
    
    # 抽取出 text 中所有的 special sign string 及 offset
    def get_special_chunk(self, text):
        signs_infos_list = []
        special_signs = [['(', ')'], ['（', '）'], ['<','>'],['《', '》'], ['【', '】'],['[',']'],['{','}'],
                         ['「', '」'], ['‘', '’'], ['\"', '\"'],['“', '”'], ['\'', '\'']]
        special_signs_rgx_info = []
        for i in range(0,len(special_signs)):
            rgx = re.compile(r'[{0}](.*?)[{1}]'.format(special_signs[i][0],special_signs[i][1]))
            type = special_signs[i][0]
            temp_dic = {}
            temp_dic['rgx'] = rgx
            temp_dic['type'] = type
            special_signs_rgx_info.append(temp_dic)
        for x in special_signs_rgx_info:
            item = x['rgx']
            type = x['type']
            item_rgx = item.finditer(text)
            if item_rgx is not None:
                for m in item_rgx:
                    signs_infos = {}
                    signs_infos['offset'] = m.span()
                    signs_infos['chunk_str'] = m.group(0)
                    signs_infos['type'] = type
                    signs_infos_list.append(signs_infos)
        return signs_infos_list

    def special_entity_merge_segment(self, s, segs):
        signs_infos_list = self.get_special_chunk(s)
        words_info = {}
        for sign_info in signs_infos_list:
            offset_start = sign_info['offset'][0]
            words_info[offset_start] = {}
            words_info[offset_start]['chunk_str'] = sign_info['chunk_str']
            words_info[offset_start]['offset_end'] = sign_info['offset'][1]
            words_info[offset_start]['type'] = sign_info['type']
        segs_ = []
        new_word = None
        end_offset = None
        for seg in segs:
            offset_start = seg['offset']
            if offset_start == end_offset:
                new_word = None
                end_offset = None
            if offset_start in words_info and end_offset is None:
                new_word = words_info[offset_start]['chunk_str']
                seg['word'] = new_word
                seg['offset'] = offset_start
                seg['nature'] = 'n'
                segs_.append(seg)
                end_offset = words_info[offset_start]['offset_end']
            if new_word is None:
                segs_.append(seg)
        return segs_

    def s_filter(self, s):
        features = ['格隆汇','龙虎榜', '罚决字', '丨', '|','？', 
                    '：', '【','[','!',':', '！','?']
        for fea in features:
            if fea in s:
                return 1
        # 利用词法句法分析初步判断哪些句子“语义不完备”主要为缺失主语
        terms = self.split_sentence(s)
        nature_list = [term['nature'] for term in terms]
        # 这、也、并、且、和、及、以及
        if len(nature_list) > 0:
            if nature_list[0].startswith(('c', 'd', 'r')):
                return 1
        condition = 0
        # 默认为句子长度，因为 存在 增持 nz，且假设句子成立必须存在谓词
        v_idx = len(nature_list)
        for i in range(len(nature_list)):
            if nature_list[i].startswith('v'):
                v_idx = i
                break
        for nature in nature_list[0: v_idx]:
            if 'n' in nature:
                condition += 1
                break
        if condition ==0:
            return 1
        return 0
        
    def split_sentence(self, sen):
        nlp_url = 'http://hanlp-nlp-service:31001/hanlp/segment/segment'
        try:
            cut_sen = dict()
            cut_sen['content'] = sen
            cut_sen['customDicEnable'] = True
            data = json.dumps(cut_sen).encode("UTF-8")
            cut_response = requests.post(nlp_url, data=data, headers={'Connection':'close'})
            cut_response_json = cut_response.json()
            return cut_response_json['data']
        except Exception as e:
            logging.exception("Exception: {}".format(e))
            logging.exception("hanlp-nlp-service error")
            logging.exception("sentence: {}".format(sen))
            return []
        
    def get_standard_datetime(self, sen, publishAt):
        url = 'http://datetime-featurextract-service:31001/datetime'
        TMP = ''
        try:
            params = dict()
            params['content'] = sen
            params['publishAt'] = publishAt
            params = json.dumps(params).encode("UTF-8")
            response = requests.post(url, data=params, headers={'Connection':'close'})
            response_json = response.json()
        except Exception as e:
            logging.exception("Exception: {}".format(e))
            logging.exception("get_standard_datetime error")
            return publishAt
        for item in response_json:
            if item['type'] == 'TMP':
                TMP = item['time_stamp'][0]
                return TMP
        for item in response_json:
            TMP = item['time_stamp'][0]
            return TMP
        return TMP
    
    def release(self):
        mdld.hit_ltp.release()
        
        
                
    
if __name__ == '__main__':
    
    event_supervision = Event_Supervision()
    
    s = '8月全国乘用车市场共售出新车156.4万辆'
    s = '<p><p>7月25日午间公告，公司董事会沉痛公告，近日从独立董事梁烽先生家属获知，梁烽先生因病不幸逝世。梁烽先生现任公司第一届董事会独立董事、审计委员会主任委员。</p></p><p><p>梁烽先生去世后，公司董事会成员减少至8人，其中独立董事减少至2人，导致公司董事会中独立董事所占比例低于1/3，根据相关法律、法规规定，公司董事会将尽快按照相关程序增补新的独立董事并及时公告。在新的独立董事选举产生之前，公司独立董事事务暂由陈汉亭先生、彭丽霞女士两位独立董事履行。</p></p><p><p>习近平指出，这是最后一个晚上</p></p>'
    result = []

    abstract_info = {}
    abstract_info['id'] = '121313123123'
    abstract_info['title'] = '光弘科技独立董事梁烽先生逝世'
    abstract_info['publishAt'] = '1571919900476'
    abstract_info['abstract'] = s

    result.extend(event_supervision.get_event_schema_(abstract_info))
    print(result)
    # TMP = event_supervision.get_standard_datetime(s, 1546272000000)
    #
    # print(TMP)
    #
    #
    # event_supervision.release()
    
    
    
    
    
    
    
    
    
    
    pass