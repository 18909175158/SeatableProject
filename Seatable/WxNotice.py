from wxauto import WeChat

wx = WeChat()
l= wx.GetSessionList()
# wx.ChatWith('文件传输助手')
w=wx.Search('文件传输助手')
wx.SendMsg('你好')