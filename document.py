import os
import re
import csv
import pandas
import random
from random import shuffle
from path import *
from keywords import KeyWords
_keyWords = KeyWords()
_keyWords.SetCSV(KEYWORDS_PATH)
#單篇文本記錄
class Document:
    def __init__(self):
        self.id = int
        self.text = ""
        self.keys = dict()

    #設置文本真實id
    def SetId (self,id):
        self.id = id

    #設置文本內容
    def SetText(self,text):
        for i in range(len(text)):
            if (i == (len(text)-1)):
                self.text += text[i][0:]
            else:
                self.text += text[i][0:-1]
        self.SetKeys()
        #self.CleanKeys(1)

    #根據文本內容設置KEYS
    def SetKeys(self):
        for key,primary in _keyWords.GetAllKey():
            if key in self.text:
                self.keys[primary] = self.keys.get(primary, 0) + self.text.count(key)

    #根據threshold篩選key出現的次數
    def CleanKeys(self,threshold):
        delete = []
        for key,value in self.keys.items():
            if value <= threshold:
                delete.append(key)
        for item in delete:
            self.keys.pop(item)
    
    #計算跟別的document重複的key
    def SameKeyByDocument(self,document):
        same = self.keys.keys() & document.keys.keys()
        return same

    #回傳重複key的個數
    def GetSameKeyNum(self,document):
        return len(self.SameKeyByDocument(document))

    #回傳重複key的總數
    def GetSameKeyTotal(self,document):
        same = self.SameKeyByDocument(document)
        total = 0
        for key in same:
            total += int(self.keys[key])
            total += int(document.keys[key])
        return total

    #回傳跟別的document不重複的key
    def DiffKeyByDocument(self,document):
        diff = (self.keys.keys() - document.keys.keys()) | (document.keys.keys() - self.keys.keys())
        return diff 

    #回傳不同的key的個數
    def GetDiffKeyNum(self,document):
        return len(self.DiffKeyByDocument(document))        

    #回傳不同key的總數
    def GetDiffKeyTotal(self,document):
        diffA = self.keys.keys() - document.keys.keys()
        diffB = document.keys.keys() - self.keys.keys()
        total = 0
        for key in diffA:
            total += int(self.keys[key])
        for key in diffB:
            total += int(document.keys[key])
        return total

    #回傳相似的key佔全部的幾趴
    def GetSameInAmountPercentage(self,document):
        sameNum = self.GetSameKeyNum(document)
        try:
            percent = sameNum/len(self.keys.keys())
        except:
            percent = 0
        return percent

    #回傳U的趴數
    def GetUnionPercentage(self,document):
        sameNum = self.GetSameKeyNum(document)
        try:
            percent = sameNum/len(self.keys.keys()|document.keys.keys())
        except:
            percent = 0
        return percent

    #回傳key類別的個數
    def GetKeysNum(self):
        return len(self.keys)

    #回傳keys的總數
    def GetKeysTotalNum(self):
        temp = 0
        for item in self.keys.values():
            temp += int(item)
        return temp

    #回傳最大的key
    def GetLargestKey(self):
        try:
            key = sorted(self.keys.items(), key = lambda kv:(kv[1], kv[0]))[0][0]
        except:
            key = None
        return key

    #回傳最大的key是否一樣
    def CheckLargestKeyByDocument(self,document):
        if (self.GetLargestKey() == document.GetLargestKey() and self.GetLargestKey()!= None):
            return 1
        else:
            return 0

#整個資料集的所有文本
class Documents:
    def __init__(self):
        self.datas = []
    
    #根據文章id設置文本
    def AddDocument(self,lines,id):
        temp = Document()
        temp.SetId(id)
        temp.SetText(lines)
        self.datas.append(temp)
    
    #根據文章id取得文本
    def GetTextById(self,_id):
        for item in self.datas:
            if (item.id == _id):
                return item.text
        return None

    #根據文章id取得Document物件
    def GetDocuById(self,_id):
        for item in self.datas:
            if (item.id == _id):
                return item
        return None

    #讀取path的csv
    def LoadTrainData(self,path):
        all_files = os.listdir(path)
        for _file in all_files:
            Data = open(path+_file,'r', encoding = 'utf8') 
            lines = Data.readlines()  
            id = int(re.sub(".txt","",_file)) 
            self.AddDocument(lines,id)
            Data.close()

