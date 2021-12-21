import csv
import pandas as pd
from path import *
#為單組關鍵字的class
class KeyWord:
    def __init__(self):
        self.primary = ""    #定義了關鍵單組關鍵字的主體       
        self.data = []       #存放這組關鍵字的組合

    #檢查是否存在特殊符號或英文數字
    def is_all_chinese(self,strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        if strs == "":
            return False
        return True

    #將輸入的關鍵字做篩選
    def ClearData(self,data):
        newData = []
        for item in data:
            if self.is_all_chinese(item):
                newData.append(item)
        return newData

    #將單組關鍵字讀進來並設置關鍵字主題
    def SetData(self,data):
        self.data = self.ClearData(data)
        if (len(self.data)>0):
            self.primary = self.data[0]

    #搜尋輸入的單詞是否屬於這個關鍵字
    def SearchInData(self,test):
        if (test in set(self.data)):
            return True
        else:
            return False 

#存取了所有關鍵字並能使用一些特化功能
class KeyWords:
    def __init__(self):
        self.datas = []

    #新增一組關鍵字
    def AddKeyWord(self,item):
        temp = KeyWord()
        temp.SetData(item)
        self.datas.append(temp)

    #取的字串在關鍵字集合裡的主體
    def GetKeyWord(self,string):
        for key in self.datas:
            if key.SearchInData(string):
                return key.primary
        return None

    #回傳所有Key
    def GetAllKey(self):
        keys = []
        for item in self.datas:
            for key in item.data:
                keys.append([key,item.primary])
        return keys
    
    #讀取csv
    def ReadDatasetCSV(self,path):
        datas = []
        with open(path,newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile) 
            for row in rows:
                datas.append(row)
        return datas

    #透過路徑的csv設定關鍵詞組
    def SetCSV(self,path):
        datas = self.ReadDatasetCSV(path)
        for item in datas:
            self.AddKeyWord(item)

    
#簡單測試了KeyWords的功能
def main():
    Words = KeyWords()
    Words.SetCSV(KEYWORDS_PATH)
    print(Words.GetKeyWord('鋅錳乃浦水懸劑'))

if __name__ == '__main__':
    main()