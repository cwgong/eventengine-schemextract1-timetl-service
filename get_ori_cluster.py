# -*- coding: utf-8 -*-

# 增量聚类时总需选定一定时间范围的簇
def load_origin_cluster_result(origin_cluster_file_path, end_time, n_reserve_days_for_1size_cluster = 3, n_reserve_days = 3):
    origin_cluster_result = []
    if not os.path.exists(origin_cluster_file_path):
        logger.info("origin_cluster_result ids: {}".format(len(origin_cluster_result)))
        return origin_cluster_result
    with io.open(origin_cluster_file_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if len(line) > 0:
                try:
                    json_data = json.loads(line)
                except:
                    continue
                info_ids = json_data['info_ids']
                length = len(info_ids)
                publish_time = json_data['publish_time']
                # 簇大小为1：去掉时间跨度大于一天的簇
                if length == 1:
                    if end_time - publish_time > int(n_reserve_days_for_1size_cluster*24*60*60*1000):
                        continue
                # 簇大小大于1：去掉时间跨度大于三天的簇
                else:
                    if end_time - publish_time > int(n_reserve_days*24*60*60*1000):
                        continue
                origin_cluster_result.append(json_data)
            else:
                break
    logger.info("origin_cluster_result ids: {}".format(len(origin_cluster_result)))
    return origin_cluster_result