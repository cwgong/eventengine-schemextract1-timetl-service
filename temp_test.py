# -*- coding: utf-8 -*-

import json
import requests
import logging

# data = {}
def requests_post(url, data):
    #print('====================')
    #print(url)
    #print(data)
    data = json.dumps(data).encode("UTF-8")
    
    response = requests.post(url, data = data)
    response = response.json()
    
    return response

# params = {}
def requests_get(url, params):

    response = requests.get(url, params = params)
    print(response)
    response = response.json()
    
    return response

def post_test():
    
    url = 'http://datetime-featurextract-service:31001/datetime'
    #url = 'http://workflow-industrydiscover-service:31001/industryDiscover'
    params={}
    params['content'] = '年是年2月3日是年是年是sada28日电2019年5月21日（星期五）下午８点-5月22日（星期六）上午9时一起去吃饭最后我们吃了米饭sada28日报道'

    params['publishAt']=1549123200000
    article_results = requests_post(url, params)

    print(article_results)

def get_test():
    
    url = 'http://datetime-featurextract-service:31001/datetime'
    #url = 'http://workflow-industrydiscover-service:31001/industryDiscover'
    params={}
    params['content'] = '年是年2月3日是年是年是sada28日电2019年5月21日（星期五）下午８点-5月22日（星期六）上午9时一起去吃饭最后我们吃了米饭sada28日报道'

    params['publishAt']=1549123200000
    article_results = requests_get(url, params =params )

    print(article_results)
    
def get_standard_datetime(sen, publishAt):
    url = 'http://datetime-featurextract-service:31001/datetime'
    try:
        params = dict()
        params['content'] = sen
        params['publishAt'] = publishAt
        params = json.dumps(params).encode("UTF-8")
        response = requests.post(url, data=params, headers={'Connection':'close'})
        response_json = response.json()
        return response_json
    except Exception as e:
        logging.exception("Exception: {}".format(e))
        logging.exception("hanlp-nlp-service error")
        logging.exception("sentence: {}".format(sen))
        return []
    
def FullToHalf(ustring):  
     """全角转半角"""  
     rstring = ""  
     for uchar in ustring:  
         inside_code=ord(uchar)  
         if inside_code == 12288:    #全角空格直接转换              
             inside_code = 32  
         elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化  
             inside_code -= 65248  
        
         rstring += chr(inside_code)  
     
     return rstring
 
def cluster_add(a):
    a.append("xxx")

def cluster_test(a, b):
    def fff():
        print('fff()')
    for i in range(len(b)):
        x = b[i]
        condition = 0 
        for j in range(len(a)):
            if i >3:
                condition +=1
            
        if condition == 0:
            cluster_add(a)
            fff()
    
    
            
    return a
        
if __name__ == "__main__":
    
    #post_test()
    #get_test()
    
    sen = '全国乘联会于9月9日公布了最新一期的国内乘用车销售数据'

    publishAt = 1549123200000
    x = get_standard_datetime(sen, publishAt)
    
    print(x)
    
    a =[1,2,3]
    b = [1,2,3,4,5,6]
    a = cluster_test(a, b)
    print(a)
    
    
    logging.info("schema_info: {}-{}-{}".format(1,"2",'adf'))

    
    
    
    content = 'a b c事件的功夫  啊'
    content_ = ''
    for char in content:
        #char = char.strip()
        if len(char) != 0:
            if char.isdigit():
                char = FullToHalf(char)
            content_ += char
                
                
    print(content_)
                
                
    