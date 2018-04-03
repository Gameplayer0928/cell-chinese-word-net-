# coding=utf-8
'''
Created on 2018��3��19��
 @author: Gameplayer0928 Qi Gao
'''

import sys
import codecs
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import matplotlib.pyplot as plt

import numpy as np


plt.rcParams[u'font.sans-serif'] = ['simhei']      # 指定默认字体

plt.rcParams['axes.unicode_minus'] = False        # 解决保存图像是负号'-'显示为方块的问题


FD = None
CODE = None

if sys.platform == 'linux':
    FD = ".\\"
    CODE = "utf-8"
elif sys.platform == "win32":
    FD = "./"
    CODE = "gbk"
    
TAV = np.dtype([("text",np.unicode_,2),("value",np.int)])
    
class Cell():
    ''' cell is the smallies element of textbrain,
        text = one text,
        size = cell use times, the more use the more bigger,
        link = link anther cell
    '''
    def __init__(self):
        self.text = ""
        self.size = 0
        self.link = []
        

class LinkTube():
    ''' linktube is the smallies element of textbrain,
        size = linktube use times, the more use the more bigger,
        selfside = link a cell 
        otherside = link other cell
    '''
    def __init__(self):
        self.size = 0
        self.selfside = None
        self.otherside = None

class CellGroup(list):
    ''' group of cell, include cell and linktube
    '''
    def __init__(self):
        list.__init__(self)
        self.cellge = []
        
    def add(self,obj):
        if obj.text in self.cellge:
            raise(Exception(" every cell must be only one "))
        else:
            self._eleget(obj)
            self.append(obj)
            
    
    def _eleget(self,obj):
        self.cellge.append(obj.text)
    
    def group_size(self):
        return len(self)

    def get_biggest_tube_size(self):
        biggesttubesize = 0
        for i in self:
            for x in i.link:
                if x.size > biggesttubesize:
                    biggesttubesize = x.size
        return biggesttubesize
    
    def get_biggest_cell_size(self):
        biggestcellsize = 0
        for i in self:
            if i.size > biggestcellsize:
                biggestcellsize = i.size
        return biggestcellsize
          
def create_cell_group(text):
    ''' get cell of the first exist '''
    cellgroup = CellGroup()
    textset = set(text)
    for i in textset:
        if ord(i) > 0x4e00 - 1 and ord(i) < 0xfa64:   # just include chinese word, no other symbol
            ce = Cell()
            ce.text = i
            cellgroup.add(ce)
    return cellgroup


def create_cell_link(cellgroup,text):
    ''' create link between cell, count cell and linktube size '''
    textcount = len(text)
    cellgroupcount = cellgroup.group_size()
    
    for i in cellgroup:
        for z in text:
            if i.text == z:
                i.size = 1
                i.link.append(LinkTube())
                
    for i in cellgroup:
        for z in i.link:
            z.selfside = i

##############################################################################  from cellgroup get current word
    for i in range(textcount-1):
        for z in range(cellgroupcount):
            if text[i] == cellgroup[z].text:
###############################################################################  from cellgroup get next word
                for p in range(cellgroupcount):
                    if text[i+1] == cellgroup[p].text:
###############################################################################  set linktube in between cell
                        for x in range(len(cellgroup[z].link)):
                            if cellgroup[z].link[x].otherside == None:
                                cellgroup[z].link[x].size += 1
                                cellgroup[p].size += 1
                                cellgroup[z].link[x].otherside = cellgroup[p]
                                break
                            elif cellgroup[z].link[x].otherside.text == cellgroup[p].text:
                                cellgroup[z].link[x].size += 1
                                cellgroup[p].size += 1
                                break
                            else:
                                pass

# 从输入文章寻找与字列相同的字
# 找到后，在文章寻找下一字与字列相同的字
# 将在字列中找到的字用链接管链接
# 将在字列中找到的字加大1尺寸
# 将链接管加大1尺寸
################################################################################ clean linktube of size is 0                    
    for i in range(cellgroupcount):
        searchtime = len(cellgroup[i].link)
        count = 0
        bcount = 0
        while count < searchtime - bcount:
            if cellgroup[i].link[count].size == 0:
                cellgroup[i].link.pop(count)
                bcount += 1
            else:
                count += 1
     
def show_cellgroup(cellgroup):
    ''' show cellgroup inside '''
    for i in cellgroup:
        print("main : %s,%d"%(i.text,i.size))
        for x in i.link:
            if x.otherside == None:
                print("lts : %d"%(x.size))
            else:
                print("lts : %d, otherside : %s, osize : %d"%(x.size,x.otherside.text,x.otherside.size))
        print("---------------------------------------------------------")

def get_two_word_vocabulary(cellgroup,pc = 0.5):
    ''' get two word struct vocabulary of chinese,
        cellgroup = input CellGroup,
        pc = get size of percent for biggest LinkTube
    '''
    biggesttubesize = cellgroup.get_biggest_tube_size()
    vocL = []
