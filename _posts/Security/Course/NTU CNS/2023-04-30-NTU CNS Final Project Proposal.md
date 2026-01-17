---
title: NTU CNS Final Project Proposal
tags: [NTUCNS, NTU]

category: "Security｜Course｜NTU CNS"
date: 2023-04-30
---

# NTU CNS Final Project Proposal
<!-- more -->
###### tags: `NTUCNS`

## Problem description / Research question(秉學)

### Terminology
Federated Learning is a decentralized machine learning method that enables training models without exposing data. Traditional machine learning methods require all data to be centralized in one location for training, but Federated Learning enables models to be trained on many distributed devices, such as smartphones, tablets, or embedded devices, with each device training its own local data. This greatly reduces data transmission and storage requirements and better protects user privacy.

---
Privacy Preserving is a method of designing and implementing computing systems aimed at protecting the privacy of data and personal information. It is typically a technique used in the exchange or processing of data to ensure the confidentiality, integrity, and availability of data.
Privacy preserving techniques can help ensure that data is protected and that sensitive information is not disclosed even during data sharing, analysis, or storage. For example, techniques such as data encryption, differential privacy, and multi-party computation can be used to protect data privacy, and these techniques have wide applications in data analysis and machine learning.


### Research Problem
In this paper, they proposed a method to prevent a malicious server as an attacker as their threat model. However, each client in the same group shared the same public/private key so that the attacker can pretend a benign user and exploit part of the packages.
So, our threat model is if the attacker is one of the user in a group, he can decrypt a part of the packages transferred in this group and the confidentiality property is gone.

## Related work (馮楷)
- FedML-HE:
    - Limitations:
      
- Decentralized Threshold HE:
The authors provided a $(t,n)$-theshold HE scheme based on CKKS HE scheme, where a center server is no longer needed for decryption. Instead, the decryption process can be done, when $t$ out of $n$ parties agree to decrypt.
    - Limitations:
    To ensure the joint key security, smudging errors are required which inevitably enlarge the entire parameter size, resulting in a huge computational overhead.
- Proxy Re-Encryption:
The scheme can re-encrypt ciphertext for multiple receivers at a time by generating the re-encryption key from private and other users' public identities, which meets the requirement of FL.
    - Limitations:
    This scheme relies on a trusted authority KGC(key generation center) for initialization. Moreover, it assumes that all participants in the federated learning system are honest and follow the protocol correctly. 

## Plan (智翔)
Our method would be mainly based on the general scheme proposed for the practical deployment of homomorphic-encryption-based federated learning [2]. Several security issues remain unsolved since the scheme aims to keep generality. We will apply two or more possible schemes to the general scheme to improve data security.

- Key management
In the general scheme, there exists only one pair of public/private keys. Once a client is compromised or is malicious, they can easily decrypt the gradient from another client and possibly reverse the gradient to the original data using the gradient inversion attack. To defend against this type of attack, we may not allow clients to share the same pair of public/private keys.
On the other hand, the key pair is published by a server. If the server is compromised or malicious, then gradients from clients can be decrypted. By the gradient inversion attack, local data can be reversed. Thus decentralization is important to any federated learning scheme.
The following are two latest solutions to the problems.
    - Proxy re-encryption [4]
    This method establishes a key management held by a trusted third party and allows all clients to use distinct key pairs. The first problem is solved, while decentralization is not fulfilled.
    - Threshold homomorphic encryption [3]
    This method establishes a decentralized scheme by using threshold cryptography. At the same time, a single client can not decrypt any gradient from another, which solves the first problem.

- Poisoning attack
Poisoning attack is still one severe threat to federated learning. A malicious or compromised client can upload a bad gradient to the server and reduce the accuracy of the training model [5]. We will discuss this attack and try to find a scheme to mitigate poisoning attacks.

- Comparison
We will compare the security and efficiency of each scheme. For the security part, we will introduce several threats and evaluate the security level of a scheme by checking if the scheme can defend against these threats.

## Timeline (馮楷)
5/8: Finish studying paper
5/15: Apply Decentralized Threshold HE on the FedML system
5/22: Apply Proxy Re-Encryption on the FedML system
5/29: Finish the report
6/5, 6/12: Oral Presentation

## Deliverables（歐華）
The final deliverable of this project will be a comprehensive analysis of the security vulnerabilities in the FedML-HE system, as well as enhancements through the addition of threshold homomorphic encryption and proxy re-encryption. These enhancements will be presented in a detailed report, as well as their potential benefits and limitations in a practical scenario. 


## Reference
* Privacy Preserving using Homomorphic Encryption
[Privacy-Preserving Deep Learning via Additively Homomorphic Encryption](https://eprint.iacr.org/2017/715.pdf)
[FedML-HE: An Efficient Homomorphic-Encryption-Based Privacy-Preserving Federated Learning System](https://paperswithcode.com/paper/fedml-he-an-efficient-homomorphic-encryption)
[How to Securely Collaborate on Data: Decentralized Threshold HE and Secure Key Update](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9223642&tag=1)
[ID-Based Multireceiver Homomorphic Proxy Re-Encryption in Federated Learning](https://dl.acm.org/doi/pdf/10.1145/3540199)
[Poisoning Attacks and Defenses in Federated Learning: A Survey](https://arxiv.org/pdf/2301.05795.pdf)