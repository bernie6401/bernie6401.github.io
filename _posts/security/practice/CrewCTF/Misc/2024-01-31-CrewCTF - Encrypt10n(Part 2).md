---
title: CrewCTF - Encrypt10n(Part 2)
tags: [CTF, CrewCTF, Misc]

category: "Security/Practice/CrewCTF/Misc"
---

# CrewCTF - Encrypt10n(Part 2)
## Background
[How To Open A TrueCrypt Container Using cryptsetup](https://kenfavors.com/code/how-to-open-a-truecrypt-container-using-cryptsetup/)
> `$ sudo cryptsetup --type tcrypt open container-to-mount container-name`

[什麽是塊設備，什麽是字符設備？有什麽區別？](https://blog.51cto.com/majesty/991565)
## Recon
這一題應該是沿用part 1得到的密碼進行解密
## Exploit
1. 用`cryptsetup`[^cryptsetup_tutorial]先進行解密
    ```bash
    $ sudo cryptsetup --type tcrypt open flag flag_decrypt
    Enter passphrase for flag:
    ```
    則輸出的結果就是一個container儲存在`/dev/mapper`，可以看到它是一個block device
    ```bash
    $ ll /dev/mapper
    total 0
    drwxr-xr-x  2 root root       80 Jul 12 21:44 .
    drwxr-xr-x 11 root root     3140 Jul 12 21:44 ..
    crw-------  1 root root  10, 236 Jul 11 23:06 control
    brw-rw----  1 root disk 252,   3 Jul 12 21:44 flag_dec
    ```
2. 再來就要把這個container掛起來，要掛起來才能讀取裡面的資料
    ```bash
    $ sudo mkdir /mnt/flag_dec
    $ sudo mount -o uid=1000 /dev/mapper/flag_dec /mnt/flag_dec
    $ ll /mnt/flag_dec
    total 12
    drwxrwxrwx 1 sbk6401 root 4096 Feb 16 19:38 .
    drwxr-xr-x 7 root    root 4096 Jul 12 21:57 ..
    -rwxrwxrwx 2 sbk6401 root 2360 Feb 12 01:08 flaaaaaaaaaaaaaaaaaaaaaaaag.txt
    $ cat /mnt/flag_dec/flaaaaaaaaaaaaaaaaaaaaaaaag.txt
    Vm0wd2QyUXlVWGxWV0d4V1YwZDRXRmxVU205V01WbDNXa2M1VjFac2JETlhhMk0xVjBaS2MySkVUbGhoTWsweFZtcEJlRll5U2tWVWJHaG9UV3N3ZUZadGNFdFRNVWw1VTJ0V1ZXSkhhRzlVVmxaM1ZsWmFkR05GWkZwV01VcEpWbTEwYTFkSFNrZGpSVGxhVmpOU1IxcFZXbUZrUjA1R1UyMTRVMkpIZHpGV1ZFb3dWakZhV0ZOcmJGSmlSMmhZV1d4b2IwMHhXbGRYYlhSWFRWZDBObGxWV2xOVWJGcFlaSHBDVjAxdVVuWlZha1pYWkVaT2MxZHNhR2xTTW1oWlYxWmtNRmxXVWtkV1dHaFlZbGhTV0ZSV2FFTlNiRnBZWlVoa1YwMUVSbGRaTUZaM1ZqSktWVkpZWkZkaGExcFlXa1ZhVDJNeFpITmhSMnhUVFcxb1dsWXhaRFJWTVZsNFUydGthbEp0VWxsWmJGWmhZMVpzY2xkdFJteFdia0pIVmpKNFQxWlhTa2RqUm14aFUwaENSRlpxU2tabFZsSlpZVVprVTFKWVFrbFhXSEJIVkRKU1YxZHVUbFJpVjJoeldXeG9iMWRXV1hoYVJGSnBUV3RzTkZkclZtdFdiVXB5WTBac1dtSkhhRlJXTVZwWFkxWktjbVJHVWxkaWEwcElWbXBLZWs1V1dsaFRhMXBxVWxkb1dGUlhOVU5oUmxweFVtMUdUMkpGV2xwWlZWcGhZVWRGZUdOSE9WaGhNVnBvVmtSS1QyTXlUa1phUjJoVFRXMW9lbGRYZUc5aU1XUnpWMWhvWVZKR1NuQlVWM1J6VFRGU1ZtRkhPVmhTTUhCNVZHeGFjMWR0U2toaFJsSlhUVVp3VkZacVJuZFNWa1p5VDFkc1UwMHlhRmxXYlhCTFRrWlJlRmRzYUZSaVJuQnhWV3hrVTFsV1VsWlhiVVpPVFZad2VGVXlkREJXTVZweVkwWndXR0V4Y0hKWlZXUkdaVWRPU0U5V1pHaGhNSEJ2Vm10U1MxUnRWa2RqUld4VllsZG9WRlJYTlc5V1ZtUlhWV3M1VWsxWFVucFdNV2h2V1ZaS1IxTnNaRlZXYkZwNlZGUkdVMk15UmtaUFYyaHBVbGhDTmxkVVFtRmpNV1IwVTJ0a1dHSlhhRmhaVkVaM1ZrWmFjVkp0ZEd0U2EzQXdXbFZhYTJGV1NuTmhNMmhYWVRGd2FGWlVSbFpsUm1SMVUyczFXRkpZUW5oV1Z6QjRZakZaZUZWc2FFOVdlbXh6V1d0YWQyVkdWWGxrUkVKWFRWWndlVll5ZUhkWGJGcFhZMGhLVjJGcldreFdha3BQVWpKS1IxcEdaRTVOUlhCS1ZqRmFVMU14VlhoWFdHaFlZbXhhVjFsc2FHOVdSbXhaWTBaa1dGWnNjRmxaTUZVMVlWVXhXRlZ1Y0ZkTlYyaDJWMVphUzFJeFRuTmFSbFpYWWtadmVsWkdWbUZaVjFKR1RsWmFVRll5YUhCVmJHaENaREZrVjFadE9WVk5WbkF3VlcwMVMxWkhTbGhoUm1oYVZrVmFNMVpyV21GalZrcDFXa1pPVGxacmIzZFhiRlpyWXpGVmVWTnVTbFJoTTFKWVZGYzFiMWRHYkZWU2EzQnNVbTFTZWxsVldsTmhSVEZaVVc1b1YxWXphSEpXVkVaclVqRldjMkZGT1ZkaGVsWjVWMWQwWVdReVZrZFdibEpyVWtWS2IxbFljRWRsVmxKelZtNU9XR0pHY0ZoWk1GSlBWMnhhV0ZWclpHRldNMmhJV1RJeFIxSXlSa2hoUlRWWFYwVktSbFpxU2pSV01XeFhWVmhvWVZKWFVsWlpiWFIzWWpGV2NWTnRPVmRTYlhoNVZtMDFhMVl4V25OalNHaFdWak5vY2xaclZYaFhSbFp6WVVaa1RtRnNXazFXYWtKclV6Rk9SMVp1VWxCV2JGcFlXV3RvUTJJeFdrZFdiVVphVm14c05WVnRkRzlWUmxsNVlVWm9XbGRJUWxoVk1GcGhZMVpPY1ZWc1drNVdNVWwzVmxSS05GWXhWWGxUYTJSVVlsVmFWbFp0ZUhkTk1WcHlWMjFHYWxacmNEQlZiVEV3VmpKS2NsTnJiRmROYmxKeVdYcEdWbVF3TVVsaVIwWnNZVEZ3V1ZkWGVHOVJNVkpIVld4YVlWSldjSE5WYlRGVFYyeHNjbGRzVG1oU1ZFWjZWVEkxYjFZeFdYcGhSMmhoVWtWYVlWcFZXbXRrVmxaMFpVWk9XRkpyY0ZwV2ExcGhXVlpzVjFSclpGZGlhelZYV1cxek1WWXhXblJsUjBaWFlrWktWMVpYTlV0VlZsWlZUVVJyUFE9PQ==
    ```

3. Decode flag
A lots of base64 encoding
    :::spoiler Screenshot
    ![](https://hackmd.io/_uploads/ryXdvQnK3.png)
    :::

4. Unmount & Delete
    ```bash
    $ sudo umount /mnt/flag_dec
    $ sudo rm -R -f /mnt/flag_dec
    $ sudo rm -R -f /dev/mapper/flag_dec
    $ sudo dmsetup remove_all
    ```

Flag: `crew{Tru33333_Crypt_w1th_V014t1l1ty!}`
## Reference
[^cryptsetup_tutorial]:[How To Open A TrueCrypt Container Using cryptsetup](https://kenfavors.com/code/how-to-open-a-truecrypt-container-using-cryptsetup/)