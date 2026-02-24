---
title: Cryptography and Network Security – Comparative Critique 3
tags: [NTUCNS, NTU]

category: "Security Course｜NTU CNS｜Paper Critique"
date: 2024-02-07
---

# Cryptography and Network Security – Comparative Critique 3
<!-- more -->

[![hackmd-github-sync-badge](https://hackmd.io/MLHx12AhT-S-DUoRfGUn4A/badge)](https://hackmd.io/MLHx12AhT-S-DUoRfGUn4A)

## Reading Topic: DNSSEC VS DoH(DNS-over-HTTPS)
###### tags: `NTUCNS`
Name: 何秉學	Student ID: R11921A16

## Background
[什麼是 DNSSEC？](https://tw.godaddy.com/help/what-is-dnssec-6135)
> 什麼是 DNSSEC？
>
>網域名稱系統安全性擴充 (DNSSEC) 可為網域名稱的 DNS (網域名稱系統) 加上電子簽名，藉此判斷來源網路名稱的真實性。此功能可以保護網路使用者不受假造 DNS 資料的威脅，讓使用者要求正確網址時不會取得其他有意誤導或惡意製作的網址。
>
>啟用 DNSSEC 後，DNS 查閱會使用電子簽名驗證網站 DNS 來源是否有效，這樣做可以協助防止受到特定類型的攻擊，而當電子簽名不一致的時候，瀏覽器便不會顯示網站。

[What is DNS Cache Poisoning? - 小心網域名稱伺服器快取毒害(DNS cache poisoning)攻擊](https://blog.miniasp.com/post/2008/10/22/Be-careful-DNS-cache-poisoning-attack)
> 簡單的說，DNS 通常都會實做快取(Cache)功能，若 DNS 收到來自惡意假造的 DNS 封包，導致將錯誤的 Domain Name v.s. IP 對應資料快取在 DNS Server 中，就會讓使用這台 DNS Server 的使用者連結到錯誤的 IP，這將會是個十分嚴重的安全性漏洞！而這樣的安全性漏洞就稱之為 DNS cache poisoning


## Summary of paper 1
DNSSEC is a security extension protocol designed to protect the security of information during domain name resolution. It uses public key encryption technology to sign and verify data in the network DNS, thereby ensuring the integrity and authenticity of the data. DNSSEC provides a mechanism for clients to verify whether the DNS resource record (such as IP addresses, email addresses, etc.) they requested is from the correct source and has not been tampered with. This effectively prevents security issues such as DNS cache poisoning attacks and DNS hijacking. DNSSEC plays an important role in protecting Internet security, and many government agencies, financial institutions, and businesses have begun to deploy DNSSEC.

## Summary of paper 2
DoH is a mechanism that encrypts DNS queries over the HTTPS protocol. Its purpose is to improve the reliability and efficiency of DNS queries while increasing privacy and security. Traditional DNS queries are in plaintext and vulnerable to eavesdropping and interception. Using DoH, DNS queries are encrypted, protecting users' privacy and data security. DoH can also prevent DNS cache poisoning attacks and DNS hijacking, improving the security of DNS resolution. DoH can also help network providers reduce a load of DNS queries, improving network performance and speed. Since DoH is transmitted via the standard HTTPS protocol, it can more easily pass through corporate and organizational firewalls and is not blocked or restricted by ISPs.

## Comparison between them
Both of them can prevent DNS cache poisoning attacks and DNS hijacking attacks and enhance the security and reliability of DNS queries. Also, they can preserve the privacy of users, e.g., DNSSEC can avoid DNS man-in-the-middle attacks and data tampering and DoH can encrypt DNS queries, protecting users' privacy and data security, preventing DNS eavesdropping and interception. However, they still have some drawbacks to conquer such as the implementation of DNSSEC and DoH are complex and requires special configuration and management. Moreover, if DoH or DNSSEC is used, it may increase network congestion and delay, because it needs to use HTTPS protocol (for DoH) to encrypt and decrypt DNS queries.

## Your own reflection
If I were the author, I would consider conducting more experiments and evaluations to validate the effectiveness and performance of these technologies in different scenarios. I would also explore ways to enhance their interoperability with other security technologies and ensure their widespread adoption and implementation. There are still some unsolved questions regarding DNSSEC and DoH, such as the challenges of key management, the potential impact on network performance, and the trade-offs between security and usability. Further research is needed to address these questions and refine these technologies.