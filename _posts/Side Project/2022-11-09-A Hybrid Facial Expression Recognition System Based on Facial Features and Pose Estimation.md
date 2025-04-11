---
title: A Hybrid Facial Expression Recognition System Based on Facial Features and Pose Estimation
tags: [NTUST, Special Topic]

---

# A Hybrid Facial Expression Recognition System Based on Facial Features and Pose Estimation
###### tags: `NTUST` `Emotional Recognition` `Openpose` `PyTorch` `Special Topic`
:::spoiler
[TOC]
:::

## Author
JING-MING GUO<sup>1</sup>, (Senior Member, IEEE), CHIH-HSIEN HSIA<sup>2</sup>,  (Member, IEEE), PING-HSUEH HO<sup>1</sup>, (Bachelor), YANG-CHEN CHANG<sup>1</sup>, (Bachelor)

<sup>1</sup>Department of Electrical Engineering, National Taiwan University of Science and Technology
Taipei City 106, Taipei County, Taiwan
<sup>2</sup>Department of Computer Science and Information Engineering, National Ilan University, Yilan City 260, Yilan County, Taiwan

<sup>1</sup>jmguo@mail.ntust.edu.tw, bernie6401@gmail.com, Max.chang965132@gmail.com
<sup>2</sup>chhsia625@gmail.com

## Data
The datasets are placed in the datasets folder, we prepare them as the link you can download by correct structure, please see the [data readme](datasets/README.txt).

In the folder, we just use [GEMEP dataset](https://www.unige.ch/cisa/gemep) that has whole body including face and body especially as our research data and compare with [other paper](https://ieeexplore.ieee.org/abstract/document/8769871).

## Models
The modes' weights are placed in the models folder, we prepare them as the link you can download by correct structure, please see [model readme](models/README.txt).

We use [Fusing Body Posture model](https://github.com/filby89/body-face-emotion-recognition) as our body model and also use [ARM model](https://github.com/JiaweiShiCV/Amend-Representation-Module) as our face model. We also use  weights that ARM team(named epoch59_acc0.9205.pth in download link) and Fusing Body team provided as our pretrained weight respectively.

Our model structure is as below:

<img src="./models/model_structure.png" alt="IMG1" style="zoom:75%;" />

## Run
> Setup environment:

```
pip install -U scikit-learn
conda install -c conda-forge matplotlib
conda install -c conda-forge argparse
conda install -c conda-forge tqdm
conda install -c conda-forge wandb
conda install -c anaconda pillow
```

> Demo GEMEP with 7 classes
```
python test_leave_one_out.py -p --data_type GEMEP --num_classes 7
```
> Demo GEMEP with 12 classes
```
python test_leave_one_out.py -p --data_type GEMEP --num_classes 12
```

## Result
### 7 Classes - Face / Body / Whole
<img src="./Confusion_matrix/GEMEP_Face7_acc0.66.png"/>
<img src="./Confusion_matrix/GEMEP_Body7_acc0.5833.png"/>
<img src="./Confusion_matrix/GEMEP_Whole7_acc0.6734.png"/>

### 12 Classes - Face / Body / Whole
<img src="./Confusion_matrix/GEMEP_Face12_acc0.5083.png"/>
<img src="./Confusion_matrix/GEMEP_Body12_acc0.525.png"/>
<img src="./Confusion_matrix/GEMEP_Whole12_acc0.6083.png"/>

## More Detail
You can download [here](./A_Hybrid_Facial_Expression_Recognition_System_Based_on_Facial_Features_and_Pose_Estimation.pdf) for more experience detail such as platform, software version, or hyper parameters, etc.


## Update
* 2022/08/14 update dataset_leave_one_out.py and test_leave_one_out.py files about adding emo_tranform() function in former file to parse num_classes argument and let the user used it more convenient. Now you can just use the comment above and no need to adjust any code in any file in testing mode.