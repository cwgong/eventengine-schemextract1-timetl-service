# -*- coding: utf-8 -*-

import re
import logging

class Abstract_Supervision():

    def __init__(self):
        
        self.features = ['日电','日讯','日消息','日报道','网讯','网消息','网报道']
        self.date_regex = re.compile('(.*)(\d日)')
        self.date_features = ['日前', '近日', '昨日', '今日']
        logging.info("Abstract_Supervision initial ... ")
        
    def get_abstract(self, paragraphs):
        
        # 参数：paragraphs
        # return ''
        #    每篇资讯先进行分段（通过永焕给出的规则 ***重要*** ）
        # 假设：
        #   1、每篇资讯最多只讲一件最主要的「事件」（也可能不讲）
        #   2、这个主要「事件」出现在开篇处
        # 规则：
        #   1、先找新闻资讯中所有段落的转述型事件特征（全局）
        #   2、若没有关键特征，则找第一个满足文本长度要求且存在「时间」的段
        
        RPT_idx = []
        TMP_idx = []
        for i in range(len(paragraphs)):
            p = paragraphs[i]
            edr = self.abstract_rule(p)
            if edr == 'RPT':
                RPT_idx.append(i)
            if edr == 'TMP':
                TMP_idx.append(i)
                
        if len(RPT_idx) != 0:
            return paragraphs[RPT_idx[0]]
        if len(TMP_idx) != 0:
            return paragraphs[TMP_idx[0]]
        return ''
     
        
    # 1、字数限制
    # 2、日期与动词
    # 3、尽量不用调用分词，速度问题
    def abstract_rule(self, p):
    
        if len(p) > 20 and len(p) < 500:
            
            #if '摄' in p and len(p) < 60:
             #   return 0
   
            for feature in self.features:
                if feature in p:
                    return 'RPT'
            
            if self.date_regex.match(p) is not None:
                return 'TMP'
                
            for df in self.date_features:
                if df in p:
                    return 'TMP'
        return ''
        
    def split(self, content, dataSource):
        # 爬虫数据进行分段 
        # 1、char.strip() 与 FullToHalf(char.isdigit())
        # 2、'</p><p>' 与 '</p></p><p><p>'
        # 3、removeAllTag(p) 去掉 p = “”
    
        content_ = ''
        for char in content:
            #char = char.strip()
            if len(char) != 0:
                if char.isdigit():
                    char = self.FullToHalf(char)
                content_ += char
        
        paragraphs = []
        if dataSource == "CRAWL":
            paragraphs = content_.split('</p><p>')
        else:
            paragraphs = content_.split('</p></p><p><p>')
        
        paragraphs = [self.removeAllTag(p) for p in paragraphs if len(self.removeAllTag(p).strip()) != 0]
        
        return paragraphs
    
    def removeAllTag(self, s):
        s = re.sub('<[^>]+>','',s)
        return s
    
    def FullToHalf(self, ustring):  
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

if __name__ == '__main__':
    
    
    paragraphs = ['18日上午，习近平专门听取兰考县教育实践活动情况汇报，并发表重要讲话。他指出，标准决定质量，有什么样的标准就有什么样的质量，只有高标准才有高质量。教育实践活动要确立一个较高标准，并严格按标准抓部署、抓落实、抓检查。要整合好组织资源、人力资源、社会资源、政策资源，使与活动相关的各种因素同向着力、相互协调。要把握好节律，解决复杂矛盾先行探索，用成功经验和管用办法示范带动。要用好批评和自我批评武器，有一点“辣味”，让每个党员干部都能红红脸、出出汗。要坚持开门搞活动，让群众大胆提意见、评头品足，特别是对群众提出的一些具体问题，能够解决的要抓紧解决，一时解决不了的要耐心细致做好解释工作，需要上级决策或制定政策的要及时反映。要严格督导把关，及时发现和帮助解决工作推进中的苗头性、倾向性问题。',
                  '18日上午，习近平专门听取兰考县教育实践活动情况汇报，并发表重要讲话。他指出，标准决定质量，有什么样的标准就有什么样的质量，只有高标准才有高质量。教育实践活动要确立一个较高标准，并严格按标准抓部署、抓落实、抓检查。要整合好组织资源、人力资源、社会资源、政策资源，使与活动相关的各种因素同向着力、相互协调。要把握好节律，解决复杂矛盾先行探索，用成功经验和管用办法示范带动。要用好批评和自我批评武器，有一点“辣味”，让每个党员干部都能红红脸、出出汗。要坚持开门搞活动，让群众大胆提意见、评头品足，特别是对群众提出的一些具体问题，能够解决的要抓紧解决，一时解决不了的要耐心细致做好解释工作，需要上级决策或制定政策的要及时反映。要严格督导把关，及时发现和帮助解决工作推进中的苗头性、倾向性问题。',
                  '习近平还对兰考县结合教育实践活动抓好当前改革发展稳定各项工作提出明确要求，希望他们把强县和富民统一起来，把改革和发展结合起来，把城镇和乡村贯通起来，不断取得事业发展新成绩。',
                  '据新华社郑州3月18日电  中共中央总书记、国家主席、中央军委主席习近平近日在河南省兰考县调研指导党的群众路线教育实践活动时强调，要准确把握第二批教育实践活动的总体要求、实践载体、重点对象、组织指导原则、特点规律，大力学习弘扬焦裕禄精神，坚持高标准严要求，在对标立规中查找差距，在上下互动中解决问题，在攻坚克难中提振信心，在思考辨析中把握规律，确保每个层级每个单位都真正取得实效。',
                  '根据中央统一安排，中央政治局常委在第二批教育实践活动中分别联系一个县，习近平联系兰考县。17日至18日，习近平深入农村和窗口服务单位，同干部群众交流座谈、听取意见和建议，实地指导兰考县教育实践活动。',
                  '17日上午，习近平一到兰考，就直接前往焦裕禄同志纪念馆。一幅幅图片、一件件实物、一个个故事，生动展现了焦裕禄的音容笑貌和感人事迹，习近平边看边问，不时驻足。他同焦裕禄亲属和基层模范干部代表亲切交流并合影留念，动情地说，我们这一代人是深受焦裕禄同志事迹教育成长起来的，焦裕禄同志的形象一直在我心中。5年前我到兰考参观了焦裕禄同志事迹展，今天来再次深受感动，引起心灵的共鸣。焦裕禄同志是县委书记的榜样，也是全党的榜样，他虽然离开我们50年了，但他的事迹永远为人们传颂，他的精神同井冈山精神、延安精神、雷锋精神等革命传统和伟大精神一样，过去是、现在是、将来仍然是我们党的宝贵精神财富，我们要永远向他学习。前来参观学习的干部群众纷纷向总书记问好。习近平走上前去同他们握手，祝他们学有所获。']
    
    
    
    
    