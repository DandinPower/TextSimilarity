import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix  
from keras.models import Sequential
from keras.layers import Dense   
from path import *

class Train:
    def __init__(self):
        self.X = None
        self.y = None 
        self.X_new = None
        self.X_train = None
        self.X_test = None 
        self.y_train = None 
        self.y_test = None
        self.classifier = None  
        self.dataSet = None
        self.data = None
        self.result = None
        self.sc = None
    
    #特徵工程selectKbest
    def CleanAttributes(self):
        kbest = SelectKBest(chi2, k=8)
        self.X_new = kbest.fit_transform(self.X, self.y)
        #6, 7, 8, 9, 10, 13, 14, 16 為篩選出來的結果

    #輸入firstTrain path
    def TrainFirst(self,path):
        dataset = pd.read_csv(path)
        #self.X = dataset.iloc[:, 2: 17].values
        dataSet = dataset.iloc[:, 6: 17]
        dataSet = dataSet.drop(['sameAmountBPercentage','union','sameTotalTotal'],axis = 1)
        self.X = dataSet.values
        self.X = self.X.astype('float64')
        self.y = dataset.iloc[:, 17].values
        print(len(self.X[0]))

    #做特徵標準化
    def Standardization(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size = 0.2, random_state = 0)
        N, D = self.X_train.shape
        self.sc = StandardScaler()
        self.X_train = self.sc.fit_transform(self.X_train)
        self.X_test = self.sc.transform(self.X_test)

    #創建模型
    def CreateClassifier(self):        
        self.classifier = Sequential()                                                                                                                
        self.classifier.add(Dense(units=4,activation='relu',kernel_initializer='uniform'))
        self.classifier.add(Dense(units=1,activation='sigmoid',kernel_initializer='uniform'))
        self.classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

    #訓練模型
    def Fit(self,batch,epoch):
        self.classifier.fit(self.X_train,self.y_train,batch_size=batch,epochs=epoch)
        print("Train score:", self.classifier.evaluate(self.X_train, self.y_train))
        print("Validation score:", self.classifier.evaluate(self.X_test, self.y_test))

    #根據threshold來驗證模型
    def Validation(self,threshold):
        y_pred = self.classifier.predict(self.X_test)
        y_pred = (y_pred > threshold) #第一次0.05      
        # Making the Confusion Matrix
        cm = confusion_matrix(self.y_test, y_pred)
        TN,FP,FN,TP = cm[0][0],cm[0][1],cm[1][0],cm[1][1] 
        precision = TP/(TP+FP)
        recall = TP/(TP+FN) 
        score = (2*precision*recall)/(precision+recall)
        print(f'TN: {TN},FP: {FP},FN: {FN},TP: {TP}')
        print(f'score: {score},precision: {precision},recall: {recall}')

    #設置待預測的path
    def SetData(self,path):
        self.dataSet = pd.read_csv(path) 
        dataSet = self.dataSet.iloc[:, 6: 17]
        dataSet = dataSet.drop(['sameAmountBPercentage','union','sameTotalTotal'],axis = 1)
        self.data = dataSet.values
        self.data = self.data.astype('float64')
        print(self.data.shape)
        self.data = self.sc.transform(self.data)

    #預測模型
    def PredictTrain(self,threshold,path,mode): 
        self.result = self.classifier.predict(self.data)
        self.result = (self.result > threshold)      
        self.dataSet['predict'] = self.result  
        filter = (self.dataSet['predict'] == 1)
        self.dataSet = self.dataSet[filter]
        self.dataSet = self.dataSet.drop(['predict'],axis = 1)
        self.dataSet = self.dataSet.drop_duplicates()
        if (mode):
            self.dataSet.to_csv(path, index = False)

    #預測模型
    def PredictTest(self,threshold,path,mode):
        self.result = self.classifier.predict(self.data)
        self.result = (self.result > threshold)
        self.dataSet = self.dataSet.drop(['label'],axis = 1)
        self.dataSet['label'] = self.result
        filter = (self.dataSet["label"] == 1)
        self.dataSet = self.dataSet[filter]
        self.dataSet = self.dataSet.drop_duplicates()
        if (mode):
            self.dataSet.to_csv(path, index = False)

    #產生answer
    def GenerateAnswer(self,path):
        answerDf = self.dataSet.drop(['keyANum','keyBNum','keyATotal','keyBTotal','sameNum','sameTotal','diffNum','diffTotal','sameAmountAPercentage','sameAmountBPercentage','union','isLargestSameKey','sameAmountTotal','sameTotalTotal','MulTotal','label'],axis = 1)
        answerDf.to_csv(path, index = False)

def FirstTrain():
    first_train = Train()
    first_train.TrainFirst(FIRST_TRAIN)
    first_train.Standardization()
    first_train.CreateClassifier()
    first_train.Fit(100,20)
    print('訓練完畢')
    first_train.Validation(0.05)
    first_train.SetData(FIRST_TRAIN)
    first_train.PredictTrain(0.05, SECOND_TRAIN,True)
    print('產生二次訓練集完畢')
    first_train.SetData(FIRST_PUBLIC)
    first_train.PredictTest(0.05, SECOND_PUBLIC,True)
    print('產生二次測試集完畢')
    first_train.SetData(FIRST_PRIVATE)
    first_train.PredictTest(0.05, SECOND_PRIVATE,True)
    print('產生二次測試集完畢')

def SecondTrain():
    second_train = Train()
    second_train.TrainFirst(SECOND_TRAIN)
    second_train.Standardization()
    second_train.CreateClassifier()
    second_train.Fit(60,30)
    print('訓練完畢')
    second_train.Validation(0.35)
    second_train.SetData(FIRST_PUBLIC)
    second_train.PredictTest(0.35, SECOND_PUBLIC,False)
    second_train.GenerateAnswer(ANSWER_PUBLIC)
    print('產生測試集答案完畢')
    second_train.SetData(FIRST_PRIVATE)
    second_train.PredictTest(0.35, SECOND_PRIVATE,False)
    second_train.GenerateAnswer(ANSWER_PRIVATE)
    print('產生測試集答案完畢')

def main():
    FirstTrain()
    SecondTrain()

if __name__ == '__main__':
    main()
