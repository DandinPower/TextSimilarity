import csv
from random import shuffle
import random
import pandas as pd 
import re
import os
from document import Document,Documents,PairDocument,PairDocuments
from generateLabel import NewTrain,NewTest
from path import *

def main():
    GenerateFirstTrain()

#產生第一次訓練所需在colab做
def GenerateFirstTrain():
    GenerateTrainLabel()
    GenerateTestLabel()  
    GenerateTrain(POSITIVE_LABEL_PATH, NEGATIVE_LABEL_PATH)
    GenerateTest(PUBLIC_LABEL_PATH, FIRST_PUBLIC)
    GenerateTest(PRIVATE_LABEL_PATH, FIRST_PRIVATE)

#根據TrainLabel跟FailLabel產生Train的訓練集
def GenerateTrain(positivePath,negativePath):
    pairDocuments = PairDocuments()
    pairDocuments.LoadTrainLabel(positivePath, 1)
    pairDocuments.LoadTrainLabel(negativePath, 0)
    pairDocuments.OutputCSV(FIRST_TRAIN)
    print('First_Train產生完畢')
    
#根據label產生訓練集
def GenerateTest(labelPath,outputPath):
    pairDocuments = PairDocuments()
    pairDocuments.LoadTrainLabel(labelPath,2)
    pairDocuments.OutputCSV(outputPath)
    print('First_Test產生完畢')

#產生FailLabel
def GenerateTrainLabel():
    newTrain = NewTrain()
    newTrain.SetDatasToId(TRAIN_DATA_PATH)
    newTrain.GenerateNewData(0)
    newTrain.GenerateCSV(NEGATIVE_LABEL_PATH)
    print("產生訓練集label完畢")

#產生public跟private的label
def GenerateTestLabel():
    newTest = NewTest()
    newTest.SetDatasToId(PRIVATE_DATA_PATH)
    newTest.GenerateNewData()
    newTest.GenerateCSV(PRIVATE_LABEL_PATH)
    newTest = NewTest()
    newTest.SetDatasToId(PUBLIC_DATA_PATH)
    newTest.GenerateNewData()
    newTest.GenerateCSV(PUBLIC_LABEL_PATH)
    print("產生測試集label完畢")
if __name__ == '__main__':
    main()