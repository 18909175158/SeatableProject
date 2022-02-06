import time
from WeChatPYAPI import WeChatPYApi
from queue import Queue

"""
必须先手动登陆微信
"""
# 建立消息队列
msg_queue = Queue()
# 工段列表
department_list = [
    '备料', '下料', '自动线', '锻压机', '热处理', '模锻', '轻跨', '精锻', '三期', '设备组', '技术组'
]
# 欢迎消息
welcome_str = '欢迎进入维修数据管理系统！\
\n点击下方链接进入功能页面，\
\n回复”1“或者”帮助“获取更多帮助，\
\n回复”2“或者”功能“重新获取功能页链接。'
# 工段功能页对应网址
link_dict = {
    '三期': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=117',
    '下料': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=112',
    '备料': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=112',
    '技术组': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=118',
    '模锻': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=115',
    '热处理': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=114',
    '精锻': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=117',
    '自动线': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=109',
    '设备组': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=118',
    '轻垮': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=116',
    '轻跨': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=116',
    '锻压机': 'https://xx26640615.m.jzfkw.cn/col.jsp?id=113'
}

# 工段分享图对应网址
img_url_dict = {
    '三期': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_7%20(1).jpg',
    '下料': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_1%20(1).jpg',
    '备料': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_1.jpg',
    '模锻': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_5.jpg',
    '热处理': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_4.jpg',
    '精锻': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_7.jpg',
    '自动线': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_2.jpg',
    '设备组': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_8.jpg',
    '轻垮': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_6%20(1).jpg',
    '轻跨': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_6.jpg',
    '锻压机': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_3.jpg',
    '技术组': 'https://cloud.seatable.cn/workspace/189828/asset/62493b7c-d93f-4d9b-afb0-f4045b5d4af1/images/2022-02/link_style_8%20(1).jpg',
}


# 消息回调，建议异步处理，防止阻塞


def on_message(msg):
    msg_queue.put(msg)


def main():
    # 创建实例
    w = WeChatPYApi(msg_callback=on_message)
    # help(WeChatPYApi)

    # 如果微信登陆状态为True
    if w.get_login_state():
        # 这里需要阻塞，等待获取个人信息
        while not w.get_self_info():
            time.sleep(5)

    my_info = w.get_self_info()
    self_wx = my_info["wx_id"]
    print("登陆成功！")
    print(my_info)

    while True:
        # 从消息队列中取出一条信息
        msg = msg_queue.get()
        # 如果消息内容在工段列表中
        if msg["msg_type"] == 37 and msg['content'].strip() in department_list:
            # 同意加好友申请
            w.agree_friend(self_wx=self_wx, msg_data=msg)
            # 查询该id是否在好友列表中，没有则等待1秒（保证加好友成功）
            while not w.query_friend_info(self_wx, msg['wx_id']):
                time.sleep(1)
            msg_sender_info = w.query_friend_info(self_wx, msg['wx_id'])
            w.alter_friend_remark(
                self_wx,
                msg['wx_id'],
                msg_sender_info['nick_name'] + msg['content'].strip()
            )
            w.send_text(self_wx, msg['wx_id'], welcome_str)
            w.send_card_link(
                self_wx,
                msg['wx_id'],
                msg['content'].strip() + '功能页',
                '维修数据管理系统',
                link_dict[msg['content'].strip()],
                img_url_dict[msg['content'].strip()]
            )
