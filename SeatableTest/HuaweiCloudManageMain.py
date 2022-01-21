import re
from difflib import SequenceMatcher
from datetime import datetime
from seatable_api import Account

# 获取账户授权。
email = '18909175158@163.com'
password = 'sincere1027'
server_url = 'https://cloud.seatable.cn/'
account = Account(email, password, server_url)
account.auth()

'''
获取所有待处理数据
'''
# 获取两张表的base。
model_base = account.get_base(189828, '配件管理总表')
record_base = account.get_base(189828, '维修记录表')

# 核心、重要配件 中需要获取的列的key。
needful_common_model_keys = '_id,配件型号,配件名称,所属工段,所属设备,最近安装、维修日期,前10次故障日期'
needful_special_model_keys = '_id,配件型号,所属工段,所属设备,最近安装、维修日期,前10次故障日期'
# 获取 普通 和 重要配件 中所有行的上述列。
existing_common_model_list = model_base.query('select ' + needful_common_model_keys + ' from 普通配件')
existing_special_model_list = model_base.query('select ' + needful_special_model_keys + ' from 重要、核心配件')
# 维修记录 中需要获取的列的key。
needful_record_keys = '_id,所属工段,所属设备,普通配件型号,普通配件名称,重要、核心配件型号,故障日期,_ctime,是否已整理'
# 获取 维修记录 和 图片版 中所有行的上述列。
record_list = record_base.query('select ' + needful_record_keys + ' from 维修记录')
pic_record_list = record_base.query('select ' + needful_record_keys + ' from 维修记录（图片版）')
# 获取本次更改前记录的数量。
existing_common_record_num = record_base.list_rows('后台数据')[-1]['总记录量']
existing_pic_record_num = record_base.list_rows('后台数据')[-1]['图片版总记录量']

# 分别创建普通和重要配件更新、追加列表容器。
common_update_data = []
common_append_data = []
special_update_data = []
special_append_data = []
# 创建更新合并记录的容器。
merge_append_data = []
# 创建更新 维修记录 和 图片版 中'是否已整理'为True的容器。
processed_record_update_data = []
processed_pic_record_update_data = []

'''
======================================================================================================
建立所有需要的函数。
'''


def cut_str(to_be_cut_str):
    """
    去除字符串中的符号和空格。
    :param to_be_cut_str:待清理的str
    :return: 清理后的str
    """
    b_cut_str = re.sub(r'_+|\W+', '', to_be_cut_str)
    return b_cut_str


