# coding=utf-8
'''
Created on 2018��3��19��
 @author: Gameplayer0928 Qi Gao
'''



textfile = ".\\example3.txt"

tfe = open(textfile,'r')
dr = tfe.read()
tfe.close()


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
    biggesttubesize *= pc
    
    for i in cellgroup:
        for x in i.link:
            if x.size > biggesttubesize:
                vocL.append(x.selfside.text + x.otherside.text)
    return vocL
    
    
                
        
cellgroup = create_cell_group(dr)                              
   
create_cell_link(cellgroup,dr)
   
show_cellgroup(cellgroup)
 
ab = get_two_word_vocabulary(cellgroup,0.15)
print(ab)
