---
title: Cryptography and Network Security – Comparative Critique 1
tags: [NTUCNS, NTU]

category: "Security/Course/NTU CNS/Paper Critique"
---

# Cryptography and Network Security – Comparative Critique 1

[![hackmd-github-sync-badge](https://hackmd.io/zB9SPcdEQkaaEMKlOtSAQg/badge)](https://hackmd.io/zB9SPcdEQkaaEMKlOtSAQg)

## Reading Topic: Reflections on trusting distributed trust
## Reading Topic: Reflections on Trusting Trust
###### tags: `NTUCNS`
Name: 何秉學	Student ID: R11921A16

:::spoiler Background
[什麼是 Intel® SGX？](https://www.intel.com.tw/content/www/tw/zh/architecture-and-technology/software-guard-extensions.html)
> 提供以硬體為基礎的記憶體加密功能，可在記憶體內隔離特定的應用程式碼與資料。Intel® SGX 允許將使用者層級的程式碼配置於記憶體中的隱私區域，這稱為「指定位址空間」(enclave)，其設計是為了在較高權限層級的執行程序中受到保護
---
[What is firefox Telemetry](https://support.mozilla.org/zh-TW/kb/send-performance-data-improve-firefox)
> 這個功能對 Mozilla 工程師來說很有幫助，它可以幫助工程師了解 Firefox 實際的運作狀況。Telemetry 會傳送使用量及體驗的資訊給 Mozilla。當您使用 Firefox 時，Telemetry 就會測量與收集與個人隱私無關的資訊，例如記憶體消耗、反應時間和各種功能的使用頻率。這些資訊會每天例行傳送給 Mozilla 利用，讓 Firefox 越來越完善。
---
[Let's Encrypt & ISRG](https://letsencrypt.org/zh-tw/getting-started/)
> Let's Encrypt 是免費、自動化和開放的憑證頒發機構，由非營利組織網路安全研究小組 (Internet Security Research Group, ISRG) 營運。 
---
[What is IETF](https://blog.twnic.tw/2021/04/28/18303/)
> 網際網路工程任務組（Internet Engineering Task Force，IETF） 成立於1986年，主要任務為負責網路技術規範的研究和標準的制定。 其屬於開放性組織，任何人都可參與，參加對象多以個人為主而非代表公司或團體。
---
[What is HSM(Hardware Security Module)](https://www.ibm.com/docs/zh-tw/blockchain-platform/2.5.1?topic=reference-glossary#glossary-hsm)
> 硬體安全模組 (Hardware Security Module)。 提供隨需應變加密、金鑰管理及金鑰儲存空間作為受管理服務。 HSM 是實體應用裝置，可處理加密法處理的資源密集型作業，並減少應用程式的延遲時間。
---

:::
## Summary of Reflections on Trusting Trust
It attempts to convey the concept that there are vulnerabilities in the compiler that are not easy to find. The main concept is if the compiler itself is tampered with maliciously, then the whole system will become vulnerable.
In this paper, the author tried to demo how his perspective and actual attack concept.
In addition, this kind of attack is untraceable, which means it's hard to defend.
The conclusion is before we trust the computing system, we must take compiler security seriously and try to find an algorithm or method to detect if the compiler is tampered with or not.

## Summary of Reflections on trusting distributed trust
Nowadays, the authors have seen an explosion of academic and industrial cryptographic systems built on distributed trust, including secure multi-party computation applications and blockchains. These systems have great potential for improving security and privacy, but face a significant hurdle on the path to deployment. This paper attempt to establish a system that easy to set up a distributed-trust application without expensive, cross-organization coordination. For now, bootstrapping without cross-organization coordination can enable small organizations to securely deploy distributed-trust systems such as end-to-end encrypted messaging applications that could use the distributed trust to establish a public-key infrastructure or backup secret keys.

## Comparison between them
In "Reflections on Trusting Trust", talked about the computing system security in compiler exploitation with uneasy to detect property. And the other one talked about how to construct a trusting system nowadays in which the global system connects together and how to deploy the system easily. So, though they talked about "trusting", the previous one focused on attacking and detecting potential crises, and the other one focused on establishing trust and maintaining it within the distributed system.

The solution of these two papers first proposed a solution that the compiler should add some protection to the source code to prevent the injection of malicious code. The other one proposed a method such as distributed hash value to establish a trusting connection and use it to check the code that runs in the trust domain.

## Reflection
As I mentioned above, these papers proposed a few perspectives on different system articles. They used a different way to prove how important the problem is, and also proposed some concept or an actual way to address it. If I were the author of the first paper, I'll attempt to use some program analysis or runtime monitoring, to detect and prevent such attacks automatically. In addition, I'll extend the trusting trust concept to hardware attacks such as microprocessors or firmware backdoors, etc. In the second paper, I'll try to extend the distributed system trusting issue to blockchain technology which may have some vulnerabilities that can solve by the concept of this paper.  Another issue that I'd like to discuss is the trade-off of security and effective in the easy-deploy system that this paper proposed. Is there a way to achieve these properties simultaneously?