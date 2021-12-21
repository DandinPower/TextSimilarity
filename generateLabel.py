import csv
import os
import re
import random
from path import *

#紀錄已存在的pair組合
class UseDataSet:
    def __init__(self):
        self.datas = []
    
    #讀取待記錄得path
    def ReadDatasetCSV(self,path):
        datas = []
        with open(path,newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile) 
            for row in rows:
                datas.append(row)
        return datas
    
    #設置組合
    def SetDatas(self,path):
        self.datas = self.ReadDatasetCSV(path)[1:]

    #檢查id組合是否配對
    def CheckIsIn(self,check):
        for data in self.datas:
            if (str(check[0]) == data[0]) and (str(check[1])==data[1]):
                return True
        return False 

#產生Fail的Train組合      
class NewTrain:
    def __init__(self):
        self.datas = []
        self.ids = []
        self.use = UseDataSet()
        self.use.SetDatas(POSITIVE_LABEL_PATH)

    #讀取路徑的id
    def SetDatasToId(self,path):
        all_files = os.listdir(path)
        for _file in all_files:
            id = int(re.sub(".txt","",_file))
            self.ids.append(id) 
    
    #產生fail 
    def GenerateNewData(self,sample):
        self.datas = []
        selfduc = 0
        usefduc = 0
        for i in range(len(self.ids)):
            for j in range(len(self.ids)):
                if (i==j):
                    selfduc +=1
                elif (self.use.CheckIsIn([self.ids[i],self.ids[j]])):
                    usefduc +=1
                else:
                    check = random.randint(0, sample)
                    if (check == 0):
                        self.datas.append([i,j])
        print(f'self{selfduc},use{usefduc}')
            
    #根據結果生成faillabel
    def GenerateCSV(self,path):
        with open(path,'w',newline='')as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Test","Reference"])
            for item in self.datas:
                item[0] = str(self.ids[item[0]])
                item[1] = str(self.ids[item[1]])
                writer.writerow(item)

#產生public或private的所有label組合
class NewTest:
    def __init__(self):
        self.datas = []
        self.ids = []

    #設置id 
    def SetDatasToId(self,path):
        all_files = os.listdir(path)
        for _file in all_files:
            id = int(re.sub(".txt","",_file))
            self.ids.append(id) 
        print(len(self.ids))
    
    #產生所有組合 
    def GenerateNewData(self):
        self.datas = []
        for i in range(len(self.ids)):
            for j in range(len(self.ids)):
                if (i != j):
                    self.datas.append([i,j])
            
    #根據結果產生csv
    def GenerateCSV(self,path):
        with open(path,'w',newline='')as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Test","Reference"])
            for item in self.datas:
                item[0] = str(self.ids[item[0]])
                item[1] = str(self.ids[item[1]])
                writer.writerow(item)

def main():
    pass

if __name__ == '__main__':
    main()