---
title: NTUSTISC - AD Note - Lab(Leak Password)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/1. 環境調查Normal"
---

# NTUSTISC - AD Note - Lab(Leak Password)
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Lab Time - 環境調查

### ==Lab - Leak Password from Description==
在Win2016的server manager當中，可以從`Dashboard/Tools/Active Directory Users and Computers`中看到整個網域使用者的部分資料，例如Name, Type和Description，而這個東西其實是所有整個網域使用者都看地到，所以==不可以把機敏資料寫在這裡例如帳密之類的==，就像下面截圖一樣，`Fara Iseabal`和`Lina Allene`的密碼都被leak出去了
![](https://hackmd.io/_uploads/HktYdvUTh.png)
當然，有加入網域的帳號也看的到，從Win10的網域帳號bear中，打開PowerShell
:::spoiler Result
```bash
$ Get-ADUser -Filter * -Proper Description | Select-object Name,Description

Name               Description
----               -----------
Administrator      Built-in account for administering the computer/domain
Guest              Built-in account for guest access to the computer/domain
DefaultAccount     A user account managed by the system.
krbtgt             Key Distribution Center Service Account
Coraline Mahalia
Gillian Marsiella
Casi Hyacinth
Mercy Edi
Cyndie Rhodie
Lucilia Lelah
Fred Carmita
Ortensia Fancy
Seana Jeanette
Logan Janeen
Cassondra Lothario
Ollie Dorita
Gertrude Felecia
Ella Randee        New User ,DefaultPassword
Anya Gypsy
Ronni Kristoforo
Maurizia Ines
Reyna Gwendolyn
Garnet Constancia
Darlleen Dorisa
Jessa Corinna
Lorne Celie
Bill Marylee
Berna Raphaela
Gabriel Diannne    Shared User
Caitrin Latia
Selestina Cassi
Carlye Chloette
Dorrie Paolina
Herminia Debby
Rosetta Lotta
Berny Kirby
Moyra Fanechka
Ranee Delinda
Orelee Peri
Shantee Marylin
Annice Eden
Stormie Natala
Glenda Dorrie
Laurena Mirelle
Casandra Cherrita
Lazaro Karoly
Lina Allene        User Password r2NE4/9:F;[k
Kiri Kath
Star Rikki
Aloise Elfrida     Shared User
Marylynne Susannah
Sherri Jacquetta
Carey Kincaid
Philippa Eugenie
Dominica Carmon
Eba Luca
Martita Juanita
Ruthie Ebony
Charis Kory
Bambi Etta
Aleda Appolonia    Shared User
Randene Lelah
Issy Eudora
Margo Sharl
Philis Gilli
Reina Claire
Corine Celesta
Lon Sonni
Joyann Sibella
Katee Annemarie
Henrieta Sabine
Daile Odetta
Marney Ranee
Marlyn Loralee
Fara Iseabal       User Password 8F%kJ2q_cVFg
Sofie Darlleen
Jori Floria        Replication Account
Alikee Perri
Karoly Nadeen
Renae Babette
Nolana Rivy
Carmelle Libbi
Sile Rhiamon
Ruthann Britta
Pietra Fern
Amabelle Gayle
Audi Rosalind
Dollie Fayina
Ricca Stefa
Kaja Brenda
Katharina Alyssa
Angelique Hilda
Linda Neda         Shared User
Jerrie Morganne
Giulietta Moyra
Erena Elinore
Lily Kristofor
Kizzee Margaux
Christi Nettle
Lilas Lindy
Celeste Kelci
Berget Celka
Babb Joanne
Andree Suki
Bear Brown
```
:::
帳密一、Lina Allene$\to$`r2NE4/9:F;[k`
帳密二、Fara Iseabal$\to$`8F%kJ2q_cVFg`

---