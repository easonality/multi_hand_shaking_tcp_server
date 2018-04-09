import time
import socket
import threading
import wx
import os
import sys
import tcp_server as ts

class Frame(wx.Frame):

    #-------------------------------------------------------------
    def __init__(self, parent, title):
        '''
        initalize
        '''
        super(frame, self).__init__(parent, title=title, size=(350, 250))
        self.ip = 'localhost'
        self.port_min = 0
        self.port_max = 0
        
        self.set_panel()
        self.Fit()
        self.Show()
    
    #-------------------------------------------------------------
    def set_panel(self):
        # Set panel
        panel = wx.Panel(self)

        # Set labels
        self.label_ip = wx.StaticText(panel, -1, '   ip:   ')
        self.label_port = wx.StaticText(panel, -1, 'ports:')

        # Set buttons
        self.button_ip_change = wx.Button(panel, -1, label='change')
        self.button_ip_change.Enable(True)

        self.button_port_change = wx.Button(panel, -1, label='change')
        self.button_port_change.Enable(True)

        self.button_run = wx.Button(panel, -1, label='run')
        self.button_run.Enable(True)

        self.button_get_ip = wx.Button(panel, -1, label='get ip')
        self.button_get_ip.Enable(True)
        
        self.button_stop = wx.Button(panel, -1, label='stop')
        self.button_stop.Enable(False)
        
        # Set texts
        self.text_ip = wx.TextCtrl(panel, -1, size=(100,25), style=wx.ALIGN_LEFT)
        self.text_ip.SetValue(self.ip)
        self.text_ip.Enable(False)

        self.text_port_min = wx.TextCtrl(panel, -1, size=(45,25), style=wx.ALIGN_LEFT)
        self.text_port_min.SetValue('2000')
        self.text_port_min.Enable(False)

        self.text_port_max = wx.TextCtrl(panel, -1, size=(45,25), style=wx.ALIGN_LEFT)
        self.text_port_max.SetValue('2010')
        self.text_port_max.Enable(False)

        self.adj = wx.StaticText(panel, -1, size = (25,25), style=wx.ALIGN_LEFT, label='')

        # Set sizers
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.label_ip, 0, wx.ALL|wx.LEFT, 5)
        sizer1.Add(self.text_ip, 0, wx.ALL|wx.LEFT, 5)
        sizer1.Add(self.button_ip_change, 5, wx.ALL|wx.RIGHT, 5)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.label_port, 0, wx.ALL|wx.LEFT, 5)
        sizer2.Add(self.text_port_min, 0, wx.ALL|wx.LEFT, 5)
        sizer2.Add(self.text_port_max, 0, wx.ALL|wx.LEFT, 5)
        sizer2.Add(self.button_port_change, 0, wx.ALL|wx.LEFT, 5)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(self.button_run, 0, wx.LEFT, 3)
        sizer3.Add(self.button_get_ip, 0, wx.LEFT, 3)
        sizer3.Add(self.button_stop, 0, wx.LEFT, 3)

        # Set sizers to the panel content
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer1, 0, wx.ALL, 15)
        sizer.Add(sizer2, 0, wx.ALL, 15)
        sizer.Add(sizer3, 0, wx.TOP|wx.RIGHT|wx.LEFT, 15)
        sizer.Add(self.adj, 0, wx.BOTTOM, 10)

        panel.SetSizer(sizer)

        # Set event handlers
        self.button_ip_change.Bind(wx.EVT_BUTTON, self.on_ip_change)
        self.button_port_change.Bind(wx.EVT_BUTTON, self.on_port_change)
        self.button_run.Bind(wx.EVT_BUTTON, self.on_run)
        self.button_get_ip.Bind(wx.EVT_BUTTON, self.on_get_ip)
        self.button_stop.Bind(wx.EVT_BUTTON, self.on_stop)
        self.Bind(wx.EVT_CLOSE, self.on_frame_close)

        # fit
        panel.Fit()

    #-------------------------------------------------------------
    def on_frame_close(self, e):
        os._exit(0)

    #-------------------------------------------------------------
    def on_ip_change(self, e):
        self.text_ip.Enable(True)

    #-------------------------------------------------------------
    def on_port_change(self, e):
        self.text_port_min.Enable(True)
        self.text_port_max.Enable(True)

    #-------------------------------------------------------------
    def on_run(self, e):
        self.text_ip.Enable(False)
        self.text_port_min.Enable(False)
        self.text_port_max.Enable(False)
        self.button_ip_change.Enable(False)
        self.button_port_change.Enable(False)
        self.button_run.Enable(False)
        self.button_get_ip.Enable(False)
        self.button_stop.Enable(True)

        ip = self.text_ip.GetValue()
        low = int(self.text_port_min.GetValue())
        high = int(self.text_port_max.GetValue())

        for i in range(low, high+1):
            addr = (ip, i)
            th = threading.Thread(target=self.func, args=(addr,))
            th.daemon = True
            th.start()

    #-------------------------------------------------------------
    def on_stop(self, e):
        self.text_ip.Enable(False)
        self.text_port_min.Enable(False)
        self.text_port_max.Enable(False)
        self.button_ip_change.Enable(True)
        self.button_port_change.Enable(True)
        self.button_run.Enable(True)
        self.button_get_ip.Enable(True)
        self.button_stop.Enable(False)

    #-------------------------------------------------------------
    def on_get_ip(self, e):
        self.text_ip.SetValue(socket.gethostbyname(socket.gethostname()))

    #-------------------------------------------------------------
    def func(self, addr):
        return ts.Tcp_server().run(addr)


if __name__ == '__main__':
    app = wx.App()
    Frame(None, title='multi-tcp-server v1.0.0')
    app.MainLoop()




