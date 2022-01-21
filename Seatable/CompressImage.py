import os

from seatable_api import Base, context
from PIL import Image

# 获取base的授权。
server_url = context.server_url or 'https://cloud.seatable.cn'
api_token = context.api_token or 'a5525acad5ee5f21a3dd2dc39cc05bf1dee3a9eb'

base = Base(api_token, server_url)
base.auth()

# 图片的临时存放路径,如果不存在，则创建。
uncompress_img_dir = r'C:\compress_img\uncompress'
compressed_img_dir = r'C:\compress_img\compressed'
if not os.path.exists(uncompress_img_dir):
    os.makedirs(uncompress_img_dir)
if not os.path.exists(compressed_img_dir):
    os.makedirs(compressed_img_dir)

# 建立批量更新行数据的容器。
update_data = []
# 获取图片表的数据list。
rows_list = base.list_rows('维修记录（图片版）')

# 表中图片列key的list。
key_list = []
# 获取所有列。
col_list = base.list_columns('维修记录（图片版）')
# 如果该列中的type属性为image，则把它的name加入key_list。
for col in col_list:
    if col['type'] == 'image':
        key_list.append(col['name'])

# 遍历获取图片的url。
for row in rows_list:
    # 设置一个该行更新数据的字典。
    update_row_dict = {
        'row_id': row['_id'],
        'row': {}
    }
    if (not ('图片是否已压缩' in row)) or row['图片是否已压缩'] == False:
        for key in key_list:
            if key in row:
                # 建立空list，保存单元格内图片压缩后存储的url。
                compressed_img_url_list = []
                for img_url in row[key]:

                    # 获取文件名。
                    uncompress_filename = img_url.split('/')[-1]
                    # 设置下载的保存路径。
                    save_path = uncompress_img_dir + '\\' + uncompress_filename
                    target_path = compressed_img_dir + '\\' + uncompress_filename
                    # 下载文件。
                    base.download_file(img_url, save_path)
                    # 获取图片文件大小(kb)。
                    file_size = os.path.getsize(save_path) / 1024
                    # 如果文件小于1m，直接删除，并把原url加入更新数据的list。
                    if file_size < 1000:
                        os.remove(save_path)
                        compressed_img_url_list.append(img_url)
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
                        compressed_img_url_list.append(info_dict['url'])
                # 更新该行更新数据的字典。
                update_row_dict['row'][key] = compressed_img_url_list
            update_row_dict['row']['图片是否已压缩'] = True
        # 更新批量更新的数据。
        update_data.append(update_row_dict)

# 批量更新行。
base.batch_update_rows('维修记录（图片版）', update_data)
