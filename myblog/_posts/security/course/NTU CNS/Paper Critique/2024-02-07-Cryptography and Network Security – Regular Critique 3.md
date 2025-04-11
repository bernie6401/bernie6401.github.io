---
title: Cryptography and Network Security – Regular Critique 3
tags: [NTUCNS, NTU]

---

# Cryptography and Network Security – Regular Critique 3

[![hackmd-github-sync-badge](https://hackmd.io/q_V04ik8RkCQS4-DbqJoGg/badge)](https://hackmd.io/q_V04ik8RkCQS4-DbqJoGg)

## Reading Topic: Automated Detection of IPv6 Privacy Leakage in Home Networks
###### tags: `NTUCNS`
Name: 何秉學	Student ID: R11921A16

## Background
[What is Customer Premise Equipment? - 用戶終端設備(CPE)](https://www.moneydj.com/kmdj/wiki/wikiviewer.aspx?keyid=047cf9b1-e1ba-4578-8fcc-160bd2d3fc8d)
> 英文名稱為Customer Premise Equipment，是指網路連接至用戶端的相關設備，包括數據機、寬頻路由器、寬頻閘道器等，但隨著電信網路應用服務逐漸多元化，只要是用戶端所使用的網路服務設備，都可稱為CPE裝置，包括VoIP閘道器、IP phone、雙模手機、IP STB等。

[What is EUI-64?](https://www.jannet.hk/ip-address-version-6-ipv6-zh-hant/)
>IPv6 Address太長，要網管人員逐個Interface設定IPv6 Address肯定是件痛苦的事。EUI-64讓我們只需幫Interface试定Prefix部份,然後Interface就會用MAC Address自動產生Interface ID，基於MAC Address 獨一無二，利用 EUI-64 必能生成獨一無二的 IPv6 Address。EUI-64 產生 Interface ID 的辦法是先把MAC Address （共48 Bits）斬開兩等份.中間插入FFFE供16 Bits），使其成為64 Bits，然後把第7 Bit由0改成1。最後在前面加上Prefix歟成為一組IPv6 Address 了。
>
>舉例，MAC Address : `00:50:56:C1:A0:E8`
中間插入 `FFFE` 使其成為 EUI-64 Interface ID : `0050:56FF:FEC1:A0E8`
最後把第 7 Bit 改成 1 : `0250:56FF:FEC1:A0E8`

[What is Stateless Address Autoconfiguration (SLAAC)?](https://www.jannet.hk/ip-address-version-6-ipv6-zh-hant/)
> Stateless Address Autoconfiguration (SLAAC)
在IPv4中我們可以透過DHCP讓 Interface自動獲PAddes,而在 Pv6 透Autoconfigurion來獲取IP Address前的部份說過EU-64可以幫我自生InterfaceD,所以現在解洪的就是她何獲取Prefix?IPv6用的是StatelessAddressAutoconfiguratio(狀態位址自動配置),Intface向Link-Local 發出 RS (Router Solicitation),IPv6 Router 可以回應RA(Router Advertisement),提供Prefix 資訊現誠把R1設定uer,R2嘗試透過AACA
![](https://i.imgur.com/rCcZUnM.png)



## Summary
We know that legacy deployment of IPv6 has leaked device identities problem. Thus, one of the solutions is privacy extensions to the IPv6 addressing mechanism. But still, it has its problem that will allow an adversary to track all users across the network, correlate users’ activities over time, or extract users’ precise geolocation. They tried to propose a tool that can allow users with minimal technical expertise to scan their local home networks to identify the IPv6-leaking devices and observe their ISP's prefix rotation policy.

## Strength(s) of the paper
They provide a tool that can view the prefixes assigned to them by their ISP and whether they are rotated on the IPv6-enabled devices that use legacy configurations of the standard. Also, they provided their tool's user-friendly user interface that allows users to easily scan and see devices.
Moreover, this paper is aimed to encourage more users to understand the issue of IPv6 privacy so they can drive the efforts to develop a more privacy-preserving IPv6 ecosystem, therefore, promotion is more important than the substance itself. I think this is a good chance for a normal user to be aware of this issue.

## Weakness(es) of the paper
My perspective is the novelty of this paper's contribution is not very state-of-the-art. Technically, it just provides a tool that is based on some previous technique so it has not had very high technical content. And in this paper, I think some of the terminologies are quite hard to understand and I hope they can describe it more to let me know the situation, the problem they encountered, the proposed method, etc.

## Your own reflection
Their starting point is they want more people to know what some issues or threats about IPv6 that more people used in recent years. Therefore, they provided a tool with a user-friendly UI that can let the user easily detect everything that they should pay attention to. However, if I were the author, I'll use a more approachable perspective or friendly terminology to tell my user what's going on with this issue and what the challenges we face are so that they can attempt to understand this important issue.
In addition, as the author said in the future work section, they tried to let these tools not just work locally and they'll try to use network traffic analysis to analyze more impact, however, some important info they store has some privacy problems. This is another issue they have to consider.
