---
title: NTU Machine Learning Homework 1
tags: [NTU_ML, Machine Learning, NTU]

category: "Security Course｜NTU ML"
date: 2023-01-16
---

# NTU Machine Learning Homework 1
<!-- more -->
###### tags: `NTU_ML` `Machine Learning`

## How to choose features of data
* After observing the training data visualized image, you can be aware of the relationship between the PM2.5 feature and the others.
* For instance, the CO image, NO image, NO2 image, and NOx image are much more correlated with PM2.5.
![co](https://imgur.com/73t0b9Q.png)![no](https://imgur.com/tSGtNe9.png)![no2](https://imgur.com/IobYzpN.png)![nox](https://imgur.com/vyz8COx.png)![pm2.5](https://imgur.com/acbWSvK.png)
* I also choose PM10, WS_HR, RAINFALL, RH,  WIND_SPEED, and PM2.5 which you can see [here](/HW1/Programming/train_data_img/)
* I used Zscore normalization to implement in my project and can see as below![zscore_CO](https://imgur.com/BTmhmRm.png)![zscore_NO](https://imgur.com/7mz2uHW.png)![zscore_NO2](https://imgur.com/NiF1vxl.png)![zscore_NOx](https://imgur.com/gW6xij3.png)
* You can see the different result of using or unusing normalization with the same config.
| Epoch | Regression | LR | Feats | Batch Size | Loss Fn. |  Opti. | RMSE | Data Filter | Norm. Data |
| :------: | :------: | -------- | :------: | :------: | :------: | :------: | :------: | :------:  | :------:  |
| 200  | 1st-order| 0.015  | [1-4, 6-9, 13, 14]     | 1024 |   MSE     | Adam     | 2.44623 | Yes|Yes|
| 200  | 1st-order| 0.015  | [1-4, 6-9, 13, 14]     | 1024 |   MSE     | Adam     | 2.44623 | Yes|No|

## Hyperparameter and Preprocessing
* All my testing config can be found in Training Result.xlsx
* I used a filter to choose valid data and set a threshold by observing the visualized figure of all features.

## My takeaway
* **(Solved->See the last paragraph)**Using normalization is not like what I thought. Practically speaking, using normalization can gather all data to a specific area that the model can converge much more rapidly. But, in this case, the result is worse and also appear negative value of the PM2.5 result. According to [this page](https://blog.csdn.net/u010947534/article/details/86632819?spm=1001.2014.3001.5506), maybe the normalization method is not suitable in my case.
* **(Solved->See the last paragraph)**I also figured that using the stored weight and bias by my pretrained model is not the right way. I used pickle to store the dump parameters during the training and used the best one as my pretrained parameter. But it's still not that good enough.
* The better way in this project to enhance your accuracy is tuning your training config and select  good features.
* After discussing with my friend, I figured out the problem and tried to solve it successfully by fitting numpy random seed. Then, the parameter will truly fix but normalization **is still not working** to help model converging.

## Update

* 2022/12/06 update - Refer to [相關](https://www.youtube.com/watch?v=z-21v0EoFh4&ab_channel=CUSTCourses) taught by Dr.李柏堅, I use `Pearson Correlation` to compute the correlation of each factor and PM2.5 and the result is shown as below. According to the [video](https://www.youtube.com/watch?v=z-21v0EoFh4&ab_channel=CUSTCourses), `|r| < 0.4` is low correlation, `0.4 ≦ |r| < 0.7`is medium correlation, and `0.7 ≦ |r| < 1` is high correlation. So, the factor **<font color=#FF0000>**`CO`, `NO`, `NO2`, `NOx`, `PM10`, and `SO2`**</font>**  are quite suitable as our input data to address this regression problem.

    |Factor|AMB_TEMP|CO|NO|NO2| NOx|O3| PM10| WS_HR| RAINFALL| RH| SO2| WD_HR| WIND_DIREC|WIND_SPEED|
    | :----: | :------------: | :-----------: | :-----------: | :-----------: | :----------: | :----------- | :----------- | :------------: | :------------: | :------------: | :-----------: | :-----------: | :-----------: | :-----------: |
    | r      | -0.176147465   | 0.659147668   | 0.227219147   | 0.554273687   | 0.51365014   | 0.233923944  | 0.818868214  | -0.102047405   | -0.060801221   | -0.081576429   | 0.361333416   | 0.171932397   | 0.137658351   | -0.10119696   |