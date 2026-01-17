---
title: NTU Machine Learning Final Project Proposal Notes
tags: [NTU_ML, Machine Learning, NTU]

category: "Security｜Course｜NTU ML"
date: 2022-12-28
---

# NTU Machine Learning Final Project Proposal Notes
<!-- more -->
###### tags: `NTU_ML` `Machine Learning`

## Deep6mAPred: A CNN and Bi-LSTM-based deep learning method for predicting DNA N6-methyladenosine sites across plant species

### Introduction & Motivation
* DNA methylation alters activities of DNA segments without changing the sequence, which thus yields a wide variety of roles in the cellular processes across organisms or tissues
* DNA methylation is widely distributed both in prokaryote and in eukaryote, but the proportion of methylated residues differs greatly with species
* DNA methylation is essential for normal development
* DNA methylation is increasingly attracting attentions from biologists

### Related works
* Even Luo et al.[41] - proposed the DNA 6mA as a new epigenetic mark in eukaryotes
* 2 major ways to detect DNA 6mA sites: 
    * Wet experiments
        * mass spectrometry / methylation-specific polymerase chain reaction / single-molecule real-time sequencing
        * Times consuming / expensive / labor-intensive
    * Dry experiments - computational methods
        * learning a classifier: feature-based and the deep learning-based methods
    * Pian et al.[45] - employed transition probability between adjacent nucleotides to construct a Markov model to identify 6mA site
    * Chen et al.[47] – `SVM` based method for rice 6mA prediction
    * The i6mA-DNCP[51] - improve the representation with optimized dinucleotide-based features
    * iDNA6mA-Rice[1] – multiple encoding schemes as representations / random forest
    * 6mA-RicePred[53] – fused multiple features including Markov feature for rice 6mA prediction
    * csDMA[54] – three representations and explore the best one
    * 6mA-Finder[55] – seven sequence-based coding schemes
    * iIM-CNN - employed CNN
    * iDNA6mA - deep learning-based method / CNN
    * Huang et al. [72] - LSTM-based method called 6mA-Pred
    * Le et al. [73] - employed transformer-based BERT
    * DNA6mA-MINT [74] - stacked CNN and LSTM simply

* Appendix
    * [41]G.Z. Luo, M.A. Blanco, E.L. Greer, C. He, Y. Shi, DNA N(6)-methyladenine: a new epigenetic mark in eukaryotes? Nat. Rev. Mol. Cell Biol. 16 (12) (2015) 705–710, https://doi.org/10.1038/nrm4076.
    * [45] C. Pian, G. Zhang, F. Li, X. Fan, MM-6mAPred: identifying DNA N6- methyladenine sites based on Markov model, Bioinformatics 36 (2) (2020) 388–392, https://doi.org/10.1093/bioinformatics/btz556.
    * [47] W. Chen, H. Lv, F. Nie, H. Lin, i6mA-Pred: identifying DNA N6-methyladenine sites in the rice genome, Bioinformatics 35 (16) (2019) 2796–2800, https://doi.org/10.1093/bioinformatics/btz015.
    * [51] L. Kong, L. Zhang, i6mA-DNCP: computational identification of DNA N6- methyladenine sites in the rice genome using optimized dinucleotide-based features, Genes 10 (10) (2019) 828, https://doi.org/10.3390/genes10100828.
    * [1] H. Lv, F.Y. Dao, Z.X. Guan, D. Zhang, J.X. Tan, Y. Zhang, W. Chen, H. Lin, iDNA6mA-Rice: a computational tool for detecting N6-methyladenine sites in rice, Front. Genet. 10 (2019) 793, https://doi.org/10.3389/fgene.2019.00793.
    * [53] Q. Huang, J. Zhang, L. Wei, F. Guo, Q. Zou, 6mA-RicePred: a method for identifying DNA N6-methyladenine sites in the rice genome based on feature fusion, Front. Plant Sci. 11 (2020) 4, https://doi.org/10.3389/fpls.2020.00004.
    * [54] Z. Liu, W. Dong, W. Jiang, Z. He, csDMA: an improved bioinformatics tool for identifying DNA 6 mA modifications via Chou’s 5-step rule, Sci. Rep. 9 (1) (2019) 1–9, https://doi.org/10.1038/s41598-019-49430-4.
    * [55] H. Xu, R. Hu, P. Jia, Z. Zhao, 6mA-Finder: a novel online tool for predicting DNA N6-methyladenine sites in genomes, Bioinformatics 36 (10) (2020) 3257–3259, https://doi.org/10.1093/bioinformatics/btaa113.
    * [72] Q. Huang, W. Zhou, F. Guo, L. Xu, L. Zhang, 6mA-Pred: identifying DNA N6- methyladenine sites based on deep learning, PeerJ 9 (2021), e10813, https://doi.org/10.7717/peerj.10813.
    * [73] N.Q.K. Le, Q.T. Ho, Deep transformers and convolutional neural network in identifying DNA N6-methyladenine sites in cross-species genomes, Methods (2021), https://doi.org/10.1016/j.ymeth.2021.12.004.
    * [74] M.U. Rehman, K.T. Chong, DNA6mA-MINT: DNA-6mA Modification Identification Neural Tool, Genes 11 (8) (2020) 898, https://doi.org/10.3390/genes11080898.


