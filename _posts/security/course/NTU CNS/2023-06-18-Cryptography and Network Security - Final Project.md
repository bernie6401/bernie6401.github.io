---
title: Cryptography and Network Security - Final Project
tags: [Cryptography, NTU]

category: "Security/Course/NTU CNS"
---

# Cryptography and Network Security - Final Project

## Threshold HE Description
With a designed scheme in place for threshold homomorphic encryption, private keys are divided into various shares among participating individuals who then work together to collaborate on computations without revealing plaintext material. 

Decryption requires collaboration from at least the minimum requirement, e.g. $(t,n)$ means there're $n$ participate parties but need at least $t$ parties' granting to decrypt the secret just like secret sharing scheme proposed by Shamir. Threshold homomorphic's primary objective is secure computation involving confidential information with lesser exposure or accessibility risks for single individuals - due to a shared understanding by several stakeholders. 

This approach can prevent possible failures or compromise issues quickly becoming apparent within an organization.

Threshold homomorphic encryption has various applications, particularly in secure multi-party computation scenarios. It enables collaborative data analysis and computations while maintaining privacy. Additionally, it can be used to securely process sensitive data in the cloud, where the data remains encrypted throughout the computation, minimizing the exposure of private information.

It's important to note that while threshold homomorphic encryption offers increased security and privacy, it can also introduce additional complexity and overhead compared to traditional homomorphic encryption schemes. The distribution of shares, coordination among parties, and the threshold determination are some of the challenges that need to be addressed when implementing threshold homomorphic encryption.

Moreover, they proposed (t, n)-threshold FHE is decentralized if all the parties have the same level of information and play the same role in the `KeyGen` and `Dec` protocols.

## Pros & Cons
### Pros
* Decentralized: This paper also proposed a scheme that can achieve decentralized property can improve the security of a system. Moreover, decentralized systems are more reliable, resilient and enhanced transparency as well.

* Security: Threshold homomorphic encryption provides a higher level of security and privacy compared to traditional homomorphic encryption schemes. By distributing the encryption key across multiple parties, it performs computations on encrypted data without revealing the underlying data itself, and also reduces the risk of a single point of failure or compromise. This makes it more resistant to attacks and enhances overall security and can enables secure collaboration on sensitive information without exposing it to all parties involved.

* Distributed computation: With threshold homomorphic encryption, computations can be distributed among multiple parties. Each party can perform part of the computation on their own encrypted data, and the results can be combined without the need to decrypt the data. This allows for efficient parallel processing and enables secure multi-party computations.

* Flexibility: Threshold homomorphic encryption supports a wide range of operations, including addition, multiplication, and more complex computations like sorting and searching. This flexibility makes it suitable for various applications that require privacy-preserving computations.

### Cons
* Complexity: Implementing threshold homomorphic encryption is more complex than traditional homomorphic encryption schemes. It requires careful coordination and secure communication among the participating parties. The additional complexity can make the implementation more challenging and may require specialized knowledge.

* Key management: Threshold homomorphic encryption requires secure key management, as the encryption key is distributed among multiple parties. Ensuring the secure generation, storage, and distribution of the key shares can be challenging and requires robust protocols and mechanisms to maintain security.

* Limited functionality: While threshold homomorphic encryption supports a wide range of operations, there are still some limitations compared to fully homomorphic encryption (FHE). Certain operations, such as division or non-polynomial functions, may not be directly supported by threshold homomorphic encryption schemes.