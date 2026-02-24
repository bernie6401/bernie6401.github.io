---
title: A&D of Network Security - Lab 2
tags: [NTU, NTU_PADNS]

category: "Security Course｜NTU PADNS"
date: 2023-03-12
---

# A&D of Network Security - Lab 2
<!-- more -->
###### tags: `Practicum of A&D of NS` `NTU`

## Lab Cheat Sheet(Cisco Packet Tracer)

### Setting VLAN
:::spoiler Switch
```bash!
Switch>enable
Switch#configure 
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#vlan 10
Switch(config-vlan)#name green
Switch(config-vlan)#vlan 20
Switch(config-vlan)#name yellow
Switch(config-vlan)#
Switch#
%SYS-5-CONFIG_I: Configured from console by console

Switch#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/5, Fa0/6, Fa0/7, Fa0/8
                                                Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                Fa0/13, Fa0/14, Fa0/15, Fa0/16
                                                Fa0/17, Fa0/18, Fa0/19, Fa0/20
                                                Fa0/21, Fa0/22, Fa0/23, Fa0/24
                                                Gig0/1, Gig0/2
10   green                            active
20   yellow                           active
...
```
:::
:::spoiler Switch相對應的Interface
```bash!
Switch#configure 
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#int f0/1
Switch(config-if)#switchport access vlan 10
Switch(config-if)#int f0/2
Switch(config-if)#switchport access vlan 10
Switch(config-if)#int f0/3
Switch(config-if)#switchport access vlan 20
Switch(config-if)#int f0/4
Switch(config-if)#switchport access vlan 20
Switch(config-if)#^Z
Switch#
%SYS-5-CONFIG_I: Configured from console by console

Switch#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/5, Fa0/6, Fa0/7, Fa0/8
                                                Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                Fa0/13, Fa0/14, Fa0/15, Fa0/16
                                                Fa0/17, Fa0/18, Fa0/19, Fa0/20
                                                Fa0/21, Fa0/22, Fa0/23, Fa0/24
                                                Gig0/1, Gig0/2
10   green                            active    Fa0/1, Fa0/2
20   yellow                           active    Fa0/3, Fa0/4
```
可以看到一開始設定的VLAN只有active，現在設定了對應的Interface後，就會加到對應的VLAN Tag(u一開始一定要先確定好哪個interface接到哪一台device)
:::

### Setting Inter-VLAN Routing
:::spoiler 各個PC
設定Default Gateway(如果要送封包出去，要從哪個大們出去)
![](https://i.imgur.com/YbEtq7B.png)
![](https://i.imgur.com/ovAxS2P.png)
![](https://i.imgur.com/oMuwoYP.png)
![](https://i.imgur.com/a1ZiSgU.png)
:::
:::spoiler Router
設定 Router 子介面 – 802.1q IP
```bash!
Router>enable
Router#configure 
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Router(config)#int g0/0/0.1
Router(config-subif)#encapsulation dot1Q 10
Router(config-subif)#ip addr 10.1.1.100 255.255.255.0
Router(config-subif)#int g0/0/0.2
Router(config-subif)#encapsulation dot1Q 20
Router(config-subif)#ip addr 10.2.2.100 255.255.255.0
Router(config-subif)#^Z
Router#
%SYS-5-CONFIG_I: Configured from console by console

Router#configure 
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Router(config)#interface GigabitEthernet0/0/0
Router(config-if)#no sh
```

---

設定靜態路由
```bash!
Router#configure 
Configuring from terminal, memory, or network [terminal]? 
Enter configuration commands, one per line.  End with CNTL/Z.
Router(config)#ip route 10.1.1.0 255.255.255.0 g0/0/0.1
%Default route without gateway, if not a point-to-point interface, may impact performance
Router(config)#ip route 10.2.2.0 255.255.255.0 g0/0/0.2
%Default route without gateway, if not a point-to-point interface, may impact performance
```
:::
:::spoiler Switch
Switch 連接 Router 改為 Trunk mode
![](https://i.imgur.com/oIZEpjS.png)
注意：是要修改與Router連接的介面
:::

:::spoiler Result
最後的結果
![](https://i.imgur.com/dxsangH.png)
:::