#     vocV = []               
    biggesttubesize *= pc
    
    for i in cellgroup:
        for x in i.link:
            if x.size > biggesttubesize:
                vocL.append((x.selfside.text + x.otherside.text,x.size))
    return vocL
    
class MainGui():
    def __init__(self):
        self.maingui = tkinter.Tk()
        self.maingui.title("Cell")
########################################################################################################
        frame1 = tkinter.Frame(self.maingui)
        button1 = tkinter.Button(frame1,text="1.input text",command=self._load_txt)
        button1.pack(side = "left")
#-------------------------------------------------------------------------------------------------------
        button2 = tkinter.Button(frame1,text="2.Cell dispose",command=self._cell_dispose,bg = 'red')
        button2.pack(side = "left")
#------------------------------------------------------------------------------------------------------
        button3 = tkinter.Button(frame1,text="show cellgroup in CLI",command=self._show_cellgroup,bg = 'green')
        button3.pack(side = "right")
        frame1.pack()
#####################################################################################################        
        frame2 = tkinter.Frame(self.maingui,relief = "groove",borderwidth = 1)
        showlabel = tkinter.Label(frame2,text = "3.set config of getted two word struct vocabulary")
        showlabel.pack()
#--------------------------------------------------------------------------------------------------        
        frame2_1 = tkinter.Frame(frame2)
        label1 = tkinter.Label(frame2_1,text = "set precent (0.0~1.0):")
        label1.grid(row = 0,column=0)
        self.entry1 = tkinter.Entry(frame2_1)
        self.entry1.grid(row=0,column=1)
#---------------------------------------------------------------------------------------------------
        label2 = tkinter.Label(frame2_1,text = "set tick size:")
        label2.grid(row = 1,column=0)
        self.entry2 = tkinter.Entry(frame2_1)
        self.entry2.grid(row=1,column=1)
#---------------------------------------------------------------------------------------------------
        label3 = tkinter.Label(frame2_1,text = "set tick rotate:")
        label3.grid(row = 2,column=0)
        self.entry3 = tkinter.Entry(frame2_1)
        self.entry3.grid(row=2,column=1)
        frame2_1.pack()
#---------------------------------------------------------------------------------------------------
        button4 = tkinter.Button(frame2,text="set and show in matplotlib",command=self._pt)
        button4.pack()
        frame2.pack()
####################################################################################################   
     
        self.textfile = None
        self.text = None
        
        self.cellgroup = None
        
        self.vocpercent = None
        self.ticksize = None
        self.tickrotate = None
        
        self.vocL = None
        
        self.maingui.mainloop()
        
    def _load_txt(self):
        try:
            fd = tkinter.filedialog.FileDialog(self.maingui,title="select txt file")
            self.textfile = fd.go(FD)
            filea = codecs.open(self.textfile,'r',encoding=CODE)
            self.text = filea.read()
            filea.close()
        except:
            tkinter.messagebox.showerror(title="text input error", message="please input text file correct,may be file encoding problem")
    
    def _cell_dispose(self):
        try: 
            self.cellgroup = create_cell_group(self.text)
            tkinter.messagebox.showinfo(title = "create and link cell group process", message = "cell group has been created,\
next will create link in cell group,\
this step spending time depand with text file size,\
just please wait. went its done, will give a messagebox.\
 click 'OK' to contiue")
            create_cell_link(self.cellgroup, self.text)
            tkinter.messagebox.showinfo(title = "process compeled", message = "ready for show in matplotlib")
        except:
            tkinter.messagebox.showerror(title="error", message="prestep something wrong")
            
    
    
    def _show_cellgroup(self):
        try:
            show_cellgroup(self.cellgroup)
        except:
            tkinter.messagebox.showerror(title="error", message="prestep something wrong")
    
    def _pt(self):
        try:
            self.vocpercent = float(self.entry1.get())
            self.ticksize = float(self.entry2.get())
            self.tickrotate = float(self.entry3.get())
            if self.vocpercent > 1.0 or self.vocpercent < 0.0:
                self.vocpercent = None
                tkinter.messagebox.showerror(title = "error", message="config setting must follow tips")
            else:
                try:
                    self.vocL = np.array(get_two_word_vocabulary(self.cellgroup, self.vocpercent),dtype = TAV)
                    ax1 = plt.subplot(111)
                    ax1.bar(self.vocL["text"],self.vocL["value"])
                    ax1.tick_params('x',rotation = self.tickrotate,labelsize = self.ticksize)
                    plt.grid(True,alpha=0.5)
                    plt.show()
                except:
                    tkinter.messagebox.showerror(title="step error", message="prestep something wrong")
        except:
            self.vocpercent = None
            tkinter.messagebox.showerror(title = "error", message="config setting must follow tips")
            
#         print(self.inputtext)
        
if __name__ == "__main__":
    MG = MainGui()