def str_contrast(model1, model2):
    """
    将两个字符串进行对比，
    以判定是否为同一型号。
    :param:str*2
    :return: str or False
    """
    # 设置判定型号一致的标识符。
    consistent = False
    '''
    如果型号完全相同，则判定型号一致。
    '''
    if model1 == model2:
        consistent = True

    # 否则，采用如下对比算法来判定是否为同型号。
    else:
        # =======================================================================================================
        '''
        前后缺字符/字符节中间有空格的判定方式。暂时不用。
        '''
        # 清除两字符串中的符号，并转为小写。
        #    cleaned_model1 = cut_str(model1)
        #    cleaned_model2 = cut_str(model2)
        #    # 比对相似度，若有效字符排序一样，并长度比大于7/10,则判定型号一致。
        #    if (cleaned_model1 in cleaned_model2 and len(cleaned_model1) >= int(len(cleaned_model2) * 0.7)) \
        #    or \
        #    (cleaned_model2 in cleaned_model1 and len(cleaned_model1) > len(cleaned_model2) >= int(
        #            len(cleaned_model1) * 0.7)):
        #            	consistent=True
        # =======================================================================================================

        # 使两字符串只保留汉字。
        model1_cn_only = re.sub(r'[\W_0-9a-zA-Z]+', '', model1)
        model2_cn_only = re.sub(r'[\W_0-9a-zA-Z]+', '', model2)
        """
        如果两者都包含汉字，且汉字占比大于等于3/5，
        则采用Levenshtein对比法。
        """
        # 如果两者都包含汉字，且汉字占比大于等于3/5。
        if len(model1_cn_only) >= len(cut_str(model1)) * 0.6 and len(model2_cn_only) >= len(cut_str(model2)) * 0.6:
            # 取得方位字符列表
            direction_regex = re.compile('轴承|进|出|上|下|左|右|前|后|东|南|西|北|内|外|大|小|长|短|a|b|c|d|[0-9]')
            direction_list1 = direction_regex.findall(model1.lower())
            direction_list2 = direction_regex.findall(model2.lower())
            # 列表完全相同,则进行Levenshtein对比
            if direction_list1 == direction_list2:
                # 原字符串去除所有符号、空格。
                char_2b_clean = r'[\W_]+'
                b_cleaned1 = re.sub(char_2b_clean, '', model1)
                b_cleaned2 = re.sub(char_2b_clean, '', model2)
                # 剩下的字符串进行Levenshtein对比。
                cleaned_lev = SequenceMatcher(None, b_cleaned1, b_cleaned2).quick_ratio()
                # 如果相似度大于0.79（5汉字差一个以内），则判定为同型号。
                if cleaned_lev > 0.79:
                    consistent = True

        else:
            """
            中文占比小于3/5的话，则采用字符节列表对比。
            """
            en_regex = re.compile(r'\bv\d+\.\d+\b|\b\d+.\d+\b|[0-9a-z]+')
            # 获得两字符串中被符号/空格等隔开的字符串切片列表。
            model1_piece_list = en_regex.findall(model1.lower())
            model2_piece_list = en_regex.findall(model2.lower())
            # 如果两列表相同，直接判定型号一致。
            if model1_piece_list == model2_piece_list:
                consistent = True
            # 否则，依次去掉长列表中的一项，再对比。
            else:
                # 判断哪个列表元素多，作为去除其中元素的对象。
                if len(model1_piece_list) < len(model2_piece_list):
                    model1_piece_list, model2_piece_list = model2_piece_list, model1_piece_list

                # 设置一个专门用来修改并做对比的列表，以避免修改原长列表。
                contrast_list = model1_piece_list.copy()
                # 去除列表中的一项。
                for piece in model1_piece_list:
                    contrast_list.remove(piece)
                    # 如与原短列表相同，则判定型号相同，并终止对比。
                    if contrast_list == model2_piece_list:
                        consistent = True
                        break
                    # 如未终止对比，则还原对比列表，重复以上过程。
                    contrast_list = model1_piece_list.copy()

    # 如果判定型号一致，return有效字符长的值(去除左右空格），否则return False。
    if consistent and len(cut_str(model1)) >= len(cut_str(model2)):
        return model1.strip()
    elif consistent and len(cut_str(model1)) < len(cut_str(model2)):
        return model2.strip()
    else:
        return False


def avoid_no_key(row_2b_examined, key_str):
    """
    避免因行中key的value是None而出错。
    :param row_2b_examined:被检查的行
    :param key_str: 行中被检查的key
    :return: 有key，return value;无key,return ''
    """
    if row_2b_examined[key_str]:
        return row_2b_examined[key_str].strip()
    else:
        return ''


def contrast_name(row1, str1, row2, str2):
    """
    名称取值函数，取有名称的行里的名称，
    如果都有名称，取有效字符较长的，
    并去除两侧空格。
    :param row1:dict,其中可能有key:str1
    :param row2:dict,其中可能有key:str2
    :param str1:可能存在于row1的key
    :param str2:可能存在于row2的key
    :return:有效字符长的str，或''
    """
    if row1[str1] is not None and row2[str2] is not None:
        if len(cut_str(row1[str1])) >= len(cut_str(row2[str2])):
            return row1[str1].strip()
        else:
            return row2[str2].strip()
    elif row1[str1]:
        return row1[str1].strip()
    elif row2[str2]:
        return row2[str2].strip()
    else:
        return ''


