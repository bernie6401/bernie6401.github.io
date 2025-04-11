---
title: PicoCTF - Some Assembly Required 1
tags: [PicoCTF, CTF, Web]

category: "Security/Practice/PicoCTF/Web"
---

# PicoCTF - Some Assembly Required 1
###### tags: `PicoCTF` `CTF` `Web`
Challenge: [Some Assembly Required 1](https://play.picoctf.org/practice/challenge/152?category=1&page=1)

## Background
[了解 WebAssembly 的基礎使用方法](https://blog.techbridge.cc/2017/06/17/webassembly-js-future/)

## Source code - After [Beautify](https://beautifier.io/)
:::spoiler source code
```javascript=
const strings = ['value', '2wfTpTR', 'instantiate', '275341bEPcme', 'innerHTML', '1195047NznhZg', '1qfevql', 'input', '1699808QuoWhA', 'Correct!', 'check_flag', 'Incorrect!', './JIFxzHyW8W', '23SMpAuA', '802698XOMSrr', 'charCodeAt', '474547vVoGDO', 'getElementById', 'instance', 'copy_char', '43591XxcWUl', '504454llVtzW', 'arrayBuffer', '2NIQmVj', 'result'];

const search_string1 = function(id1, _0x53c021) {
    id1 = id1 - 470;
    let strings6f = strings[id1];
    return strings6f;
};

(function(id1, id2) {
    const search_string = search_string1;
    while (!![]) {
        try {
            const secret_key = -parseInt(search_string(0x1eb)) + parseInt(search_string(0x1ed)) + -parseInt(search_string(0x1db)) * -parseInt(search_string(0x1d9)) + -parseInt(search_string(0x1e2)) * -parseInt(search_string(0x1e3)) + -parseInt(search_string(0x1de)) * parseInt(search_string(0x1e0)) + parseInt(search_string(0x1d8)) * parseInt(search_string(0x1ea)) + -parseInt(search_string(0x1e5));
            if (secret_key === id2) break;
            else id1['push'](id1['shift']());
        } catch (_0x41d31a) {
            id1['push'](id1['shift']());
        }
    }
}(strings, 627907));
let exports;
(async () => {
    const search_string = search_string1;
    let _0x5f0229 = await fetch(search_string(489)),
        _0x1d99e9 = await WebAssembly[search_string(479)](await _0x5f0229[search_string(474)]()),
        _0x1f8628 = _0x1d99e9[search_string(470)];
    exports = _0x1f8628['exports'];
})();

function onButtonPress() {
    const search_string = search_string1;
    let input_value = document['getElementById'](search_string(484))[search_string(477)]; // document['getElementById'](input)[value]
    for (let i = 0; i < input_value['length']; i++) {
        exports[search_string(471)](input_value[search_string(492)](i), i);
    }
    exports['copy_char'](0, input_value['length']), exports[search_string(487)]() == 1 ? document[search_string(494)](search_string(0x1dc))[search_string(0x1e1)] = search_string(0x1e6) : document[search_string(0x1ee)](search_string(0x1dc))[search_string(0x1e1)] = search_string(0x1e8);
}
```
:::
## Exploit - Beautify JS + Analyze
Please check line 24, the process will fetch `./JIFxzHyW8W` file at main webpage. We can check it out what this file is.
Payload: `mercury.picoctf.net:40226/JIFxzHyW8W`
Then the flag hide in the file you downloaded.
:face_with_rolling_eyes: 

## Reference
[parseInt](https://medium.com/unalai/認識-parseint-parsefloat-與-number-轉換成數字的三種方法-276640aedb4e)