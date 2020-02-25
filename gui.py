#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A GUI for MLHub from the Objects model

author: Graham Williams
website: mlhub.ai
"""

import wx
import subprocess

MODEL = "Objects"

class MLHub(wx.Frame):

    def __init__(self, parent, title):
        super(MLHub, self).__init__(parent,
                                    title=title,
                                    size=(650, 400))

        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        tc1 = wx.TextCtrl(panel, value="Type a local path or a URL to an image (jpg, png, gif) file")
        hbox1.Add(tc1, proportion=1)
        bt_browse = wx.Button(panel, label="Browse")
        hbox1.Add(bt_browse, flag=wx.LEFT, border=10)
        bt_display = wx.Button(panel, label='Display')
        hbox1.Add(bt_display, flag=wx.LEFT, border=10)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        sample = wx.Bitmap("cache/images/sample.jpg", wx.BITMAP_TYPE_ANY)
        sb_sample = wx.StaticBitmap(panel, wx.ID_ANY, sample)
        hbox2.Add(sb_sample, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        bt_identify = wx.Button(panel, label="Identify")
        bt_identify.Bind(wx.EVT_BUTTON, self.OnIdentify)
        hbox3.Add(bt_identify, flag=wx.RIGHT, border=10)
        st_identity = wx.StaticText(panel, label="Identified as a ...")
        hbox3.Add(st_identity, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        panel.SetSizer(vbox)

    def OnIdentify(self, event):
        subprocess.run(["ml", "identify", "objects", "cache/images/sample.jpg"])


    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
        
def main():
    app = wx.App()
    mlhub = MLHub(None, title='MLHub: ' + MODEL)
    mlhub.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
