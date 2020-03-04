#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A MLHub GUI for Objects

author: Graham Williams
website: mlhub.ai
"""

import os
import wx
import subprocess
import re

MODEL = "Objects"
CMD_IDENTIFY = ["ml", "identify", "objects"]

DEFAULT_PATH = "Enter a local path to an image (jpg, png) file"
DEFAULT_IMAGE = os.path.join(os.getcwd(), "cache/images/sample.jpg")
DEFAULT_ID = "Results will appear here ..."

NO_RESULTS = "No results returned from the model."

WILDCARD = "Images (*.jpg,*.png)|*.jpg;*.png|" \
           "All files (*.*)|*.*"

class MLHub(wx.Frame):

    def __init__(self, parent, title):
        super(MLHub, self).__init__(parent,
                                    title=title,
                                    size=(750, 500))

        self.InitUI()
        self.Centre()

    def InitUI(self):
        # self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.images_dir = os.path.join(os.getcwd(), "cache/images")
        self.last_browse_dir = ""
        
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc_path = wx.TextCtrl(panel, value=DEFAULT_PATH)
        hbox1.Add(self.tc_path, proportion=1)
        bt_browse = wx.Button(panel, label="Browse")
        bt_browse.Bind(wx.EVT_BUTTON, self.OnBrowse)
        hbox1.Add(bt_browse, flag=wx.LEFT, border=10)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        sample = wx.Bitmap(DEFAULT_IMAGE, wx.BITMAP_TYPE_ANY)
        sample = self.ScaleBitmap(sample, 500, 300)
        self.sb_sample = wx.StaticBitmap(panel, wx.ID_ANY, sample)
        self.hbox2.Add(self.sb_sample, flag=wx.EXPAND)
        self.hbox2.Add((10, -1))
        self.st_results = wx.StaticText(panel, label=DEFAULT_ID)
        self.hbox2.Add(self.st_results, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(self.hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
	# IDENTIFY
        bt_identify = wx.Button(panel, label="Identify")
        bt_identify.Bind(wx.EVT_BUTTON, self.OnIdentify)
        hbox3.Add(bt_identify, flag=wx.RIGHT, border=10)
	# Add to the panel.
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
        if self.last_browse_dir == "":
            default_dir = self.images_dir
        else:
            default_dir = self.last_browse_dir
        dlg = wx.FileDialog(self,
                            message="Choose a file",
                            defaultDir=default_dir, 
                            defaultFile="",
                            wildcard=WILDCARD,
                            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if len(paths):
                self.last_browse_dir = os.path.dirname(paths[0])
                # Display path in text control.
                self.tc_path.SetValue(paths[0])
                # Update the image display.
                sample = wx.Bitmap(paths[0], wx.BITMAP_TYPE_ANY)
                sample = self.ScaleBitmap(sample, 500, 300)
                self.sb_sample.SetBitmap(sample)
                # Update the Identification text.
                self.st_results.SetLabel(DEFAULT_ID)
                # Recenter the image
                self.hbox2.Layout()

    def OnIdentify(self, event):
        wait = wx.BusyCursor()
        path = self.tc_path.GetValue()
        if path == DEFAULT_PATH:
            path = DEFAULT_IMAGE
        cmd = CMD_IDENTIFY.copy()
        cmd.append(path)
	# Show the command line.
        print("$ " + " ".join(cmd))
        results = subprocess.check_output(cmd)
        if len(results) == 0:
            self.st_results.SetLabel(NO_RESULTS)
        else:
            r = re.sub(r'^(.*?),', r'[\1] ',
                       re.sub(r'\n(.*?),', r'\n\n[\1] ',
                              results.decode("utf-8")))
            self.st_results.SetLabel(r)
        self.hbox2.Layout()
	# Show the command line results.
        print(results.decode("utf-8"))
        del(wait)

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