### Background
* What is methylation?
DNA methylation alters activities of DNA segments without changing the sequence, which thus yields a wide variety of roles in the cellular processes across organisms or tissues. In addition, the DNA methylation appears essential for normal development.
* What is 6mA?
The 6mA refers to a biological process where the methyl group is attached to the 6-th nitrogen atom of adenine by the enzyme of DNA methyltransferase. The 6mA is a type of non-canonical DNA modification because it might occur in other nucleotide molecules including mRNA, tRNA, rRNA, small nuclear RNA (snRNA) as well as long non coding RNA
* Why is it important?
A large volume of evidence suggested that the DNA 6mA would play vital roles in many key biological processes.
The DNA 6mA participated in regulation of gene expression both in prokaryotes and in some eukaryotes, and was responsible for DNA repair as well as DNA replication.
The 6mA distinguished invading foreign DNAs from host DNA in prokaryotes, was closely associated with many disease including tumor in human genome, and was involved in regulation of drug resistance in triple negative breast cancer

### My Opinions
For this paper, my perspective is this is a little bit trivial to solve the problem. For simplicity speaking, they just change the stacking model structure to a sequence structure. In addition, the result of this paper is exaggerating.

### Comparison
* The result below is the experience on `6mA-rice-LV`(rice) dataset, and this paper method is `Deep6mAPred`. They used 5-fold cross validation on this data(`6mA-rice-LV`). In the original context, they said:
    > The `Deep6mAPred` reached better Sn than three baseline methods (`Deep6mA` , `SNNRice6mA-large` and `Deep6mAPred`), and achieved competitive SP, ACC and MCC in contrast with the `Deep6mA`, which completely outperformed the `SNNRice6mA-large` and MM-6mAPred.

    However, the fun fact is the performance of $Sp, ACC, MCC, AUC$ is not good enough in this dataset. 

    ![](https://imgur.com/vccb3m0.png)
* The result below is for `6mA-rice-chen` dataset. Compared with `Deep6mA`, `Deep6mAPred` increased $Sn$ by 0.1572, ACC by 0.0750, MCC by 0.1436, and AUC of ROC curve by 0.0237, completely superior to the other two methods. The $Sp$ of `Deep6mAPred` is slightly lower than that of `Deep6mA`, but much higher than that of the other two methods.
![](https://imgur.com/ixsSXSK.png)
This result is quite distinguished that can show how special their model is under this another rice data.
* This is ROC curves and PR curves result on `6mA-Fuse-R`(Rosa chinensis) and `6mA-Fuse-F`(Fragaria vesca, a kind of wild strawberry) respectively. In order to show how robust on their model, they try to test different species such as rose and wild strawberry without training, and the result is quite significant that almost similar to rice data.
![](https://imgur.com/eODMhQm.png)
* This is a self-created table that I wanna show the AUC of two curves with different species. 
The original context said:
    > As for the 6mA-Fuse-R, the `Deep6mAPred` outperformed three baseline methods in terms of the AUCs of ROC curves, while in terms of the AUCs of the PR curves it was equivalent to the `Deep6mA` but superior to the `SNNRice6mA-large` and `MM-6mAPred` a bit
    
    Follow the description above, we can know that the result of `6mA-Fuse-R` is better than three baseline methods but without any table or figure to prove that and this is not rigourous enough for this information.
    ![](https://imgur.com/UVaJ7sL.png)
* They also do some ablation experiment to prove that the attention mechanism they choose is quite valid and useful in this project.
We can see that in each experiment of different species, with attention mechanism is generally better than the experiment that without attention.
![](https://imgur.com/3Sj3Tfz.png)

### Other Issue
* Why can wild rose and rice use the same architecture or we can ask how to process input data so that they can be applicable at the same model structure.
* There is no extra explanation for the selected attention mechanism method.


### Conclusion
* The 6mA is a key mechanism of regulation in the cellular processes. 
* We presented a CNN and LSTM-based method (Deep6mAPred)  with paralleling manner
* They also used attention mechanism to improve their model and it's really helpful proved by ablation experiment.
* In addition, they developed a user-friendly webserver to automatically detect 6mA sites
* Deep6mAPred can also detect other plants

### References


## Ensemble Learning of Convolutional Neural Network, Support Vector Machine, and Best Linear Unbiased Predictor for Brain Age Prediction: ARAMIS Contribution to the Predictive Analytics Competition 2019 Challenge

### Introduction & Motivation
* Chronological age is an important risk factor for many conditions such as neurological disorders (e.g., Alzheimer’s and Parkinson’s), chronic (including cardiovascular) disorders, cancer, or stroke, to name a few.
* However, it is an imperfect predictor of disease risk or of healthy individuals’ functional capability
* Brain age (and PAD(predicted age difference)) trained on healthy participants may be applied to case-control samples where they have been shown to be non-specific predictors of disease status: Alzheimer’s disease and conversion[8-10], schizophrenia[11], alcohol dependence[12], cognitive impairment[13], or functional abilities[6, 14]
* However, chronological age cannot explain everything, brain age correlates with disease, mortality, and function beyond what chronological age can explain

### Related works
[2]Cole J, Marioni RE, Harris SE, Deary IJ. Brain age and other bodily “ages”: implications for neuropsychiatry. Mol Psychiatr. (2019) 24:266–81. doi: 10.1038/s41380-018-0098-1 
[3]Horvath S, Raj K. DNA methylation-based biomarkers and the epigenetic clock theory of ageing. Nat Rev Genet. (2018) 19:371–84. doi: 10.1038/s41576-018-0004-3 
[4]Sajedi H, Pardakhti N. Age prediction based on brain MRI image: a survey. J Med Syst. (2019) 43:279. doi: 10.1007/s10916-019-1401-7 
[5]Baker GT, Sprott RL. Biomarkers of aging. Exp Gerontol. (1988) 23:223–39. doi: 10.1016/0531-5565(88)90025-3 
[6]Cole J, Ritchie SJ, Bastin ME, Valdés Hernández MC, Muñoz Maniega S, Royle N, et al. Brain age predicts mortality. Mol Psychiatr. (2018) 23:1385–92. doi: 10.1038/mp.2017.62
[8]Franke K, Gaser C. Longitudinal changes in individual brainAGE in healthy aging, mild cognitive impairment, alzheimer’s disease. GeroPsych. (2012) 25:235–45. doi: 10.1024/1662-9647/a000074
[9]Gaser C, Franke K, Klöppel S, Koutsouleris N, Sauer H. BrainAGE in mild cognitive impaired patients: predicting the conversion to alzheimer’s disease. PLoS ONE. (2013) 8:67346. doi: 10.1371/journal.pone.0067346 
[10]Wang J, Knol MJ, Tiulpin A, Dubost F, Bruijne M, de, et al. Gray matter age prediction as a biomarker for risk of dementia. Proc Natl Acad Sci USA. (2019) 116:21213–8. doi: 10.1073/pnas.1902376116 
[11]Koutsouleris N, Davatzikos C, Borgwardt S, Gaser C, Bottlender R, Frodl T, et al. Accelerated brain aging in schizophrenia and beyond: a neuroanatomical marker of psychiatric disorders. Schizophrenia Bull. (2014) 40:1140–53. doi: 10.1093/schbul/sbt142
[12]Guggenmos M, Schmack K, Sekutowicz M, Garbusow M, Sebold M, Sommer C, et al. Quantitative neurobiological evidence for accelerated brain aging in alcohol dependence. Transl Psychiatr. (2017) 7:1279. doi: 10.1038/s41398-017-0037-y
[13]Liem F, Varoquaux G, Kynast J, Beyer F, Kharabian Masouleh S, Huntenburg JM, et al. Predicting brain-age from multimodal imaging data captures cognitive impairment. NeuroImage. (2017) 148:179–88. doi: 10.1016/j.neuroimage.2016.11.005
[14]Beheshti I, Maikusa N, Matsuda H. The association between “Brain- Age Score” (BAS) and traditional neuropsychological screening tools in Alzheimer’s disease. Brain Behav. (2018) 8:e01020. doi: 10.1002/brb3.1020

### Background
* Latest research focus on telomere length, methylation site, brain structure, and function[2-6]
* In particular, brain age estimation from MRI images is a rapidly expanding field of research with several hundred publications to date

### My Opinions
The main opinion to this paper is that it's report of the competition they attended. And listed as clear as possible what problems they encountered, what techniques they used etc.

### Comparison
* The * symbol represents a significant reduction in $MAE$ by Ensemble Learning compared to Inception alone ($p\ value < 0.05$)
    * For the objective of minimize MAE, the way of deep learning is better than `BLUP` and `SVM` ($pvalue\ of\ paired\ t-test<3.1e-4$)
    * There was no significant difference in the performance of the deep learning algorithms ($p > 0.027$)
    * In contrast, Ensemble Learning's $MAE=3.46$, there is a significant difference (p=1.3e-4)
    * Taking challenge 2 as an example, the author uses median and mean absolute deviation per site to rescale the prediction. The results show that $MAE$ will increase by one year compared to the original one, but will reduce the bias. The same that ensemble learning has a significant improvement compared to Inception($p=0.010$).
![](https://imgur.com/5jR4hWo.png)

* They also tried to evaluate whether their conclusions depend on the train/test split used in the previous section by performing a 5-fold cross-validation experiment.
    * Within each fold, they found a nominally significant difference in MAE between `BLUP`/`SVM` and `ResNet` ($p < 5.5E−3$)
    * In each fold, the composite age score using linear regression outperformed `Inception V1`'s predictions ($p < 0.0022$). For folds 2 and 3, ensemble learning via random trees significantly outperforms `Inception V1` alone ($p=4.0E−3 and 3.4E−4$)
    * Note that the $MAE$ obtained using Random Forest is very close to the $MAE$ obtained by taking the mean or median score for each person. We cannot conclude that there is a significant difference between **linear model combinations** and **random forests**.
![](https://imgur.com/zyIaGAd.png)
* The low performance of `BLUP`/`SVM` shown above compared to deep learning algorithms motivated the authors to test whether it could be attributed to the input data or the algorithm itself. Therefore, the author retrains `BLUP` and `SVM` <font color="FF0000">(trained on gray matter maps)</font>
    * † Symbols represent: the algorithm trained with gray matter map is significantly **better than** the algorithm trained with surface-based vertices ($p < 0.05/15$).
    * The * symbol indicates: the performance of the algorithm trained on the gray matter image is significantly **lower than** that of `Inception V1` ($p < 0.05/15$)
    * Despite the reduction in MAE, `BLUP-mean` and `SVM` trained on gray matter still performed <font color="FF0000">**worse than**</font> `Inception V1` ($p < 0.0033$), although the difference between `Inception V1` and `BLUP-quantile` became not significant.
![](https://imgur.com/gO86vVb.png)
* The participant is older, the prediction error is larger. → Therefore, the predictor will tends to underestimate the age of older participants and overestimate the age of younger participants.
We did not observe significant associations of prediction errors with gender or location
![](https://imgur.com/a3ugXLy.png)

### Other Issue
* They didn't explain why they used two `6-Layers CNN` to combine and the effect in detailed.
* They also didn't explain the gray/white matter map difference and the properties of these maps in detailed.


### Conclusion
* Proposed an ensemble learning algorithm of 7 different age predictions from T1w MRI images 
* Ranked third in PAC2019
* Ranking of prediction accuracy may be highly dependent on the metric chosen as well as on the test data
* Evaluated the effect on performance of algorithm choice, ensemble learning methods, feature input/data processing, number and type of scores in ensemble learning, and covariates such as age, sex, and site

### References


## Machine learning workflows to estimate class probabilities for precision cancer diagnostics on DNA methylation microarray data

### Introduction & Motivation
* DNA methylation data-based precision cancer diagnostics
* Application for class probability (CP): Stratified Medicine
* Standards for choosing statistical methods with regard to well-calibrated probability estimates for these typically highly multiclass classification tasks are still lacking
* We compared these workflows on a recently published brain tumor 450k DNA methylation cohort of 2,801 samples with 91 diagnostic categories using a 5 5-fold nested cross validation scheme and demonstrated their generalizability on external data from The Cancer Genome Atlas
* Purpose of this study: 
    * to perform a benchmark analysis to support the choice for optimal DNA methylation microarray data analysis through extensive comparisons of well-established ML classifiers and their combination with post-processing algorithms
    * such as `Platt Scaling` and ridge-penalized `multinomial L`(MR)
* `ELNET` was the top stand-alone classifier
* The best overall two-stage workflow was MR-calibrated `SVM` with linear kernels closely followed by ridge-calibrated tuned RF
* MR was the most effective regardless of the primary classifier
* The number of features (p\) vastly outnumbers the sample size (n)
* Therefore, a more reasonable require predictions ment is that the estimated CP function provides well-calibrated(e.g. `Platt scaling`)
* Multiclass classification problems → unbalanced classification problems

### Related works
* High multiclass & unbalanced classification problem
    [7]Baek, S., Tsai, C.-A. & Chen, J. J. Development of biomarker classifiers from high-dimensional data. Brief.Bioinform. 10, 537–546 (2009).
    [8]Dupuy, A. & Simon, R. M. Critical review of published microarray studies for cancer outcome andguidelines on statistical analysis and reporting. J. Natl Cancer Inst. 99,147–157 (2007).
    [9]. Hastie, T., Tibshirani, R. & Friedman, J. The Elements of Statistical Learning: Data Mining, Inference andPrediction 2nd edn (Springer, New York, NY, 2009).
    [10]. Lee, J. W., Lee, J. B., Park, M. & Song, S. H. An extensive comparison of recent classification tools applied tomicroarray data. Comput. Stat. Data Anal. 48, 869–885 (2005).
    [11]. Simon, R. Roadmap for developing and validating therapeutically relevant genomic classifiers. J. Clin. Oncol.23, 7332–7341 (2005).
* DNA methylation application
    [1]. Capper, D. et al. DNA methylation-based classification of central nervous system tumours. Nature 555,469–474 (2018).
    [4]. Rodríguez-Paredes, M. & Esteller, M. Cancer epigenetics reaches mainstream oncology. Nat. Med. 17,330–339 (2011).
    [13]. Fernandez, A. F. et al. A DNA methylation fingerprint of 1628 human samples. Genome Res. 22, 407–419 (2012).
    [14]. Wiestler, B. et al. Assessing CpG island methylator phenotype, 1p/19q codeletion, and MGMT promotermethylation from epigenome-wide data in the biomarker cohort of the NOA-04 trial. Neuro Oncol. 16,1630–1638 (2014).
* The number of features (p) vastly outnumbers the sample size (n)
    [9]. Hastie, T., Tibshirani, R. & Friedman, J. The Elements of Statistical Learning: Data Mining, Inference and Prediction 2nd edn (Springer, New York, NY, 2009).
    [20]. Simon, R. Class probability estimation for medical studies. Biom. J. 56, 597–600 (2014).

### Background
* The problem of stratified medicine
    1. Unbiased classification problem (there are fewer patients in some categories, of course there will be inequality problems)
    2. Usually medical diagnosis is to classify patients in several categories of interest, but real medical behavior should be able to achieve multi-category diagnosis (50 or more than 100 categories)

### My Opinions
This paper is just like a `Readme` file that wanna teach someone how to use their tool, each technique they used, each problem they encountered, and also which programming package they used etc. as clear as possible. Although the paper should be as clear as possible, but too much unnecessary information is really a waste of time and annoying.

### Comparison
* **Random Forest(RFs)**
    * Vanilla RF(vRF)
        * The ME of vRF was 4.8%, the AUC was 99.9%, and the corresponding BS and LL were 0.32 and 0.78, respectively
        * Platt scaling with LR and `FLR` improves BS and LL by a factor of 2-4, furthermore, `FLR` is better than `LR`
        * MR slightly outperformed Platt's two variants and achieved very low 10th and 9th overall BS (0.073) and LL (0.155) metrics respectively
    * tuned RF(tRF)
        * RF tuned for ME (`tRFME`) showed 10th overall error rate (3.5%) and 4th AUC (99.9%), while it had relatively high BS (0.35) and LL (0.86) similar to `vRF`
        * Both `tRFBS` and `tRFLL` have higher error rates, about 5.5%
        * After calibration with <font color="FF0000">**MR**</font>, almost all versions of `tRF` get the biggest performance improvement

    ![](https://imgur.com/MgjyT0T.png)
* **ELNET**
    * It used 1,000 most variable CpG probes
    * ME ranked 8th, AUC ranked 5th
    * ME (2.7%), BS (0.048) and LL (0.109) and negligibly low AUC (99.9 %)

    ![](https://imgur.com/A2RRIAp.png)
* **SVM**
    * More effective ME = 2.1% (lowest overall) with Platt scaling with Firth regression
    * While simple LR can be more effective to improve BS (second) and LL (fourth) by 8-9 times respectively
    * MR (<font color="FF0000">**`SVM-LK+MR`**</font>) achieves the most comprehensive improvement across all metrics. It reduced BS by a factor of 9.5 and LL by a factor of 11.5, resulting in the second lowest ME (2.1%) and AUC (99.9%), lowest BS (0.039) and lowest LL (0.085)
    
    ![](https://imgur.com/CaeII1m.png)
* **Boost Tree**
    * Boosted model using ME as evaluation metric outperforms model using LL
    * Overall ME of 5.1% and AUC of 99.9%, with the second lowest BS (0.15) and LL (0.43) among the base ML classifiers studied

    ![](https://imgur.com/XXdGN2p.png)

### Other Issue

### Conclusion
* We performed extensive comparative analyses of four well-established classifier algorithms including RF, `ELNET`, `SVM` and boosted ensemble trees in combination with `Platt scaling` and `multinomial ridge regression`
* The best overall two-stage workflow was MR-calibrated `SVM-LK`, and it generated the best overall BS, LL and AUC metrics.
* For calibration, `multinomial ridge-penalized regression` was the most effective regardless of the primary classifier

### References