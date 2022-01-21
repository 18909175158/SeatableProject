import Levenshtein
import re


def cut_str(to_be_cut_str):
    """
    去除字符串中的符号和空格
    :param:str
    :return: 清理后的str
    """
    b_cut_str = re.sub(r'_+|\W+', '', to_be_cut_str)
    return b_cut_str


def str_contrast(model1, model2):
    """
    将两个字符串进行对比
    以判定是否为同一型号
    :param:str*2
    :return: str or False
    """
    # 设置判定型号一致的标识符
    consistent = False

    '''
    前后缺字符/字符节中间有空格的判定方式。暂时不用。
    '''
    # 清除两字符串中的符号，并转为小写
    #    cleaned_model1 = cut_str(model1)
    #    cleaned_model2 = cut_str(model2)
    #    # 比对相似度，若有效字符排序一样，并长度比大于7/10,则判定型号一致
    #    if (cleaned_model1 in cleaned_model2 and len(cleaned_model1) >= int(len(cleaned_model2) * 0.7)) \
    #    or \
    #    (cleaned_model2 in cleaned_model1 and len(cleaned_model1) > len(cleaned_model2) >= int(
    #            len(cleaned_model1) * 0.7)):
    #            	consistent=True

    # 使两字符串只保留汉字
    model1_cn_only = re.sub(r'(\W|_|[0-9]|[a-z])+', '', model1)
    model2_cn_only = re.sub(r'(\W|_|[0-9]|[a-z])+', '', model2)
    # 如果两者都包含汉字，且汉字占比大于等于2/3
    if len(model1_cn_only) >= len(cut_str(model1)) * 0.66 and len(model2_cn_only) >= len(cut_str(model2)) * 0.66:
        # 取得方位字符列表
        direction_single_char = re.compile('轴承|进|出|上|下|左|右|前|后|东|南|西|北|内|外|大|小|长|短|a|b|c|d|A|B|C|D|[0-9]')
        direction_single_list1 = direction_single_char.findall(model1)
        direction_single_list2 = direction_single_char.findall(model2)
        # 列表完全相同,则进行Levenshtein对比
        if direction_single_list1 == direction_single_list2:
            # 原字符串去除所有符号、空格
            char_2b_clean = r'\W+|_+'
            b_cleaned1 = re.sub(char_2b_clean, '', model1)
            b_cleaned2 = re.sub(char_2b_clean, '', model2)
            # 剩下的字符串进行Levenshtein对比
            cleaned_lev = Levenshtein.ratio(b_cleaned1, b_cleaned2)
            # 如果相似度大于0.83（5汉字差一个以内），则判定为同型号
            if cleaned_lev > 0.83:
                consistent = True
    # 中文占比小于2/3的话，则采用字符节列表对比
    else:
        en_regex = re.compile(r'\bv\d+\.\d+\b|\b\d+.\d+\b|[0-9a-z]+')
        # 获得两字符串中被符号隔开的字符串切片列表
        model1_piece_list = en_regex.findall(model1.lower())
        model2_piece_list = en_regex.findall(model2.lower())
        # 设置计数符
        same_counter = 0
        # 如果两列表相同，直接判定型号一致
        if model1_piece_list == model2_piece_list:
            consistent = True
        # 判断哪个列表元素多，作为去除其中元素的对象
        if len(model1_piece_list) < len(model2_piece_list):
            model1_piece_list, model2_piece_list = model2_piece_list, model1_piece_list

        # 设置一个专门用来修改并做对比的列表，以避免修改原长列表
        contrast_list = model1_piece_list.copy()
        # 去除列表中的一项，如与原短列表相同，则计数+1
        for piece in model1_piece_list:
            contrast_list.remove(piece)
            if contrast_list == model2_piece_list:
                same_counter += 1
            # 还原对比列表，重复以上过程
            contrast_list = model1_piece_list.copy()
        # 任一次对比结果相同，则判定两型号一致
        if same_counter > 0:
            consistent = True

    #如果判定型号一致，return有效字符长的值，否则return False。
    if consistent and len(cut_str(model1)) >= len(cut_str(model2)):
        return model1.strip()
    elif consistent and len(cut_str(model1)) < len(cut_str(model2)):
        return model2.strip()
    else:
        return False


str1 = 'aaaa bbbb11-cc22cc/dd5-6666 v3.0'
str2 = 'aaaa bbbb11-cc22cc/dd5-6666'
str3 = 'bbbb11-cc22cc/dd5-6666 v3.0'
str4 = 'aaaa   BBBB11,cc22CC,dd5.6666   '

cn1 = '制动器齿盘'
cn2 = '制动器齿圈'
cn3 = '下顶料流量阀'
cn4 = '下顶料阀'
cn5 = '下顶料安全阀'
cn6 = '上顶料流量阀'
cn7 = '连皮传送带轴'
cn8 = '连皮传送带轴承'

print(str_contrast(str4, str3))
print(str_contrast(cn3, cn4))
