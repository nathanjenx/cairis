#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import wx
import armid
import WidgetFactory
from Borg import Borg

class CodeRelationshipDialog(wx.Dialog):
  def __init__(self,parent,fromName = '',toName = '',rType = ''):
    wx.Dialog.__init__(self,parent,armid.CODERELATIONSHIP_ID,'Add Code Relationship',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,200))

    self.theFromName = ''
    self.theToName = ''
    self.theRelationship = ''
    self.commitLabel = 'Add'
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    self.rtLookup = {'==':'associated','=>':'implies','<>':'conflict','[]':'part-of'}

    b = Borg()
    codeList = b.dbProxy.getDimensionNames('code')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'From',(87,30),armid.CODERELATIONSHIP_COMBOFROMCODE_ID,codeList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'To',(87,30),armid.CODERELATIONSHIP_COMBOTOCODE_ID,codeList),0,wx.EXPAND)
    rtList = ['==','=>','<>','[]']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'To',(87,30),armid.CODERELATIONSHIP_COMBORTTYPE_ID,rtList),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.CODERELATIONSHIP_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.CODERELATIONSHIP_BUTTONADD_ID,self.onCommit)

  def load(self,fromName,toValue,rType):
    fromCtrl = self.FindWindowById(armid.CODERELATIONSHIP_COMBOFROMCODE_ID)
    toCtrl = self.FindWindowById(armid.CODERELATIONSHIP_COMBOTOCODE_ID)
    rtCtrl = self.FindWindowById(armid.CODERELATIONSHIP_COMBORTTYPE_ID)
    commitCtrl.SetLabel('Edit')
    fromCtrl.SetValue(fromName)
    toCtrl.SetValue(toName)
    rtCtrl.SetValue(pRationale)
    self.commitLabel = 'Edit'
    
  def onCommit(self,evt):
    fromCtrl = self.FindWindowById(armid.CODERELATIONSHIP_COMBOFROMCODE_ID)
    toCtrl = self.FindWindowById(armid.CODERELATIONSHIP_COMBOTOCODE_ID)
    rtCtrl = self.FindWindowById(armid.CODERELATIONSHIP_COMBORTTYPE_ID)
    self.theFromName = fromCtrl.GetValue()
    self.theToName = toCtrl.GetValue()
    self.theRelationship = rtCtrl.GetValue()

    commitTxt = self.commitLabel + ' Relationship' 
    if len(self.theFromName) == 0:
      dlg = wx.MessageDialog(self,'No from code selected',commitTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theToName) == 0):
      dlg = wx.MessageDialog(self,'No to code selected',commitTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRelationship) == 0):
      dlg = wx.MessageDialog(self,'No relationship selected',commitTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CODERELATIONSHIP_BUTTONADD_ID)

  def fromName(self): return self.theFromName
  def toName(self): return self.theToName
  def relationship(self): return self.rtLookup[self.theRelationship]
