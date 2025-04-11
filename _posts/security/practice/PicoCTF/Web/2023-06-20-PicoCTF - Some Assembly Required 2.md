---
title: PicoCTF - Some Assembly Required 2
tags: [PicoCTF, CTF, Web]

category: "Security > Practice > PicoCTF > Web"
---

# PicoCTF - Some Assembly Required 2
###### tags: `PicoCTF` `CTF` `Web`

## Background

## Source code
:::spoiler source
```javascript
const list_str = ['copy_char', 'value', '207aLjBod', '1301420SaUSqf', '233ZRpipt', '2224QffgXU', 'check_flag', '408533hsoVYx', 'instance', '278338GVFUrH', 'Correct!', '549933ZVjkwI', 'innerHTML', 'charCodeAt', './aD8SvhyVkb', 'result', '977AzKzwq', 'Incorrect!', 'exports', 'length', 'getElementById', '1jIrMBu', 'input', '615361geljRK'];
const func1_cal = function(var_a, var_b) {
    var_a = var_a - 195;
    let list_strc4 = list_str[var_a];
    return list_strc4;
};
(function(var_a, var_b) {
    const func1_cal = func1_cal;
    while (!![]) {
        try {
            const var_c = -parseInt(func1_cal(200)) * -parseInt(func1_cal(201)) + -parseInt(func1_cal(205)) + parseInt(func1_cal(207)) + parseInt(func1_cal(195)) + -parseInt(func1_cal(198)) * parseInt(func1_cal(212)) + parseInt(func1_cal(203)) + -parseInt(func1_cal(217)) * parseInt(func1_cal(199));
            if (var_c === var_b) break;
            else var_a['push'](var_a['shift']());
        } catch (_0x4f8a) {
            var_a['push'](var_a['shift']());
        }
    }
}(list_str, 310022));
let exports;
(async () => {
    const func1_cal = func1_cal;
    let res_1 = await fetch(func1_cal(210)),
        res_2 = await WebAssembly['instantiate'](await res_1['arrayBuffer']()),
        res_3 = res_2[func1_cal(204)];
    exports = res_3[func1_cal(214)];
})();

function onButtonPress() {
    const func1_cal = func1_cal;
    let res_1 = document[func1_cal(216)](func1_cal(218))[func1_cal(197)];
    for (let idx = 0; idx < res_1['length']; idx++) {
        exports[func1_cal(196)](res_1[func1_cal(209)](idx), idx);
    }
    exports['copy_char'](0, res_1[func1_cal(215)]), exports[func1_cal(202)]() == 1 ? document['getElementById'](func1_cal(211))[func1_cal(208)] = func1_cal(206) : document[func1_cal(216)](func1_cal(211))['innerHTML'] = func1_cal(213);
}
```
:::

## Exploit
這一題也是想破頭了，首先應該很容易可以拿到前端驗證的code如上，beautify之後可以看到一個`./aD8SvhyVkb`的可疑檔案，取得之後發現是一個`.wasm` file
```bash
$ file aD8SvhyVkb
aD8SvhyVkb: WebAssembly (wasm) binary module version 0x1 (MVP)
$ strings aD8SvhyVkb
memory
__wasm_call_ctors
strcmp
check_flag
input
        copy_char
__dso_handle
__data_end
__global_base
__heap_base
__memory_base
__table_base
j!
  F!!A
!" ! "q!# #
!% $ %q!&
!( ' (q!) & )k!*
!+ +
        q!
+xakgK\Ns><m:i1>1991:nkjl<ii1j0n=mm09;<i:u
```
感覺最後的字串有一點奇怪，丟到[cyberchef](https://gchq.github.io/CyberChef)用magic解看看，就出現flag了，其實就只是XOR 8而已
Flag: `picoCTF{64e2a9691192fcbd4aa9b8f5ee8134a2}`

## Reference
[ picoCTF 2021 Some Assembly Required 2 ](https://youtu.be/2TCZEkW0bjc)