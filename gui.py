#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A GUI for MLHub from the Objects model

author: Graham Williams
website: mlhub.ai
"""

import os
import wx
import subprocess

MODEL = "Objects"

DEFAULT_PATH = "Type a local path or a URL to an image (jpg, png, gif) file"

WILDCARD = "Images (*.jpg)|*.jpg|" \
           "All files (*.*)|*.*"

class MLHub(wx.Frame):

    def __init__(self, parent, title):
        super(MLHub, self).__init__(parent,
                                    title=title,
                                    size=(650, 400))

        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.images_dir = os.path.join(os.getcwd(), "cache/images")
        
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc_path = wx.TextCtrl(panel, value=DEFAULT_PATH)
        hbox1.Add(self.tc_path, proportion=1)
        bt_browse = wx.Button(panel, label="Browse")
        bt_browse.Bind(wx.EVT_BUTTON, self.OnBrowse)
        hbox1.Add(bt_browse, flag=wx.LEFT, border=10)
        bt_display = wx.Button(panel, label='Display')
        hbox1.Add(bt_display, flag=wx.LEFT, border=10)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        sample = wx.Bitmap("cache/images/sample.jpg", wx.BITMAP_TYPE_ANY)
        self.sb_sample = wx.StaticBitmap(panel, wx.ID_ANY, sample)
        self.hbox2.Add(self.sb_sample, proportion=1, flag=wx.EXPAND)
        vbox.Add(self.hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        bt_identify = wx.Button(panel, label="Identify")
        bt_identify.Bind(wx.EVT_BUTTON, self.OnIdentify)
        hbox3.Add(bt_identify, flag=wx.RIGHT, border=10)
        self.st_identity = wx.StaticText(panel, label="Identified as a ...")
        hbox3.Add(self.st_identity, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        panel.SetSizer(vbox)

    def ScaleBitmap(self, bitmap, width, height):
        image = bitmap.ConvertToImage()
        # Retain the aspect ratio
        w = image.GetWidth()
        h = image.GetHeight()
        oar = w/h # Original aspect ratio
        par = width/height # Proposed aspect ratio
        if oar > par:
            height = width / oar
        else:
            width = height * oar
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return(result)

    def OnBrowse(self, event):
        dlg = wx.FileDialog(self,
                            message="Choose a file",
                            defaultDir=self.images_dir, 
                            defaultFile="",
                            wildcard=WILDCARD,
                            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if len(paths):
                self.tc_path.SetValue(paths[0])
                sample = wx.Bitmap(paths[0], wx.BITMAP_TYPE_ANY)
                sample = self.ScaleBitmap(sample, 450, 250)
                self.sb_sample.SetBitmap(sample)
                # Recenter the image
                self.hbox2.Layout()

    def OnIdentify(self, event):
        wait = wx.BusyCursor()
        path = self.tc_path.GetValue()
        if path == DEFAULT_PATH:
            path = "cache/images/sample.jpg"
        results = subprocess.check_output(["ml", "identify", "objects", path])
        del(wait)
        r = results.decode("utf-8").split()[0].split(",")
        self.st_identity.SetLabel(f"Identified as a {r[1]} with a certainty of {r[0]}.")

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
                               "Do you really want to close MLHub " + MODEL +"?",
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
