import os
from pprint import pprint

from seatable_api import Account
from PIL import Image

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
record_base = account.get_base(189828, '维修记录表')
declare_base = account.get_base(189828, '短缺备件申报表')
# 获取表的所有行数据
record_row_list = record_base.list_rows('维修记录（图片版）')
elc_declare_row_list = declare_base.list_rows('短缺备件申报表（电器）')
mec_declare_row_list = declare_base.list_rows('短缺备件申报表（机械）')
# 建立各表更新数据的容器。
record_update_data = []
elc_declare_update_data = []
mec_declare_update_data = []

# 图片的临时存放路径,如果不存在，则创建。
uncompress_img_dir = r'C:\compress_img\uncompress'
compressed_img_dir = r'C:\compress_img\compressed'
if not os.path.exists(uncompress_img_dir):
    os.makedirs(uncompress_img_dir)
if not os.path.exists(compressed_img_dir):
    os.makedirs(compressed_img_dir)


def compress_img(img_url, base):
    '''
    压缩图片的函数。
    :param img_url: 原图片的url
    :param base: 图片所属的base
    :return: 处理后需要更新到总更新数据的url
    '''
    # 获取文件名。
    uncompress_filename = img_url.split('/')[-1]
    # 设置下载的保存路径。
    save_path = uncompress_img_dir + '\\' + uncompress_filename
    target_path = compressed_img_dir + '\\' + uncompress_filename
    # 下载文件。
    base.download_file(img_url, save_path)
    # 获取图片文件大小(kb)。
    file_size = os.path.getsize(save_path) / 1024
    # 如果文件小于1m，直接删除。
    if file_size < 1000:
        os.remove(save_path)
        # 返回原img_url。
        return img_url
    # 否则，压缩。
    else:
        # 将图片读入内存。
        o_img = Image.open(save_path)
        # 压缩比率算法，大概4m:30,2m:50,1m:80。
        compress_rate = (1 / file_size) ** 0.69 / 0.000106
        # 压缩，存到压缩后文件夹。
        o_img.save(target_path, quality=int(compress_rate))
        # 上传压缩后的图片，replace网上的原图。
        info_dict = base.upload_local_file(target_path, file_type='image', replace=True)
        # 删除本地的压缩前/后的图片。
        os.remove(save_path)
        os.remove(target_path)
        # 返回压缩后上传的img_url。
        return info_dict['url']


'''
压缩 维修记录（图片版）中的图片。
'''
# 表中图片列key的list。
record_key_list = []
# 获取所有列。
record_col_list = record_base.list_columns('维修记录（图片版）')
# 如果该列中的type属性为image，则把它的name加入key_list。
for record_col in record_col_list:
    if record_col['type'] == 'image':
        record_key_list.append(record_col['name'])

# 遍历获取图片的url。
for record_row in record_row_list:
    # 设置一个该行更新数据的字典。
    update_record_row_dict = {
        'row_id': record_row['_id'],
        'row': {}
    }
    # 如果‘图片已压缩’项目不存在或为False。
    if (not ('图片是否已压缩' in record_row)) or record_row['图片是否已压缩'] == False:
        # 遍历此行的图片列的key。
        for key in record_key_list:
            # 如果该行中此列有内容
            if key in record_row:
                # 建立空list，保存单元格内图片压缩后存储的url。
                compressed_record_img_url_list = []
                # 遍历该行该列（该单元格）中图片url的列表。
                for record_img_url in record_row[key]:
                    # 处理该图片，并把返回的url加入压缩后url列表
                    compressed_record_img_url_list.append(
                        compress_img(record_img_url, record_base)
                    )
                # 更新该行更新数据的字典。
                update_record_row_dict['row'][key] = compressed_record_img_url_list
        update_record_row_dict['row']['图片是否已压缩'] = True
        # 更新批量更新的数据。
    record_update_data.append(update_record_row_dict)

'''
压缩 短缺备件申报表（电器）中的图片
'''
# 遍历行。
for elc_declare_row in elc_declare_row_list:
    # 设置一个该行更新数据的字典。
    update_elc_row_dict = {
        'row_id': elc_declare_row['_id'],
        'row': {}
    }
    # 如果‘图片已压缩’项目不存在或为False，并且该行中此列有内容。
    if ((not ('图片是否已压缩' in elc_declare_row)) \
        or \
        elc_declare_row['图片是否已压缩'] == False) \
            and \
            '备件照片' in elc_declare_row:
        # 建立空list，保存单元格内图片压缩后存储的url。
        compressed_elc_img_url_list = []
        # 遍历该行该列（该单元格）中图片url的列表。
        for elc_img_url in elc_declare_row['备件照片']:
            # 处理该图片，并把返回的url加入压缩后url列表
            compressed_elc_img_url_list.append(
                compress_img(elc_img_url, declare_base)
            )
        # 更新该行更新数据的字典。
        update_elc_row_dict['row']['备件照片'] = compressed_elc_img_url_list
    update_elc_row_dict['row']['图片是否已压缩'] = True
    # 更新批量更新的数据。
    elc_declare_update_data.append(update_elc_row_dict)

'''
压缩 短缺备件申报表（机械）中的图片
'''
# 遍历行。
for mec_declare_row in mec_declare_row_list:
    # 设置一个该行更新数据的字典。
    update_mec_row_dict = {
        'row_id': mec_declare_row['_id'],
        'row': {}
    }
    # 如果‘图片已压缩’项目不存在或为False，并且该行中此列有内容。
    if ((not ('图片是否已压缩' in mec_declare_row)) \
        or \
        mec_declare_row['图片是否已压缩'] == False) \
            and \
            '备件照片' in mec_declare_row:
        # 建立空list，保存单元格内图片压缩后存储的url。
        compressed_mec_img_url_list = []
        # 遍历该行该列（该单元格）中图片url的列表。
        for mec_img_url in mec_declare_row['备件照片']:
            # 处理该图片，并把返回的url加入压缩后url列表
            compressed_mec_img_url_list.append(
                compress_img(mec_img_url, declare_base)
            )
        # 更新该行更新数据的字典。
        update_mec_row_dict['row']['备件照片'] = compressed_mec_img_url_list
    update_mec_row_dict['row']['图片是否已压缩'] = True
    # 更新批量更新的数据。
    mec_declare_update_data.append(update_mec_row_dict)

# 批量更新行。
record_base.batch_update_rows('维修记录（图片版）',record_update_data)
declare_base.batch_update_rows('短缺备件申报表（电器）',elc_declare_update_data)
declare_base.batch_update_rows('短缺备件申报表（机械）',mec_declare_update_data)
