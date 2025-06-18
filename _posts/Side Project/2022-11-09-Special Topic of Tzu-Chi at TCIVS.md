---
title: Special Topic of Tzu-Chi at TCIVS
tags: [Side Project, Special Topic, TCIVS]

category: "Side Project"
---

# Special Topic of Tzu-Chi at TCIVS
<!-- more -->
###### tags: `TCIVS` `Side Project` `Special Topic`
:::spoiler
[TOC]
:::

## Purpose of this file
+ I just want to write up some problems while I set up the environment and hardware of this project

## Hardware info.
Spec.|Raspberry Pi 3 Model B+
:-------------------------:|:---:
CPU|ARM Cortex-A53 1.4GHz
RAM|1GB SRAM
Wi-Fi|2.4GHz and 5GHz
Ethernet speed|300Mbps
Bluetooth|4..2

## Set up sequence(Ideal)
* Install OS to Raspberry pi
	> You can just check this [page](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#4-boot-ubuntu-server)
	```
	$  vim /etc/netplan/50-cloud-init.yaml
	(add the line at the end, and the indentation is very important)
	wifis:
		wlan0:
		dhcp4: true
		optional: true
		access-points:
			"home network":
				password: "123456789"
	$  sudo reboot
* Install Anaconda in a correct version
	```
	$  cd ~
	$  curl -O https://repo.anaconda.com/archive/Anaconda3-2021.04-Linux-aarch64.sh
	$  bash Anaconda3-2021.04-Linux-aarch64.sh
	$  vim ~/.bashrc
	(add "export PATH='/home/ubuntu/anaconda3/bin:$PATH' at the end")
	$  source ~/.bashrc
	$  sudo reboot
* Install the Library you need
	```
	$  conda install -c anaconda scipy
	$  conda install -c conda-forge/label/broken tensorflow
	$  pip install opencv-contrib-python
	$  conda install -c anaconda numpy
	$  conda install -c anaconda requests
	$  conda install -c conda-forge keras
	
	$  conda install -c conda-forge imutils
	$  conda install -c conda-forge face_recognition
	$  conda install -c conda-forge dlib
* Run the python file you mount from the external disk, e.g. flash disk

## Problem
1. There're 3 different OSs can choose including **Raspberry Pi OS**, **Ubuntu server**, **Ubuntu desktop**
   + First of all is Raspberry Pi OS(32-bits), because it's an official recommendation, I install it first. But as I show the spec. above, the CPU is 64-bits and you must run **Raspberry Pi Imager** before you install OS to Raspberry Pi. Then your OS architecture will be not compatible with Anaconda though it has a 32-bits  version as well. You'll get the error.
   + The second one is Ubuntu-Desktop (22.04 or 20.04). It'll get frozen all the time because of the small SRAM with 1GB
   + The third one seems quite a good choice as an OS. It'll not get frozen because it's just a simple CLI system and it also has an aarch64 version. Then the statements below are the problems you'll encounter.

2. If I install Anaconda correctly, I'll encounter a problem that **conda create** instruction can not be used. You'll get an error message like this: **Illegal instruction(core dumped)**. 

	* [Solution](https://github.com/conda/conda/issues/10723) by installing Miniconda.

	+ But...miniconda still has another problem: version conflict with the library. So, this is not the best solution as well.

	+ For more information on this solution: though I can use **conda create** instruction, I can not install python with the 3.6 version. The reason that I must install this version is for the library I want to install later. If I don't install version 3.6, I can't install **imutils**, **face_recognition**, and **dlib** at the same time. The other library list above including scipy, TensorFlow, NumPy, and so on will install successfully in versions 3.6 to 3.9.

	+ Briefly speaking, because of my OS architecture, I can't install these 3 libraries by the statement that anaconda official supplied. I can install the package available on **noarch** or **aarch64** platform only.
	+ For imutils, like the image below(img1)
	```$  conda install --channel https://conda.anaconda.org/gilbertfrancoins imutils```
	+ For face_recognition, like the image below(img2)
	```$  conda install --channel https://conda.anaconda.org/conda-forge face_recognition```
	- You can check the error on this [page](https://blog.csdn.net/ksws0292756/article/details/79192268), then there is another problem I encounter is I can not use **anaconda** instruction to search the library package. So, I use my laptop(a normal win10 system) to search.
	* BTW, you can not use the x86 version, because it'll crash while the installation
***

![img1](/assets/posts/TCIVS_Special_Topic/error_1.png)

***

![img1](/assets/posts/TCIVS_Special_Topic/error_2.png)

***

3. I also followed [this article](https://blog.csdn.net/YMWM_/article/details/107022521) and tried to address this problem. Though it can use anaconda instruction smoothly, it still has some problems to solve(I forgot the problem, QAQ)

4. You might be wondering why I don't use pip instruction. Because you'll get an error message like this: **Illegal instruction(core dumped)**.
5. Other problems must address
	* If you install OS and Anaconda successfully.

	```
	$  python
	$  import numpy
	
	(error message)
	$  Illegal instruction(core dumped)
	```

## Conclusion for the above
> The solutions above are not suitable for this project

## New Solution
This solution seems fine so far, so I write it up as below
1. First, we can install **Raspberry Pi OS (64-bit)** by Raspberry Pi Imager. It has a desktop version and is still compatible with the hardware.
2. Second, install Miniconda by following the instruction on this [page](https://blog.csdn.net/mtl1994/article/details/122240677)(PS version is Miniconda3-py37_4.9.2-Linux-aarch64.sh)
3. Third, create a new environment in Anaconda without python. You should install python independently(v3.6).
    ```
    $ conda install -c moussi python
    $ conda install -c akode face_recognition_models
    $ conda install -c gilbertfrancois imutils
    $ conda install -c conda-forge fortran_stdlib
    $ conda install -c jetson-tx2 scipy
    $ conda install -c intel tensorflow-base
	$ conda install -c anaconda numpy
	$ conda install -c conda-forge/label/cf202003 requests
	$ conda install -c conda-forge keras
	$ pip install opencv-contrib-python
	```
	These libraries can be installed with python=3.6, but TensorFlow.
	Please go to this [page](https://anaconda.org) and search the library you want to install(set the platform filter as noarch or Linux-aarch64)

## Practical Solution
In order to avoid not being able to do it in the end, we change another solution with higher success rate - we used Arduino instead. You can check the code in [here](https://github.com/bernie6401/TCIVS_Special_Topic/tree/master/serial_read). And our os platform is my x86 laptop, we don't have the software compatible problem.