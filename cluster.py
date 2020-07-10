# -*- coding: utf-8 -*-

import io
import logging

class Cluster():

    def __init__(self):
        
        self.synonym_info = self.load_synonym('./WordsDic/CoreSynonym.txt')
        logging.info("Cluster initial ... ")

    def load_synonym(self, file_path):
        synonym_info = {}
        with io.open(file_path, "r", encoding='utf-8') as f:
            while True:
                line = f.readline()
                line = line.strip()
                if len(line) > 0:
                    if '=' in line:
                        words_in_line = line.split('=')[1].strip().split(' ')
                        #print(words_in_line)
                        for word in words_in_line:
                            if word not in synonym_info:
                                synonym_info[word] = set(words_in_line)
                            else:
                                synonym_info[word] = synonym_info[word] | set(words_in_line)
                else:
                    break
        return synonym_info
    
    def sort(self, clusters):
        
        result = sorted(clusters, key=lambda x:len(x['schema_ids']), reverse = True)
        return result
    
    # 1、固定域 schema 的 clustering（merge）
    # 2、开放域 schema 的 clustering（merge）
    def clustering(self, ori_clusters, schemas):
        
        for i in range(len(schemas)):
            print('schemas_clustering process schema count: ', i)
            schema = schemas[i]
            condition = 0 
            for j in range(len(ori_clusters)):
                # cluster = {}
                cluster = ori_clusters[j]
                score = self.merge_condition(schema, cluster)
                if score == 1:
                    condition += 1
                    # 更新簇相关信息
                    cluster_ = self.cluster_update(cluster, schema)
                    ori_clusters[j] = cluster_
                    break
    
            if condition == 0:
                self.clusters_add(ori_clusters, schema)
        
        return ori_clusters
        
    def cluster_update(self, cluster, schema):
        
        # 更新 cluster
        cluster['schema_ids'].append(schema['id'])
        cluster['info_ids'].append(schema['info_id'])
        schemas = cluster['schemas']
        schemas.append(schema)
        cluster['schemas'] = schemas
        # 重新统计 选出权重较高的 schema info 作为 cluster info，cluster id 不变 
        # 要保持 schema、info_id、s、p、publishAt 的一致性
        sort_dic = {}
        for schema_info in schemas:
            key = ''
            for role_info in schema_info['schema']:
                if role_info['necessary'] == 1:
                    key += role_info['name'] + '_'
            
            if key not in sort_dic.keys():
                sort_dic[key] = {'schema': schema_info,
                                 'count': 1}
            else:
                sort_dic[key]['count'] += 1
        
        x = sorted(sort_dic.items(), key=lambda d:d[1]['count'], reverse = True)
        for key, value in x[0][1]['schema'].items():
            if key != 'id':
                cluster[key] = value
                       
        return cluster
        
        
    def clusters_add(self, ori_clusters, schema):
        
        temp_dic = schema
        temp_dic['schema_ids'] = [schema['id']]
        temp_dic['info_ids'] = [schema['info_id']]
        temp_dic['schemas'] = [schema]
        ori_clusters.append(temp_dic)
        
    # 动词会存在近义词，如 发布、颁发、印发、考虑利用近义词表进行归并
    # 主语或宾语存在如 “习近平”、“习近平主席”、“国家主席习近平”、“外商投资法配套法规”、“《外商投资法》配套法规”
    def merge_condition(self, schema, cluster):
        
        if '固定域' in cluster['extractScope'] and '固定域' in schema['extractScope']:
            # 事件类型必须相同
            if cluster['schemaType'] == schema['schemaType']:
                # 'necessary' == 1 ？:
                pass
            
        # 目前只有谓词同义，如果开放域 slot 都同义或近义意味着 生成 事件类型
        if '开放域' in cluster['extractScope'] and '开放域' in schema['extractScope']:
            
            for i in range(0, len(cluster['schema'])):
                if cluster['schema'][i]['type'] == 'v':
                    v = cluster['schema'][i]['name']
                    v_ = schema['schema'][i]['name']
                if cluster['schema'][i]['type'] == 'Sub':
                    sub = cluster['schema'][i]['name']
                    sub_ = schema['schema'][i]['name']
                if cluster['schema'][i]['type'] == 'Obj':
                    obj = cluster['schema'][i]['name']
                    obj_ = schema['schema'][i]['name']
            try:
                sub_score = len(set(sub)&set(sub_)) / min([len(set(sub)), len(set(sub_))])
            except:
                sub_score = 0
                
            # 排除掉空字符串的比较 ‘’与‘’
            if sub == sub_:
                sub_score = 1
                
            try:
                obj_score = len(set(obj)&set(obj_)) / min([len(set(obj)), len(set(obj_))])
            except:
                obj_score = 0
            
            if obj == obj_:
                obj_score = 1
            
            # 动作的包含关系
            v_score = len(set(v)&set(v_)) / min([len(set(v)), len(set(v_))])
            
            if v in v_ or v_ in v:
                v_score = 1
            # 动作的同义关系
            if v in self.synonym_info:
                if v_ in self.synonym_info[v]:
                    v_score = 1
            if v_ in self.synonym_info:
                if v in self.synonym_info[v_]:
                    v_score = 1
            if sub_score > 0.66 and obj_score > 0.66 and v_score > 0.66 :
                return 1
            
            return 0
        
        return 0
        
