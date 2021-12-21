# TextSimilarity

---

### 環境安裝

- 在Colab可以直接上面運行
- 安裝以下函式庫
    
    > numpy
    > 
    > 
    > matplotlib
    > 
    > pandas
    > 
    > sklearn
    > 
    > keras
    > 
    > csv
    > 

---

### 使用說明

- 運行preprocess.py來產生Label跟訓練集
    
    ```bash
    python preprocess.py
    ```
    
- 運行train.py來訓練模型跟產生答案
    
    ```bash
    python train.py
    ```
    

---

### 文件放置

- 透過更改path.py裡的參數可以更改文件放置位置
    
    > KEYWORDS_PATH                                  存放主辦方提供的關鍵字資料
    > 
    > 
    > ALL_DATA_PATH                                     存放主辦方提供的所有文本資料                                       
    > 
    > TRAIN_DATA_PATH                                 存放主辦方提供的訓練集資料                                   
    > 
    > PUBLIC_DATA_PATH                               存放主辦方提供的Public測試集資料
    > 
    > PRIVATE_DATA_PATH                              存放主辦方提供的Private測試集資料
    > 
    > NEGATIVE_LABEL_PATH                         存放訓練集的Negative Label組合
    > 
    > POSITIVE_LABEL_PATH                           存放主辦方提供的Positive Label組合
    > 
    > PUBLIC_LABEL_PATH                              存放所有Public的Label組合(N*(N-1))
    > 
    > PRIVATE_LABEL_PATH                            存放所有Private的Label組合(N*(N-1))
    > 
    > FIRST_TRAIN                                          存放根據Label產生出來的訓練集(第一次訓練)
    > 
    > FIRST_PUBLIC                                        存放根據Label產生出來的Public測試集(第一次篩選)
    > 
    > FIRST_PRIVATE                                      存放根據Label產生出來的Private測試集(第一次篩選)
    > 
    > SECOND_TRAIN                                    存放第一次訓練完篩選後產生出來的訓練集
    > 
    > SECOND_PUBLIC                                  存放第一次篩選後產生出來的Public測試集
    > 
    > SECOND_PRIVATE                                 存放第一次篩選後產生出來的Private測試集
    > 
    > ANSWER_TRAIN                                   存放最後的訓練答案
    > 
    > ANSWER_PUBLIC                                  存放最後的Public答案
    > 
    > ANSWER_PRIVATE                                存放最後的Private答案
    > 

---