#單組的配對文本
class PairDocument:
    def __init__(self):
        self.id = int 
        self.document1 = None 
        self.document2 = None
        self.id1 = None
        self.id2 = None
        self.key1Total = None
        self.key2Total = None 
        self.key1Num = None
        self.key2Num = None 
        self.sameNum = None 
        self.sameTotal = None 
        self.diffNum = None
        self.diffTotal = None 
        self.sameAmount1Percentage = None 
        self.sameAmount2Percentage = None 
        self.unionPercentage = None
        self.isLargestSameKey = None 
        self.sameAmountTotal = None
        self.sameTotalTotal = None
        self.MulTotal = None
        self.label = None  #Yes or No
        
    #設置文本一的物件
    def SetDocumentOne(self,document):
        self.document1 = document
    
    #設置文本二的物件
    def SetDocumentTwo(self,document):
        self.document2 = document

    #設置配對文本的id
    def SetId(self,_id):
        self.id = _id

    #設置文本1文本2的id
    def SetPairIds(self,id1,id2):
        self.id1 = id1
        self.id2 = id2
    
    #設置這篇配對的label
    def SetLabel(self,label):
        self.label = label

    #計算這兩篇文本的特徵
    def SetAttributes(self):
        self.key1Total = self.document1.GetKeysTotalNum()   #文本1有的所有key的總數
        self.key2Total = self.document2.GetKeysTotalNum()   #文本2有的所有key的總數
        self.key1Num = self.document1.GetKeysNum()      #文本1有的所有key種類的總數
        self.key2Num = self.document2.GetKeysNum()      #文本2有的所有key種類的總數
        self.sameNum = self.document1.GetSameKeyNum(self.document2)     #文本1,2中一樣的key種類的總數
        self.sameTotal = self.document1.GetSameKeyTotal(self.document2)     #文本1,2中一樣的key的總數
        self.diffNum = self.document1.GetDiffKeyNum(self.document2)      #文本1,2中不一樣的key種類的總數
        self.diffTotal = self.document1.GetDiffKeyTotal(self.document2)      #文本1,2中不一樣的key的總數
        self.sameAmount1Percentage = self.document1.GetSameInAmountPercentage(self.document2)       #相似的key種類占文本1本身的%數
        self.sameAmount2Percentage = self.document2.GetSameInAmountPercentage(self.document1)       #相似的key種類占文本2本身的%數
        self.unionPercentage = self.document1.GetUnionPercentage(self.document2)        #相似的key種類占文本1文本2所有種類的%數
        self.isLargestSameKey = self.document1.CheckLargestKeyByDocument(self.document2)        #文本1文本2數量最多的那個key是否一樣
        self.sameAmountTotal = self.sameAmount1Percentage + self.sameAmount2Percentage      #各自佔的比例相加
        try:
            self.sameTotalTotal = self.sameTotal/(self.key1Total + self.key2Total)      #一樣的key總數佔文本1文本2key總數的%數
        except:
            self.sameTotalTotal = 0
        self.MulTotal = self.sameAmountTotal * self.sameTotalTotal      #將各自佔的比例x一樣的key總數佔文本1文本2key總數的%數

class PairDocuments:
    def __init__(self):
        self.index = 0
        self.datas = []
        self.documents = Documents()
        self.documents.LoadTrainData(ALL_DATA_PATH)

    #將已建立好的pairdocuments寫成csv供dnn訓練
    def OutputCSV(self,path):
        with open(path,'w',newline='',encoding='utf-8')as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['idA', 'idB','keyANum','keyBNum','keyATotal','keyBTotal','sameNum','sameTotal','diffNum','diffTotal','sameAmountAPercentage','sameAmountBPercentage','union','isLargestSameKey','sameAmountTotal','sameTotalTotal','MulTotal','label'])
            for row in self.datas:
                idA = row.id1
                idB = row.id2
                keyATotal = row.key1Total
                keyBTotal = row.key2Total
                keyANum = row.key1Num
                keyBNum = row.key2Num
                sameNum = row.sameNum
                sameTotal = row.sameTotal
                diffNum = row.diffNum
                diffTotal = row.diffTotal
                sameAmountAPercentage = row.sameAmount1Percentage
                sameAmountBPercentage = row.sameAmount2Percentage
                union = row.unionPercentage
                isLargestSameKey = row.isLargestSameKey 
                sameAmountTotal = row.sameAmountTotal
                sameTotalTotal = row.sameTotalTotal
                MulTotal = row.MulTotal
                label = row.label
                writer.writerow([idA, idB,keyANum,keyBNum,keyATotal,keyBTotal,sameNum,sameTotal,diffNum,diffTotal,sameAmountAPercentage,sameAmountBPercentage,union,isLargestSameKey,sameAmountTotal,sameTotalTotal,MulTotal,label])

    #新增一組PairDocument
    def AddOnePairDocument(self,label,id1,id2):
        temp = PairDocument()
        temp.SetDocumentOne(self.documents.GetDocuById(id1))
        temp.SetDocumentTwo(self.documents.GetDocuById(id2))
        temp.SetId(len(self.datas))
        temp.SetPairIds(id1, id2)
        temp.SetLabel(label)
        temp.SetAttributes()
        self.datas.append(temp)

    #讀取csv 
    def ReadDatasetCSV(self,path):
        datas = []
        with open(path,newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile) 
            for row in rows:
                datas.append(row)
        return datas
    
    #讀取path的label並根據建立好的documents建立計算好的測資
    def LoadTrainLabel(self,path,label):
        train = self.ReadDatasetCSV(path)[1:]
        for item in train:
            self.AddOnePairDocument(label, int(item[0]), int(item[1]))

#簡單測試Documents的功能
def main():
    _documents = Documents()
    _documents.LoadTrainData(ALL_DATA_PATH)
    print(_documents.GetDocuById(411).keys)
    print(_documents.GetDocuById(774).keys)
if __name__ == '__main__':
    main()