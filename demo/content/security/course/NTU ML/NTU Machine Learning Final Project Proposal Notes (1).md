---
title: NTU Machine Learning Final Project Proposal Notes
tags: [NTU_ML, Machine Learning, NTU]

---

# NTU Machine Learning Final Project Proposal Notes
###### tags: `NTU_ML` `Machine Learning`
| Paper | Used Technique / Ingenuity| Suitable / Unsuitable Reason| Replace to |
|:-----:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |:----------:|
|  [1]  | Models overview<br><li>3D maps of gray and/or white matter (deep learning models: six layer CNN, ResNet, and Inception V1)</li><li>vertex wise measurements from the surface-based processing (models BLUP and SVM)</li><br />Model 1: Best Linear Unbiased Predictor(BLUP)</br>Model 2: Support Vector Regression</br>Model 3: Six-Layer Convolutional Neural Networks</br>Model 4: Specialized Six-Layer Convolutional Neural Networks for Younger and Older Subjects</br>Model 5: ResNet</br>Model 6: Inception V1</br></br> Additional Experiments<li>Different Types of Model Combination: Linear Regression vs. Random Forest</li><li>Combining Seven (Identical) Convolutional Neural Networks or the Seven Best Epochs</li><li>Influence of the Type of Brain Features on Prediction Accuracy</li> |Suitable:</br>In this field, it's very clearly on comparing 6 variety models which can help us to know the implementation what we learned in class.</br>Also can aware of the result between high level model and custom level model</br></br>For linear regression and random forest, they trained the **ensemble algorithms** on a random subset. They repeated this process 500 times to get a bootstrap estimate of the SE of the MAE.   | N/A   |
| [2]     |2D and 3D-CNN on age estimation<li>For 2D-CNN, we consider the features as an image of size 168×60 (DH×M) ignoring the days as temporal information.</li><li>However, for 3D-CNN, we consider the features as a 3D volume with temporal information across the days, where each day has 24 hours and an hour is 60 minutes. So to break it down, we represent the features as a three dimensional information of 7×24×60 (D×H×M) minutes.</li>| Unsuitable:</br> Though the topic is interesting, the technique content is less then expectation and the .| No Idea Yet     |
| [3]     | Model for classification:</br>Random Forest, GLMNet, SVM(including e1071, which is a package of LibSVM in R language, LiblinearR, kernlab, Rgtsvm),  and xgboost</br></br>Calibration Algorithm(i.e. post-processing):logistic regression(GLM function), BRGLM, GLMNet</br></br>Performance evaluation: HandTill2001| Suitable:</br>The reason is as the same as [1] which also used various methods and compare it to other papers detailed.| N/A     |

## Appendix
* The custom model in <font color=Red>[1]</font>
![proposed six-layer CNN](https://imgur.com/JXPDeLS.png)

* Self-defined ResNet in <font color=Red>[1]</font>
![](https://imgur.com/4VmhNRg.png)

* Self-defined Inception V1 in <font color=Red>[1]</font>
![](https://imgur.com/je2cCQL.png)

* The whole result of experience in <font color=Red>[1]</font>
![](https://imgur.com/xgASnkl.png)

* Architecture of the proposed DL methods in <font color=Red>[2]</font>
![Architecture of the proposed DL methods](https://imgur.com/7Okv3TC.png)

* The reuslt in <font color=Red>[3]</font>
![](https://imgur.com/HDYFr36.png)

## Reference
[1]Machine learning workflows to estimate class probabilities for precision cancer diagnostics on DNA methylation microarray data
[2]Estimating Biological Age from Physical Activity using Deep Learning with 3D CNN
[3]Ensemble Learning of Convolutional Neural Network, Support Vector Machine, and Best Linear Unbiased Predictor for Brain Age Prediction