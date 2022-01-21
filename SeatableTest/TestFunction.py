# from seatable_api import Account
# import pprint
#
# email = '18909175158@163.com'
# password = 'sincere1027'
# server_url = 'https://cloud.seatable.cn/'
# account = Account(email, password, server_url)
# account.auth()
#
# # pprint.pprint(account.list_workspaces())
# m_base = account.get_base(189828, '配件管理总表')
#
# # a_data={'配件名称':''}
# # m_base.append_row('普通配件',a_data)
# #
# # c_data = m_base.list_rows('普通配件')
# # pprint.pprint(c_data)
# # u_data = {'所属工段': 'uuu'}
# # m_base.update_row('普通配件', 'I7NhzejSQxW0NEX7UC0QzQ', u_data)
# c_data = m_base.list_rows('普通配件')
# pprint.pprint(c_data)
import re

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

a='FZ1600R17KF6——b2'
b='FZ1600R17KF6_B2'
c='FZ1600R17KF6'
print(str_contrast(b,c))