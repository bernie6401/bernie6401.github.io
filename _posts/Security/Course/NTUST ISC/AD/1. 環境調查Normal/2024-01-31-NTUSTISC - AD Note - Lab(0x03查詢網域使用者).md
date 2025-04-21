---
title: NTUSTISC - AD Note(Lab - 查詢網域使用者)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/1. 環境調查Normal"
---

# NTUSTISC - AD Note(Lab - 查詢網域使用者)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Lab Time - 環境調查

### ==查詢網域使用者==
常用的cheat sheet
```bash!
$ net user /domain
$ net user <username> /domain
```

:::spoiler Implementation
```bash!
$ net user /domain
這項要求會在網域 kuma.org 下的網域控制站處理。


\\WIN-818G5VCOLJO.kuma.org 的使用者帳戶

-------------------------------------------------------------------------------
Administrator            aleda.appolonia          alikee.perri
aloise.elfrida           amabelle.gayle           andree.suki
angelique.hilda          annice.eden              anya.gypsy
audi.rosalind            babb.joanne              bambi.etta
bear                     berget.celka             berna.raphaela
berny.kirby              bill.marylee             caitrin.latia
carey.kincaid            carlye.chloette          carmelle.libbi
casandra.cherrita        casi.hyacinth            cassondra.lothario
celeste.kelci            charis.kory              christi.nettle
coraline.mahalia         corine.celesta           cyndie.rhodie
daile.odetta             darlleen.dorisa          DefaultAccount
dollie.fayina            dominica.carmon          dorrie.paolina
eba.luca                 ella.randee              erena.elinore
fara.iseabal             fred.carmita             gabriel.diannne
garnet.constancia        gertrude.felecia         gillian.marsiella
giulietta.moyra          glenda.dorrie            Guest
henrieta.sabine          herminia.debby           issy.eudora
jerrie.morganne          jessa.corinna            jori.floria
joyann.sibella           kaja.brenda              karoly.nadeen
katee.annemarie          katharina.alyssa         kiri.kath
kizzee.margaux           krbtgt                   laurena.mirelle
lazaro.karoly            lilas.lindy              lily.kristofor
lina.allene              linda.neda               logan.janeen
lon.sonni                lorne.celie              lucilia.lelah
margo.sharl              marlyn.loralee           marney.ranee
martita.juanita          marylynne.susannah       maurizia.ines
mercy.edi                moyra.fanechka           nolana.rivy
ollie.dorita             orelee.peri              ortensia.fancy
philippa.eugenie         philis.gilli             pietra.fern
randene.lelah            ranee.delinda            reina.claire
renae.babette            reyna.gwendolyn          ricca.stefa
ronni.kristoforo         rosetta.lotta            ruthann.britta
ruthie.ebony             seana.jeanette           selestina.cassi
shantee.marylin          sherri.jacquetta         sile.rhiamon
sofie.darlleen           star.rikki               stormie.natala
命令已經成功完成。
```
:::
說明：如果目前登入的帳號是在domain底下，就會出現類似如上的結果，會有一大堆使用者，但是目前的帳號沒有在該domain底下，會出現以下error:
```bash!
$ C:\User\low>net user /domain
這項要求會在網域 kuma.org 下的網域控制站處理。

系統發生 5 錯誤。

存取被拒。
```

---