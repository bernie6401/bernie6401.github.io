---
title: NTU Machine Learning Homework 2
tags: [NTU_ML, Machine Learning, NTU]

category: "Security > Course > NTU ML"
---

# NTU Machine Learning Homework 2
###### tags: `NTU_ML` `Machine Learning`
:::spoiler Click to open TOC
[TOC]
:::

## Objective
We'd like to classify human-being emotion by using CNN model that self-construct or others ready-made such as ResNet or VGG model.

## Data
We used emotional dataset from [FER2013](https://www.kaggle.com/datasets/msambare/fer2013?datasetId=786787&sortBy=dateRun&tab=profile) that were preprocessed by lecture TA.

## Models
* Originial
    ```python
    self.conv_0 = nn.Sequential(
        nn.Conv2d(1, 64, kernel_size=3, padding=1),
        nn.BatchNorm2d(64, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),
    )
    ```
* I've used 3-level model for training but not have good result
    ```python
    self.conv_3layer = nn.Sequential(
        nn.Conv2d(1, n_chansl, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, 32, 32, 32)->(B, C, H, W)

        nn.Conv2d(n_chansl, n_chansl//2, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl//2, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, 64, 16, 16)->(B, C, H, W)

        nn.Conv2d(n_chansl//2, n_chansl//4, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl//4, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, 128, 8, 8)->(B, C, H, W)
    )
    self.fc_3layer = nn.Sequential(
        nn.Linear(n_chansl//4 * 8 * 8, 7),
    )
    ```
* I've also used 4-layer that the channel increase in the first three layers and decrease the channel at the last layer but still not good enough
    ```python
    self.conv_4layer = nn.Sequential(
        nn.Conv2d(1, n_chansl, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),    # (Batch_size, n_chansl, 32, 32)->(B, C, H, W)

        nn.Conv2d(n_chansl, n_chansl*2, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl*2, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),    # (Batch_size, n_chansl*2, 16, 16)->(B, C, H, W)

        nn.Conv2d(n_chansl*2, n_chansl*4, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl*4, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),    # (Batch_size, n_chansl*4, 8, 8)->(B, C, H, W)

        nn.Conv2d(n_chansl*4, n_chansl*2, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl*2, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),    # (Batch_size, n_chansl*2, 4, 4)->(B, C, H, W)
    )
    self.fc_4layer = nn.Sequential(
        nn.Linear(n_chansl*2 * 4 * 4, 7),
    )
    ```

* 4-Level New is similar to previous version but double the channel size and always increasing. Then the result is not bad.
    ```python=
    self.conv_4layer = nn.Sequential(
        nn.Conv2d(1, n_chansl, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, n_chansl, 32, 32)->(B, C, H, W)

        nn.Conv2d(n_chansl, n_chansl*4, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl*4, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, n_chansl*4, 16, 16)->(B, C, H, W)

        nn.Conv2d(n_chansl*4, n_chansl*8, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl*8, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, n_chansl*8, 8, 8)->(B, C, H, W)

        nn.Conv2d(n_chansl*8, n_chansl*16, kernel_size=3, padding=1),
        nn.BatchNorm2d(n_chansl*16, eps=1e-05, affine=True),
        nn.LeakyReLU(negative_slope=0.05),
        nn.MaxPool2d((2, 2)),   # (Batch_size, n_chansl*16, 4, 4)->(B, C, H, W)
    )
    self.fc_4layer = nn.Sequential(
        nn.Linear(n_chansl*16 * 4 * 4, n_chansl*4 * 4 * 4),
        nn.Linear(n_chansl*4 * 4 * 4, 7)
    )
    ```


## Other Technique I used
* Early-Stopping
* Normalization: you can find the code that I compute the mean and standard deviation in `temp.py`.
* Data Augmentation
    * [Ver. 1] including RandomChoice from RandomHorizontalFlip, ColorJitter, RandomRotation and used CenterCrop to a specific size then used Pad to original size. This version is for **self-defined model**.
* Plot Confusion Matrix: must command `--plot_cm` in cmd
* Visualize Data Distribution by bar chart.

## Environment
```
conda install -c conda-forge argparse
conda install -c conda-forge tqdm
conda install -c conda-forge wandb
conda install -c anaconda more-itertools
conda install -c anaconda scikit-learn
conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge
```

## Run
* We supply some self-defined arguments such as basic `--epochs`, `--lr`, `--batch_size`, `--val_batch_size`, `--checkpoint`.
* And we also supply advanced setting like `--optimizer` including Adam and SGD, `--weight_d`, `--momentum`, `--gamma` and `--step` for learning rate scheduler, `--channel_num` for model channel numbers.
* Other tools such as `--wandb` which is a visualized and logging tool to record every things you want to update on [website](https://wandb.ai/), and `--plot_cm` to visualize validation result.
* For training with using data augmentation, scheduler and early stopping
    ```
    python MLHW.py  --epoch 600 --lr 0.001 --gamma 0.2 --step 40 --batch_size 256 --early_stop --data_aug -c ./epoch490_acc0.6243.pth
    ```
* For testing
    ```
    python MLHW.py --mode test -c ./epoch115_acc0.6318.pth
    ```

## Result
* Whole result with the configuration and technique above is [here](https://wandb.ai/bernie6401/MLHW2/overview?workspace=user-bernie6401).

### Early-Stopping
As you can see below, if I use early stopping technique, it'll break the training loop when overfitting. The orange line is what I set early stopping with threshold 5. That is, if the model loss rise up 5 times consequently, then stop training. The other one doesn't set early stopping and you can see it'll complete the training loop even overfitting occur. ![early_stop_train_acc](https://imgur.com/FrJElIp.png)![early_stop_train_loss](https://imgur.com/GlFBuhu.png)![early_stop_val_acc](https://imgur.com/xmTOt04.png)![early_stop_val_loss](https://imgur.com/9M8Wdwa.png)

### Data Augmentation
As you can see below, if I use data augmentation, it can conquer overfitting. The other configurations are the same and the breakpoint of orange line is because of early-stopping. I set data augmentation technique on purple one and the others didn't.
```python
transform_set = [
    transforms.RandomHorizontalFlip(p=0.5),   # Horizontal Flip in random
    transforms.ColorJitter(brightness=(0, 5), contrast=(0, 5), saturation=(0, 5), hue=(-0.1, 0.1)),  # Adjust image brightness, contrast, satuation and hue in random
    transforms.RandomRotation(30, center=(0, 0), expand=False),]   # expand only for center rotation

transform_aug = transforms.Compose([
    transforms.RandomChoice(transform_set),
    transforms.Resize(224)])
```
I choose RandomChoice to choose transform_set including RandomHorizontalFlip, ColorJitter, RandomRotation. ColorJitter will adjust the brightness, contrast, saturation and hue of the input image randomly. So, it can increase the diversity of training dataset properly. Though, lecture TA is not very suggestive to use RandomVerticalFlip skill on training image, because it'll transform the image that no human can recognize it. So, I use RandomHorizontalFlip instead.
![data_aug_train_acc](https://imgur.com/PL2Ykmq.png)![data_aug_train_loss](https://imgur.com/V6NxzMD.png)![data_aug_val_acc](https://imgur.com/aOtnNaf.png)![data_aug_val_loss](https://imgur.com/sewt3kI.png)

### Confusion Matrix
As you can see the confusion matrix below. The second class(emotion Disgust) is the worst result of the classification and the Happy class is the best. Also, the Fear class is not good enough. I think the main reason is data imbalance that shown below of second one. The prior of these two classes are 0.0155 and 0.1443 respectively. Under this circumstance, the model can't learn this class by enough images properly. And the bad result of Fear class. I think it's just not learn very well with bad model structure and bad configuration.
![confusion_matrix](https://imgur.com/JXcbEKx.png)
![data_distribution](https://imgur.com/SEHelPa.png)

### Data Distribution
The result of data distribution is shown above. The prior probability of the highest probability is $6525/25887=0.252$. If not targeting a specific category and just choose the Happy class, it would be worse than normal classification progress.