def average_time(multi_str, single_str):
    """
    计算“前10次故障日期"的str,
    和平均故障间隔
    :param multi_str: 原本的“前10次故障日期"
    :param single_str: 新的故障日期
    :return: 新的“前10次故障日期"的str，和平均故障间隔（天）
    """
    # 合并原有10次故障日期和新故障日期。
    str_of_10times = multi_str + single_str + '/'
    # 把合并后的str转换为单次date的列表。
    regex_10times = re.compile(r'\d{4}-\d\d-\d\d')
    list_10times = regex_10times.findall(str_of_10times)
    # 对列表中的日期进行排序。
    list_10times.sort()
    # 如果列表长度大于10，去除最早的日期，保留10个元素。
    if len(list_10times) > 10:
        list_10times = list_10times[-10:]
        # 并重新计算10次故障日期的str。
        str_of_10times = ''
        for remain_str in list_10times:
            str_of_10times += remain_str + '/'
    # 计算平均故障间隔天数。
    first_time = datetime.strptime(list_10times[0], '%Y-%m-%d')
    last_time = datetime.strptime(list_10times[-1], '%Y-%m-%d')
    delta_time = last_time - first_time
    average_days = int(delta_time.days / (len(list_10times) - 1))
    # 返回新的10次故障时间str，和平均故障间隔天数。
    return str_of_10times, average_days


