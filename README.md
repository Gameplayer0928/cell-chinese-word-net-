# cell-chinese-word-net-
看了一点点关于NLP和神经网络的知识，头比较晕，觉得没有怎么理解。自己按照自己理解写代码，尝试找
找文章里字与字的联系。

learn a little bit knowlage of NLP and NN,my head is dizzy,i think i am not understand 
much,so i follow my think about NLP and NN to code,try to find connection between words 
in text

基于原则和假设：完全不懂中文的人，不懂字和词的意义，但是会看字与字之间的关系，会统计字出现的
次数和字的组合出现的次数，这样找出常用字和常用字组合。我个人理解的生物体变化原则是“越用越大
，越用越强，不用就萎缩退化遗忘”，但由于计算机和人不同，所以不考虑萎缩退化遗忘。

my ruld and assume: a man dont know chinese and dont know chinese words mean,but can 
look out relation between words,and count exist time of word,find out word and word 
group usual used.i understanding the organism changes ruld is "the more use,the more 
bigger. the more use, the more stronger. No use will atrophy,degeneration and 
forget".but computer and human is different,so discard atrophy,degeneration and forget.

具体定义：1中文字为一个细胞，1个中文字与其后面的中文字关联为一个链接管。中文字出现在文章里的
次数和被提及的次数越多，其尺寸就变大。中文字与后面的中文字组合出现越多，链接管尺寸就变大。不
考虑数字、英文字符、标点符号。

detal defind: one chinese word is a Cell,one chinese word link behind another word by 
LinkTube.a same word exsit time and link time the more many, the cell size more bigger.
word link behind word exsit time the more many,LinkTube size the more bigger. exclude 
number, english word, punctuation.

![image](https://github.com/Gameplayer0928/cell-chinese-word-net-/blob/master/celltube.png)
![image](https://github.com/Gameplayer0928/cell-chinese-word-net-/blob/master/cellcellcell.png)

2018.4.3
add gui contrul and matplotlib to show two word struct vocabulary in cell group

![image](https://github.com/Gameplayer0928/cell-chinese-word-net-/blob/master/2018-04-03%2022-06-24.png)
![image](https://github.com/Gameplayer0928/cell-chinese-word-net-/blob/master/2018-04-03%2022-33-55%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)

2018.4.5
add show three word struct vocabulary in cell group

![image](https://github.com/Gameplayer0928/cell-chinese-word-net-/blob/master/2018-04-05%2021-35-49.png)
