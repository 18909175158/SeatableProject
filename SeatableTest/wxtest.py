import time
from WeChatPYAPI import WeChatPYApi
from queue import Queue

"""
必须先手动登陆微信
"""
# 建立消息队列
msg_queue = Queue()
# 工段列表
department_list = ['备料', '自动线', '锻压机', '热处理', '模锻', '轻跨', '精锻']


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
        msg = msg_queue.get()
        if msg["msg_type"] == 37 and msg['content'].strip() in department_list:
            w.agree_friend(self_wx=self_wx, msg_data=msg)
            while not w.query_friend_info(self_wx,msg['wx_id']):
                time.sleep(1)
            w.alter_friend_remark(self_wx,msg['wx_id'],msg['content'].strip())