'''
所有函数建立完成。
======================================================================================================
'''
'''
对所有维修记录中，需要分发到配件管理表的数据，进行整理。
把 是否已整理 中值为True的行全部删除。
把两种型号都无值的删除。
把没有日期的行中，日期填上该行创建日期。
'''
def manage_main(*args):
    for single_dict in record_list[::-1]:
        # 若 是否已整理 中值为True，或两种型号都无值，删除。
        if single_dict['是否已整理'] \
                or \
                (single_dict['普通配件型号'] is None and single_dict['重要、核心配件型号'] is None):
            processed_record_update_data.append({'row_id': single_dict['_id'], 'row': {'是否已整理': True}})
            record_list.remove(single_dict)
        # 若无日期，填上该行创建日期。
        elif not single_dict['故障日期']:
            single_dict['故障日期'] = single_dict['_ctime'][:10]
        else:
            pass

    for single_dict in pic_record_list[::-1]:
        # 若 是否已整理 中值为True，或两种型号都无值，删除。
        if single_dict['是否已整理'] \
                or \
                (single_dict['普通配件型号'] is None and single_dict['重要、核心配件型号'] is None):
            processed_pic_record_update_data.append({'row_id': single_dict['_id'], 'row': {'是否已整理': True}})
            pic_record_list.remove(single_dict)
        # 若无日期，填上该行创建日期。
        elif not single_dict['故障日期']:
            single_dict['故障日期'] = single_dict['_ctime'][:10]
        else:
            pass

    # 将两列表合并，成为待分流数据的列表。
    increased_record_list = record_list + pic_record_list

    '''
    将新增维修记录与普通配件表数据进行单循环对比。
    若:
        经清洗函数和对比函数后，认定型号一致。
        工段和所属设备一致。
    则:
        提取两条记录中，名称和型号有效值较长的值。
        补充'前10次维修日期'，并提取。
        计算'平均故障间隔(天)'，并提取。
        将以上提取数据和其他数据加入更新列表。
    '''
    # 单循环遍历新增维修记录与普通配件表数据。
    for record_row_common in increased_record_list[::-1]:
        for common_model_row in existing_common_model_list:
            # 如果两条记录中都存在型号,并且工段和设备一致。
            if record_row_common['普通配件型号'] is not None \
                    and \
                    common_model_row['配件型号'] is not None \
                    and \
                    record_row_common['所属工段'] == common_model_row['所属工段'] \
                    and \
                    record_row_common['所属设备'] == common_model_row['所属设备']:
                '''
                计算型号，并提取。
                '''
                # 用对比函数对比两型号，若一致，则提取有效字符较长的型号。
                contrast_result = str_contrast(record_row_common['普通配件型号'], common_model_row['配件型号'])

                # 判定型号一致,则进行后面的运算。
                if contrast_result:
                    '''
                    计算所取得名称，并提取。
                    '''
                    chosen_name_common = contrast_name(record_row_common, '普通配件名称', common_model_row, '配件名称')

                    '''
                    补充'前10次故障日期'的str，和平均故障间隔，并提取。
                    '''
                    update_10times_common, failure_rate_common = \
                        average_time(common_model_row['前10次故障日期'], record_row_common['故障日期'])

                    '''
                    添加更新普通配件表数据条目。
                    '''
                    common_update_data.append(
                        {
                            'row_id': common_model_row['_id'],
                            'row': {
                                '前10次故障日期': update_10times_common,
                                '平均故障间隔(天)': failure_rate_common,
                                '最近安装、维修日期': record_row_common['故障日期'],
                                '配件名称': chosen_name_common,
                                '配件型号': contrast_result
                            }
                        }
                    )

                    """
                    进行 普通配件 型号/名称合并记录的运算。
                    """
                    # 对两行中的配件名称进行避免key的value是None的检测，是None会return ''。
                    common_model_name = avoid_no_key(common_model_row, '配件名称')
                    record_name = avoid_no_key(record_row_common, '普通配件名称')
                    # 若对比的两行中配件型号或名称不同。
                    if record_row_common['普通配件型号'].strip() != common_model_row['配件型号'].strip() \
                            or \
                            common_model_name != record_name:
                        # 添加合并的两行的原始数据，作为合并记录条目。
                        merge_append_data.extend(
                            [
                                {
                                    '配件型号': common_model_row['配件型号'],
                                    '所属工段': common_model_row['所属工段'],
                                    '所属设备': common_model_row['所属设备'],
                                    '配件名称': common_model_row['配件名称'],
                                    '最近安装、维修日期': common_model_row['最近安装、维修日期']
                                },
                                {
                                    '配件型号': record_row_common['普通配件型号'],
                                    '所属工段': record_row_common['所属工段'],
                                    '所属设备': record_row_common['所属设备'],
                                    '配件名称': record_row_common['普通配件名称'],
                                    '最近安装、维修日期': record_row_common['故障日期']
                                }
                            ]
                        )

                    # 如果该维修记录行中没有核心型号，删除该行数据。
                    if not record_row_common['重要、核心配件型号']:
                        increased_record_list.remove(record_row_common)
                    # 否则，删除此record_row中的'普通配件型号'的key。
                    else:
                        record_row_common['普通配件型号'] = None

                    # 因已找到判定一致的型号，故终止此条新增记录的对比，进行下一行新增记录的对比。
                    break

    '''
    将剩余新增维修记录与重要配件表数据进行单循环对比。
    若:
        型号一致。
        工段和所属设备一致。
    则:
        补充'前10次维修日期'，并提取。
        计算'平均故障间隔(天)'，并提取。
        将以上提取数据和其他数据加入更新列表。
    '''
    for record_row_special in increased_record_list[::-1]:
        for special_model_row in existing_special_model_list:
            if record_row_special['重要、核心配件型号'] == special_model_row['配件型号'] \
                    and \
                    record_row_special['所属工段'] == special_model_row['所属工段'] \
                    and \
                    record_row_special['所属设备'] == special_model_row['所属设备']:
                '''
                补充'前10次故障日期'的str，和平均故障间隔，并提取。
                '''
                update_10times_special, failure_rate_special = \
                    average_time(special_model_row['前10次故障日期'], record_row_special['故障日期'])

                # 添加重要配件更新数据。
                special_update_data.append(
                    {
                        'row_id': special_model_row['_id'],
                        'row': {
                            '前10次故障日期': update_10times_special,
                            '平均故障间隔(天)': failure_rate_special,
                            '最近安装、维修日期': record_row_special['故障日期'],
                        }
                    }
                )

                # 如果该维修记录行中没有普通型号，删除该行数据。
                if not record_row_special['普通配件型号']:
                    increased_record_list.remove(record_row_special)
                # 否则，删除此record_row中的'重要、核心配件型号'的key。
                else:
                    record_row_special['重要、核心配件型号'] = None

                # 因已找到判定一致的型号，故终止此条新增记录的对比，进行下一行新增记录的对比。
                break

    """
    将新增维修记录数据中剩余部分，分别加入普通和重要配件追加数据集中。
    """
    for record_row_remain in increased_record_list:
        if record_row_remain['普通配件型号'] is not None \
                and \
                re.sub(r'\W|_', '', record_row_remain['普通配件型号']) != '':
            common_append_data.append(
                {
                    '前10次故障日期': record_row_remain['故障日期'] + '/',
                    '所属工段': record_row_remain['所属工段'],
                    '所属设备': record_row_remain['所属设备'],
                    '最近安装、维修日期': record_row_remain['故障日期'],
                    '配件名称': avoid_no_key(record_row_remain, '普通配件名称'),
                    '配件型号': record_row_remain['普通配件型号']
                }
            )

        if record_row_remain['重要、核心配件型号']:
            special_append_data.append(
                {
                    '前10次故障日期': record_row_remain['故障日期'] + '/',
                    '所属工段': record_row_remain['所属工段'],
                    '所属设备': record_row_remain['所属设备'],
                    '最近安装、维修日期': record_row_remain['故障日期'],
                    '配件型号': record_row_remain['重要、核心配件型号']
                }
            )

    """
    更新维修记录表的后台数据
    """
    # 获取修改后的维修记录总量。
    new_common_record_num = len(record_base.list_rows('维修记录'))
    new_pic_record_num = len(record_base.list_rows('维修记录（图片版）'))
    # 获取本次新增维修记录条数。
    new_increased_common_record_num = new_common_record_num - existing_common_record_num
    new_increased_pic_record_num = new_pic_record_num - existing_pic_record_num
    # 本次将追加的后台数据。
    background_append_data = {
        '日期': datetime.now().strftime('%Y-%m-%d/'),
        '总记录量': new_common_record_num,
        '较上次新增': new_increased_common_record_num,
        '图片版总记录量': new_pic_record_num,
        '图片版较上次新增': new_increased_pic_record_num
    }

    # 添加更新 维修记录 和 图片版 中'是否已整理'为True的数据。
    for processed_record_row in record_list:
        processed_record_update_data.append(
            {
                'row_id': processed_record_row['_id'],
                'row': {
                    '故障日期': processed_record_row['故障日期'],
                    '是否已整理': True
                }
            }
        )
    for processed_pic_record_row in pic_record_list:
        processed_pic_record_update_data.append(
            {
                'row_id': processed_pic_record_row['_id'],
                'row': {
                    '故障日期': processed_pic_record_row['故障日期'],
                    '是否已整理': True
                }
            }
        )
    """
    批量修改实表。
    """
    # 批量更新普通配件实表。
    model_base.batch_update_rows('普通配件', rows_data=common_update_data)
    # 批量追加合并记录实表。
    model_base.batch_append_rows('普通配件型号/名称合并记录', merge_append_data)
    # 批量更新重要配件实表。
    model_base.batch_update_rows('重要、核心配件', rows_data=special_update_data)
    # 批量追加普通和重要配件实表。
    model_base.batch_append_rows('普通配件', common_append_data)
    model_base.batch_append_rows('重要、核心配件', special_append_data)
    # 批量更新 维修记录 和 图片版 中'是否已整理'为True。
    record_base.batch_update_rows('维修记录', processed_record_update_data)
    record_base.batch_update_rows('维修记录（图片版）', processed_pic_record_update_data)
    # 如果'较上次新增'大于0，则追加后台数据。
    if new_increased_common_record_num > 0 or new_increased_pic_record_num > 0:
        record_base.append_row('后台数据', background_append_data)

manage_main()