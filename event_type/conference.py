# -*- coding: utf-8 -*-
import sys 
sys.path.append('../')


    #外事
    def extract_affairs(self,title,content=None,mediaFrom=None):
        #  
        study_opt='介绍'
        set_study_opt_regex=r'(({}).*(访问|会谈|会晤|磋商).*(成果))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return None
    
        if title.endswith('将访华') or title.endswith('访问') :
            return '会见访问|访问'
        
        
        if '访问' in title:
            words = pseg.cut(title)
            words =list(words)
            for i in range(len(words)-1):
                if '访问' == words[i].word and i:
                    for j in range(i):
                        if words[j].flag in ['rm','nr']:
                            return '会见访问|访问'
                if '访问' == words[i].word and i+1<len(words) and words[i+1].flag in ['ns'] :
                    return '会见访问|访问'
        if '首访' in title:
            words = pseg.cut(title)
            words =list(words)
            for i in range(len(words)):
                if '首访' == words[i].word and i+1<len(words) and words[i+1].flag in ['ns']:
                    return '会见访问|访问'
                
        
        
        study_opt='举行|出席|主持'
        set_study_opt_regex=r'(({}).*(会晤))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会见访问|会晤'
        study_opt='会晤'
        set_study_opt_regex=r'(({}).*(举行|落幕|出席|开幕))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会见访问|会晤'
      
        study_opt='举行|出席'
        set_study_opt_regex=r'(({}).*(磋商))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会见访问|磋商'
        
        study_opt='磋商'
        set_study_opt_regex=r'(({}).*(开幕|结束|举行))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会见访问|磋商'
        
        study_opt='驻'
        set_study_opt_regex=r'(({}).*(拜会|拜见))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会见访问|拜会'
      
        if '拜会' in title or '拜见' in title:
            words = pseg.cut(title)
            words =list(words)
            for i in range(len(words)):
                if ('拜会' == words[i].word and i and i<len(words))or ('拜见' == words[i].word and i and i<len(words)):
                    if words[i-1].flag in ['rm','nr'] or  words[i+1].flag in ['rm','nr']:
                        return '会见访问|拜会'
                    if words[i-1].word in ['辞行','省长','到任','上任','部长'] and words[i-2].flag in ['rm','nr'] and i-1:
                        return '会见访问|拜会'
                    if i+1 < len(words) and words[i+1].flag in ['ns'] and i+2 < len(words) and words[i+2].flag in ['jg'] :
                        return '会见访问|拜会'
                    if words[i+1].flag in ['jg'] and i+1 < len(words):
                        return '会见访问|拜会'
    #会议
    def extract_meeting(self,title,content=None,mediaFrom=None):
        

        if  '会议' in title and ('：'  in title  or ':'  in title or '解码'  in title or '解析'  in title):
            
            return  None

        if '新闻发布会' in title:
            return  None

        study_opt='关于'
        set_study_opt_regex=r'(({}).*(的决议))'.format(study_opt)
        meeting1=re.findall(set_study_opt_regex, title.strip())
        study_opt='通过'
        set_study_opt_regex=r'(({}).*(决议|决议草案))'.format(study_opt)
        meeting2=re.findall(set_study_opt_regex, title.strip())
        if title.endswith('会议决议') or meeting1 or meeting2:
            return '会议报道'
        #习近平同XXX集体谈话
        study_opt='习近平同'
        set_study_opt_regex=r'(({}).*(集体谈话))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        
        study_opt='在'
        set_study_opt_regex=r'(({}).*(会议上作|会上作).*(报告))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        study_opt='会议'
        set_study_opt_regex=r'(({}).*(公报))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        
        study_opt='出席|参加'
        set_study_opt_regex=r'(({}).*(冬季达沃斯|亚洲金融论坛|中国经济前瞻论坛|中国经济50人论坛|亚布力中国企业家论坛|博鳌亚洲论坛|鳌论坛|中国发展高层论坛|陆家嘴论坛|一带一路高峰论坛|中国金融四十人论坛|夏季达沃斯|东方经济论坛|中国国际进口博览会|正和岛新年论坛|金麒麟论坛|APEC))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        study_opt='冬季达沃斯|亚洲金融论坛|中国经济前瞻论坛|中国经济50人论坛|亚布力中国企业家论坛|博鳌亚洲论坛|鳌论坛|中国发展高层论坛|陆家嘴论坛|一带一路高峰论坛|中国金融四十人论坛|夏季达沃斯|东方经济论坛|中国国际进口博览会|正和岛新年论坛|金麒麟论坛|APEC'
        set_study_opt_regex=r'(({}).*(召开|开幕|闭幕))'.format(study_opt)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        
        opt_regex='《.*》'
        if title:
            tmpcont=re.findall(opt_regex, title.strip())
            if tmpcont:
                if '举办' in tmpcont[0] or '参加' in tmpcont[0] or '出席' in tmpcont[0] or '参观' in tmpcont[0] or '召开' in tmpcont[0] or '举行' in tmpcont[0]:
                    return None
                meeting_name='峰|大|现场|座谈|联席|召开|发布|总结|生活|咨询|宴|检查|论证|博览|赏映|交流|交易|研讨|议|调度|讨论|对接|工作|推进|吹风|培训|评审|协调|学习|部署|推介|动员|启动|年|珠洽|宣讲|次|全|专题|茶话|视频'
                set_meeting_name_regex = "(({})(会))".format(meeting_name)
                meeting=re.findall(set_meeting_name_regex, tmpcont[0].strip())
                if meeting:
                    return None
        meeting_name='集体学习|集中学习|学习|传达学习|专题学习|落实|贯彻'
        set_study_opt_regex=r'((考察|调研).*({}).*(会议|讲话|批示精神|指示精神|会精神|会议精神|讲话精神|重要讲话精神|主旨演讲|主旨讲话|主旨发言))'.format(meeting_name)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            meeting_opt='会|会议'
            set_meeting_opt_regex="(({}).*(召开|举行|开幕|闭幕|举办|学习|传达))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            meeting_opt='主持|参加|出席|召开|主办|举办|举行|学习|传达'
            set_meeting_opt_regex="(({}).*(会|会议))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            return '考察调研'
        
        meeting_name='集体学习|集中学习|学习|传达学习|专题学习|落实|贯彻'
        set_study_opt_regex=r'(({}).*(会议|讲话|批示精神|指示精神|会精神|会议精神|讲话精神|重要讲话精神|主旨演讲|主旨讲话|主旨发言).*(考察|调研))'.format(meeting_name)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            meeting_opt='会|会议'
            set_meeting_opt_regex="(({}).*(召开|举行|开幕|闭幕|举办|学习|传达))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            meeting_opt='主持|参加|出席|召开|主办|举办|举行|学习|传达'
            set_meeting_opt_regex="(({}).*(会|会议))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            return '考察调研'
        
        meeting_name='集体学习|集中学习|学习|传达学习|专题学习|落实|贯彻'
        set_study_opt_regex=r'(({}).*(会议|讲话|批示精神|指示精神|会议精神|会精神|讲话精神|重要讲话精神|主旨演讲|主旨讲话|主旨发言))'.format(meeting_name)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        #if  '会谈' in title or title.endswith('纪实') or title.endswith('通知'):
            
            #return None
        
        #if  '集中学习' in title or '集体学习' in title:
            
            #return '会议'
        ##学习/贯彻 XX指示批示精神
        investigation_opt='学习|落实|贯彻' 
        set_investigation_opt_regex=r'(({}).*(精神))'.format(investigation_opt)
        meeting=re.findall(set_investigation_opt_regex, title.strip()) 
        if meeting:
            return '会议报道'
        
        if ('项目推介会' in title or '讲座' in title or '仪式' in title or '典礼' in title or '活动' in title or '培训' in title or '培训会' in title or '讲坛' in title or '运动会' in title or '培训班' in title or '晚会' in title or '党课' in title or '联欢会'in title or '招待会' in title or '联谊会' in title) and not title.endswith('讲话') and  '学习培训' not in title:
            
            return '活动报道'
        
        
        meeting_name='在'
        set_study_opt_regex=r'(({}).*(上发表讲话|上发表重要讲话))'.format(meeting_name)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return '会议报道'
        

        meeting_name='峰|大|现场|座谈|联席|召开|发布|总结|生活|咨询|宴|检查|论证|博览|赏映|交流|交易|研讨|议|调度|讨论|对接|工作|推进|吹风|培训|评审|协调|学习|部署|推介|动员|启动|年|珠洽|宣讲|次|全|专题|茶话'
        set_meeting_name_regex = "(({})(会))".format(meeting_name)
        meeting=re.findall(set_meeting_name_regex, title.strip())
        if '学习培训' in title or meeting or '会议'  in title or '活动' in title or '培训班' in title or '出席' in title or '参观' in title or '召开' in title or '参加' in title or '举办' in title or '举行' in title or '主持' in title or '开幕' in title or '闭幕' in title or '开展' in title:
            
            meeting_opt='会|会议'
            set_meeting_opt_regex="(({}).*(召开|举行|开幕|闭幕|举办))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            meeting_opt='组织'
            set_meeting_opt_regex="(({}).*(会议))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            meeting_opt='主持|参加|出席|召开|主办|举办|举行'
            set_meeting_opt_regex="(({}).*(会|会议))".format(meeting_opt)
            meeting=re.findall(set_meeting_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            
            meeting_name='在'
            set_study_opt_regex=r'(({}).*(上发表讲话|上发表重要讲话))'.format(meeting_name)
            meeting=re.findall(set_study_opt_regex, title.strip())
            if meeting:            
                return '会议报道'
            
            meeting_name='峰|大|现场|座谈|联席|召开|发布|总结|生活|咨询|宴|检查|论证|博览|赏映|交流|交易|研讨|议|调度|讨论|对接|工作|推进|吹风|培训|评审|协调|学习|部署|推介|动员|启动|年|珠洽|宣讲|次|全|专题|茶话'
            set_study_opt_regex=r'(({})(会议|会).*(发表主旨演讲|发表主旨讲话|发表讲话|发表重要讲话|讲话|演讲|主旨演讲))'.format(meeting_name)
            meeting=re.findall(set_study_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            
            meeting_name='集体学习|集中学习|学习|传达学习|专题学习'
            set_study_opt_regex=r'(({}).*(会议|讲话|批示精神|指示精神|会议精神|讲话精神|重要讲话精神))'.format(meeting_name)
            meeting=re.findall(set_study_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            
            meeting_name='召开'
            set_study_opt_regex=r'(({}).*(集体学习))'.format(meeting_name)
            meeting=re.findall(set_study_opt_regex, title.strip())
            if meeting:
                return '会议报道'
            words = pseg.cut(title)
            words=list(words)
            for i in range(len(words)):
                if words[i].word=='学习' and (words[i-1].word=='集体' or words[i-1].word=='集中' or words[i-1].word=='传达' or words[i-1].word=='专题') and i:
                    for j in range(i):
                        if words[j].flag in ['jg','rm']:
                            return '会议报道'
            meeting0=''
            meeting1=''
            meeting2=''
            meeting3=''
            pattern="<p>(.+?)</p>"
            paragraphs=re.findall(r"<p>(.+?)</p>", content)            
            for   paragraph   in   paragraphs:
                if paragraph:
                    
                    meeting_opt='会|会议'
                    set_meeting_opt_regex="(({}).*(召开|举行|开幕|闭幕|举办))".format(meeting_opt)
                    meeting=re.findall(set_meeting_opt_regex, title.strip())
                    if meeting:
                        return '会议报道'
                    
                    meeting_opt='主持|参加|出席|召开|主办|举办|举行'
                    set_meeting_opt_regex="(({}).*(会|会议))".format(meeting_opt)
                    meeting=re.findall(set_meeting_opt_regex, paragraph.strip())
                    if meeting:
                        meeting1=meeting
                    
                    meeting_opt='会议|主旨|本次|与会'
                    set_meeting_opt_regex="(({})(指出|强调|要求|传达|表示|学习|议程|围绕|发言|发布|通报|总结|讨论|安排|代表|验收|会议|表决))".format(meeting_opt)
                    meeting=re.findall(set_meeting_opt_regex, paragraph[:10].strip())
                    if meeting:
                        meeting2=meeting
        
                    
                    meeting_opt='\S{0,5}'
                    set_meeting_opt_regex="(({})(指出|强调|表示|认为|说|要求))".format(meeting_opt)
                    meeting=re.findall(set_meeting_opt_regex, paragraph[:10].strip())
                    if meeting :
                        #return '会议'
                        words = pseg.cut(meeting[0][0])
                        for word,flag in words:
                            if 'nr' in flag or 'nt' in flag or 'rm' in flag or 'jg' in flag:
                                meeting3=meeting
            if (meeting0 or meeting1) and (meeting2 or meeting3):
                return '会议报道'
            #if '会上' in content or '会前' in content or '会议上' in content:
                
                #return '会议'

            
            return '活动报道'
        
        return None
    #考察调研
    def extract_investigation(self,title,content=None,mediaFrom=None):
        
        #investigation='考察|调研'
        #meeting_name='集体学习|集中学习|学习|传达学习|专题学习|落实|贯彻'
        #set_study_opt_regex=r'((考察|调研).*({}).*(会议|讲话|批示精神|指示精神|会议精神|讲话精神|重要讲话精神|主旨演讲|主旨讲话|主旨发言))'.format(meeting_name)
        #meeting=re.findall(set_study_opt_regex, title.strip())
        #if meeting:
            #return '考察调研'
        meeting_name='峰|大|现场|座谈|联席|召开|发布|总结|生活|咨询|宴|检查|论证|博览|赏映|交流|交易|研讨|议|调度|讨论|对接|工作|推进|吹风|培训|评审|协调|学习|部署|推介|动员|启动|年|珠洽|宣讲|次|全|专题|茶话'
        set_meeting_name_regex = "(({})(会))".format(meeting_name)
        meeting=re.findall(set_meeting_name_regex, title.strip())
        if meeting:
            return None
        meeting_name='集体学习|集中学习|学习|传达学习|专题学习|落实|贯彻'
        set_study_opt_regex=r'(({}).*(会议|讲话|批示精神|指示精神|会精神|会议精神|讲话精神|重要讲话精神|主旨演讲|主旨讲话|主旨发言))'.format(meeting_name)
        meeting=re.findall(set_study_opt_regex, title.strip())
        if meeting:
            return None
        pattern="<p>(.+?)</p>"
        text=re.findall(r"<p>(.+?)</p>", content)
        if not text:
            return None
        investigation_opt='在|去|实地|到|就|赴' 
        set_investigation_opt_regex=r'(({}).*(考察|调研|开展调研|开展考察|看望))'.format(investigation_opt)
        meeting=re.findall(set_investigation_opt_regex, title.strip()) 
        
        if meeting and not title.endswith('纪实') and '调研报告' not in title and '调研会议' not in title and not title.endswith('问答') and not title.endswith('?')and not title.endswith('？'): 
            
            return '考察调研'
        if ('考察' in title or '调研' in title) and '调研报告' not in title and '调研会议' not in title and not title.endswith('纪实')and not title.endswith('问答')and not title.endswith('?')and not title.endswith('？'):
            return '考察调研'
        if '看望' in title:
            words = pseg.cut(title)
            words =list(words)
            for i in range(len(words)):
                if words[i].word=='看望' and words[i-1].flag in ['rm','nr','nrfg'] and i :
                    return '考察调研'
                if words[i].word=='看望' and words[i-1].word in ['亲切','走访'] and (words[i-2].flag in ['rm','nr','nrfg'] or words[i-2].word in ['局长']) and i-1:
                    return '考察调研'
                if words[i].word=='看望' and words[i-1].word in ['部长','领导','大年初一','春节前夕','同志','夫妇','总督'] and i:
                    return '考察调研'
        return None
        
        
    

