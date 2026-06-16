"""Apply content-based tags to Books Notes posts with empty tags."""
import re
from pathlib import Path

ROOT = Path(r"d:/Website/_posts/Books Notes")

# path (relative to _posts) -> 1-5 tags based on content analysis
TAGS: dict[str, list[str]] = {
    "_posts/Books Notes/大眾文學/2026-05-18-末日之前不要睡著.md": [
        "網路暴力",
        "親子關係",
        "台灣文學",
        "失蹤案",
    ],
    "_posts/Books Notes/大眾文學/2026-05-29-你的孩子不是你的孩子.md": [
        "親子教育",
        "台灣文學",
        "家庭關係",
        "管教方式",
    ],
    "_posts/Books Notes/大眾文學/日本/2023-08-15-華麗なる一族(華麗一族).md": [
        "家族興衰",
        "山崎豐子",
        "日本文學",
        "金融改革",
        "性別議題",
    ],
    "_posts/Books Notes/大眾文學/日本/2025-07-07-一億円のさようなら(一億元的分手費).md": [
        "家庭謊言",
        "白石一文",
        "日本文學",
        "遺產",
    ],
    "_posts/Books Notes/大眾文學/日本/2025-07-14-未來.md": [
        "湊佳苗",
        "日本文學",
        "時間書信",
        "家庭創傷",
    ],
    "_posts/Books Notes/大眾文學/日本/2025-11-29-君の膵臓をたべたい(我想吃掉你的胰臟).md": [
        "青春文學",
        "住野夜",
        "日本文學",
        "生死議題",
    ],
    "_posts/Books Notes/大眾文學/日本/2025-12-25-かがみの孤城(鏡之孤城).md": [
        "拒學",
        "辻村深月",
        "日本文學",
        "校園霸凌",
        "本屋大賞",
    ],
    "_posts/Books Notes/大眾文學/日本/2026-01-25-成瀬は天下を取りにいく(奪取天下的少女).md": [
        "宮島未奈",
        "日本文學",
        "青春",
        "跳脫舒適圈",
    ],
    "_posts/Books Notes/大眾文學/日本/2026-01-28-蜜蜂と遠雷(蜜蜂與遠雷).md": [
        "鋼琴",
        "恩田陸",
        "日本文學",
        "音樂",
        "本屋大賞",
    ],
    "_posts/Books Notes/大眾文學/日本/2026-05-25-永遠の0(永遠的0).md": [
        "二戰",
        "百田尚樹",
        "日本文學",
        "神風特攻",
        "反戰",
    ],
    "_posts/Books Notes/大眾文學/歐美/2023-08-26-The Outcast(被放逐的孩子).md": [
        "童年創傷",
        "歐美文學",
        "自我放逐",
        "戰後英國",
    ],
    "_posts/Books Notes/大眾文學/歐美/2025-05-29-Billy Lynns Long Halftime Walk(半場無戰事).md": [
        "伊拉克戰爭",
        "歐美文學",
        "反戰",
        "美國政治",
    ],
    "_posts/Books Notes/大眾文學/歐美/2025-08-16-The Kite Runner(追風箏的孩子).md": [
        "阿富汗",
        "卡勒德·胡賽尼",
        "歐美文學",
        "贖罪",
        "友情",
    ],
    "_posts/Books Notes/大眾文學/歐美/2025-08-27-Das Parfum – Die Geschichte eines Mörders(香水).md": [
        "Patrick Süskind",
        "歐美文學",
        "氣味書寫",
        "巴黎",
        "連環殺人",
    ],
    "_posts/Books Notes/大眾文學/歐美/2025-09-27-Het Achterhuis(安妮日記).md": [
        "Anne Frank",
        "二戰",
        "歐美文學",
        "猶太人",
        "日記",
    ],
    "_posts/Books Notes/大眾文學/歐美/2025-12-17-Conversation With Friends(聊天紀錄).md": [
        "Sally Rooney",
        "歐美文學",
        "開放式關係",
        "情感糾葛",
    ],
    "_posts/Books Notes/大眾文學/歐美/2026-01-30-A Gentleman in Moscow(莫斯科紳士).md": [
        "俄國革命",
        "Amor Towles",
        "歐美文學",
        "軟禁",
    ],
    "_posts/Books Notes/大眾文學/歐美/2026-06-05-Lessons in Chemistry(化學家).md": [
        "女權",
        "Bonnie Garmus",
        "歐美文學",
        "1950年代",
        "化學",
    ],
    "_posts/Books Notes/大眾文學/韓國/2025-08-02-82년생 김지영(82年生的金智英).md": [
        "女權",
        "趙南柱",
        "韓國文學",
        "性別歧視",
    ],
    "_posts/Books Notes/大眾文學/韓國/2026-01-06-시간의 계단(時間的階梯).md": [
        "時間穿越",
        "韓國文學",
        "戀愛",
        "情緒勒索",
    ],
    "_posts/Books Notes/大眾文學/韓國/2026-02-19-시한부(死限來臨前請抓住我).md": [
        "青少年",
        "韓國文學",
        "憂鬱症",
        "校園霸凌",
        "自殺議題",
    ],
    "_posts/Books Notes/奇幻/2023-08-23-鹿の王(鹿王).md": [
        "上橋菜穗子",
        "奇幻",
        "戰爭",
        "日本文學",
    ],
    "_posts/Books Notes/奇幻/2026-01-20-六月のぶりぶりぎっちょう(六月的振振毬杖).md": [
        "萬城目學",
        "奇幻",
        "日本歷史",
        "日本文學",
    ],
    "_posts/Books Notes/恐怖靈異/2023-12-12-怪談和尚の京都怪奇譚(京都怪奇談).md": [
        "怪談",
        "京都",
        "日本文學",
        "短篇",
    ],
    "_posts/Books Notes/恐怖靈異/2023-12-12-日本恐怖實話.md": [
        "怪談",
        "日本文學",
        "靈異",
        "都市傳說",
    ],
    "_posts/Books Notes/恐怖靈異/2025-10-13-詭念.md": [
        "若花燃燃",
        "恐怖",
        "台灣文學",
        "科幻副作用",
    ],
    "_posts/Books Notes/恐怖靈異/2025-11-01-樓下的房客.md": [
        "九把刀",
        "偷窺",
        "台灣文學",
        "犯罪慾望",
    ],
    "_posts/Books Notes/恐怖靈異/2025-12-20-山村夜話.md": [
        "蔡耀彬",
        "台灣文學",
        "民俗恐怖",
        "人面花",
    ],
    "_posts/Books Notes/恐怖靈異/2026-04-22-近畿地方のある場所について(發生在近畿某處的那些事).md": [
        "背筋",
        "怪談",
        "日本文學",
        "偽紀錄",
        "詛咒",
    ],
    "_posts/Books Notes/恐怖靈異/2026-04-23-わたしと一緒にくらしましょう(和我一起生活吧).md": [
        "尾八原十時",
        "怪談",
        "日本文學",
        "詭異",
    ],
    "_posts/Books Notes/恐怖靈異/2026-05-12-筷：怪談競演奇物語.md": [
        "怪談",
        "短篇集",
        "陳浩基",
        "三津田信三",
        "台港日",
    ],
    "_posts/Books Notes/懸疑推理/2025-11-22-13.67.md": [
        "陳浩基",
        "香港",
        "推理",
        "本格推理",
        "警匪",
    ],
    "_posts/Books Notes/懸疑推理/2026-04-28-遺忘．刑警.md": [
        "陳浩基",
        "香港",
        "推理",
        "本格推理",
        "PTSD",
    ],
    "_posts/Books Notes/懸疑推理/2026-05-08-Vera Wong's Unsolicited Advice for Murderers(茶館裡的嫌疑人).md": [
        "推理",
        "溫馨",
        "華裔作家",
        "茶館",
    ],
    "_posts/Books Notes/懸疑推理/日本/2023-08-12-謎解きはディナーのあとで(推理要在晚餐後).md": [
        "東川篤哉",
        "本格推理",
        "日本文學",
        "短篇",
        "輕鬆推理",
    ],
    "_posts/Books Notes/懸疑推理/日本/2023-08-19-砂の器(砂之器).md": [
        "松本清張",
        "社会派推理",
        "日本文學",
        "冤案",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-05-15-ゴメンナサイ(對不起).md": [
        "日高由香",
        "日本文學",
        "詛咒",
        "校園",
        "第一人稱",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-06-02-ソロモンの偽証(所羅門的偽證-事件).md": [
        "宮部美幸",
        "社会派推理",
        "日本文學",
        "校園",
        "少年法庭",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-09-16-変な家2 ～11の間取り図～(詭屋 2：11張平面圖).md": [
        "雨穴",
        "本格推理",
        "日本文學",
        "間取り図",
        "建築推理",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-11-09-教室が、ひとりになるまで(直到教室只剩下一個人).md": [
        "淺倉秋成",
        "日本文學",
        "校園",
        "班級階級",
        "推理",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-11-29-世界でいちばん透きとおった物語(世界上最透明的故事).md": [
        "杉井光",
        "日本文學",
        "敘事詭計",
        "純文學",
        "尋父",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-11-29-＃真相をお話しします(#我要說出真相).md": [
        "結城真一郎",
        "日本文學",
        "短篇",
        "反轉",
        "推理",
    ],
    "_posts/Books Notes/懸疑推理/日本/2025-12-20-六つの嘘つきな大学生(六個說謊的大學生).md": [
        "淺倉秋成",
        "日本文學",
        "面試",
        "misdirection",
        "推理",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-01-15-かんぜんむざい(完全無罪).md": [
        "大門剛明",
        "社会派推理",
        "日本文學",
        "冤獄",
        "檢警",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-02-02-ノースライト(北光).md": [
        "橫山秀夫",
        "日本文學",
        "建築",
        "文学性推理",
        "失蹤",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-02-21-絕叫.md": [
        "葉真中顯",
        "社会派推理",
        "日本文學",
        "女性困境",
        "第二人稱",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-02-23-ナミヤ雑貨店の奇蹟(解憂雜貨店).md": [
        "東野圭吾",
        "日本文學",
        "時間穿越",
        "諮商",
        "暖心",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-05-14-奇岩館の殺人(奇岩館殺人案).md": [
        "高野結史",
        "日本文學",
        "後設推理",
        "本格推理",
        "密室",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-05-22-天才画の女(天才女畫家).md": [
        "松本清張",
        "社会派推理",
        "日本文學",
        "藝術",
        "側寫",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-06-07-放課後(放學後).md": [
        "東野圭吾",
        "本格推理",
        "日本文學",
        "密室",
        "校園",
    ],
    "_posts/Books Notes/懸疑推理/日本/2026-06-11-重力ピエロ(重力小丑).md": [
        "伊坂幸太郎",
        "日本文學",
        "兄弟",
        "復仇",
        "文学性推理",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2023-12-13-Hidden Pictures(詭畫連篇).md": [
        "Jason Rekulak",
        "歐美文學",
        "推理",
        "塗鴉",
        "戒毒",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2025-07-15-Origin(起源).md": [
        "Dan Brown",
        "歐美文學",
        "宗教",
        "科技",
        "驚悚",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2025-08-06-Choose Me(選擇).md": [
        "Tess Gerritsen",
        "歐美文學",
        "出軌",
        "推理",
        "古典文學",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2025-09-12-The Puppet Show(歡迎觀賞殺人預告).md": [
        "M.W. Craven",
        "歐美文學",
        "連環殺人",
        "犯罪側寫",
        "英國",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2025-11-01-Black Summer(黑色夏天殺人事件).md": [
        "M.W. Craven",
        "歐美文學",
        "連環殺人",
        "Washington系列",
        "英國",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2025-11-16-The Alienist(精神病學家).md": [
        "Caleb Carr",
        "歐美文學",
        "犯罪側寫",
        "1890年代",
        "紐約",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2025-12-05-The Lost Symbol(失落的符號).md": [
        "Dan Brown",
        "歐美文學",
        "共濟會",
        "華盛頓",
        "驚悚",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-01-03-Inferno(地獄).md": [
        "Dan Brown",
        "歐美文學",
        "人口過剩",
        "生物武器",
        "驚悚",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-01-19-Conclave(秘密會議).md": [
        "Robert Harris",
        "歐美文學",
        "梵蒂岡",
        "政治",
        "教宗選舉",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-02-13-The Long Goodbye(漫長的告別).md": [
        "Raymond Chandler",
        "歐美文學",
        "硬漢推理",
        "洛杉磯",
        "黑色電影",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-04-30-First Lie Wins(第一個謊最關鍵).md": [
        "Ashley Elston",
        "歐美文學",
        "特務",
        "社交工程",
        "反轉",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-05-03-The man who died twice(死了兩次的男人（週四謀殺俱樂部2）).md": [
        "Richard Osman",
        "歐美文學",
        "週四謀殺俱樂部",
        "養老院",
        "英式幽默",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-05-05-The Bullet That Missed(擦身而過的子彈（週四謀殺俱樂部3）).md": [
        "Richard Osman",
        "歐美文學",
        "週四謀殺俱樂部",
        "養老院",
        "推理",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-05-21-The Deep, Deep Snow(那年雪深幾呎).md": [
        "Brian Freeman",
        "歐美文學",
        "犯罪懸疑",
        "北歐",
        "綁架",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-06-02-The Last Devil to Die(魔鬼的最後一眼（週四謀殺俱樂部4）).md": [
        "Richard Osman",
        "歐美文學",
        "週四謀殺俱樂部",
        "失智症",
        "安樂死",
    ],
    "_posts/Books Notes/懸疑推理/歐美/2026-06-09-The Murders in the Rue Morgue and Other Great Tales(莫爾格街凶殺案： 謎與詭計的開端，推理小說開山祖愛倫坡，推理奇幻傑作選).md": [
        "Edgar Allan Poe",
        "歐美文學",
        "推理始祖",
        "偵探小說",
        "短篇集",
    ],
    "_posts/Books Notes/旅行文學/2025-10-18-十日談2020 Day 1：那些發生在瘟疫大流行前的故事.md": [
        "疫情",
        "旅行文學",
        "愛情",
        "十日談",
        "台灣文學",
    ],
    "_posts/Books Notes/旅行文學/2026-02-03-早知道就待在家.md": [
        "謝哲青",
        "旅行",
        "哲學",
        "台灣文學",
    ],
    "_posts/Books Notes/漫畫/2025-09-20-Điện Biên Phủ(奠邊府戰歌).md": [
        "越戰",
        "漫畫",
        "西島大介",
        "戰爭",
        "法國",
    ],
    "_posts/Books Notes/漫畫/2025-09-28-cocoon コクーン(cocoon 繭：沖繩姬百合隊的血色青春).md": [
        "沖繩",
        "二戰",
        "漫畫",
        "姬百合學徒隊",
        "戰爭",
    ],
    "_posts/Books Notes/科幻/2020-03-01-Vingt Mille Lieues sous les mers(海底兩萬里).md": [
        "Jules Verne",
        "科幻",
        "潛水艇",
        "冒險",
        "經典",
    ],
    "_posts/Books Notes/科幻/2025-06-04-Do Androids Dream of Electric Sheep(銀翼殺手).md": [
        "Philip K. Dick",
        "科幻",
        "仿生人",
        "末世",
        "人性",
    ],
    "_posts/Books Notes/科幻/2025-08-04-Cat's Cradle(貓的搖籃).md": [
        "Kurt Vonnegut",
        "科幻",
        "宗教諷刺",
        "末日",
        "黑色幽默",
    ],
    "_posts/Books Notes/科幻/2025-09-09-タイム・リープ：あしたはきのう(時間跳躍的你來自昨日).md": [
        "高畑京一郎",
        "科幻",
        "意識穿越",
        "日本文學",
        "時間",
    ],
    "_posts/Books Notes/科幻/2025-11-08-Project Hail Mary(極限返航).md": [
        "Andy Weir",
        "科幻",
        "太空",
        "外星人",
        "硬科幻",
    ],
    "_posts/Books Notes/科幻/2026-02-16-Cadáver exquisito(食人輓歌).md": [
        "Agustina Bazterrica",
        "科幻",
        "反烏托邦",
        "食人",
        "人口控制",
    ],
    "_posts/Books Notes/純文學/2024-04-24-傾城之戀【張愛玲百歲誕辰紀念版】：短篇小說集一　1943年.md": [
        "張愛玲",
        "純文學",
        "短篇集",
        "香港",
        "第一爐香",
    ],
    "_posts/Books Notes/純文學/2025-12-12-成為真正的人（minBunun）.md": [
        "甘耀明",
        "純文學",
        "三叉山事件",
        "布農族",
        "二戰",
    ],
    "_posts/Books Notes/純文學/2026-01-20-色，戒【張愛玲百歲誕辰紀念版】：短篇小說集三 1947年以後.md": [
        "張愛玲",
        "純文學",
        "短篇集",
        "色戒",
        "1940年代",
    ],
    "_posts/Books Notes/純文學/2026-05-08-海邊的房間.md": [
        "黃麗群",
        "純文學",
        "短篇集",
        "台灣文學",
        "女性",
    ],
    "_posts/Books Notes/純文學/日本/2020-01-25-人間失格.md": [
        "太宰治",
        "純文學",
        "日本文學",
        "頹廢",
        "自傳性",
    ],
    "_posts/Books Notes/純文學/日本/2023-08-30-色彩を持たない多崎つくると、彼の巡礼の年(沒有色彩的多崎作和他的巡禮之年).md": [
        "村上春樹",
        "純文學",
        "日本文學",
        "友情",
        "巡禮",
    ],
    "_posts/Books Notes/純文學/日本/2025-07-03-ノルウェイの森(挪威的森林).md": [
        "村上春樹",
        "純文學",
        "日本文學",
        "愛情",
        "1960年代",
    ],
    "_posts/Books Notes/純文學/日本/2026-04-17-火花.md": [
        "又吉直樹",
        "純文學",
        "日本文學",
        "漫才",
        "喜劇",
    ],
    "_posts/Books Notes/純文學/日本/2026-05-19-博士の愛した数式(博士熱愛的算式).md": [
        "小川洋子",
        "純文學",
        "日本文學",
        "數學",
        "記憶",
    ],
    "_posts/Books Notes/純文學/日本/2026-06-09-コンビニ人間(便利店人間).md": [
        "村田沙耶香",
        "純文學",
        "日本文學",
        "社會規範",
        "便利店",
    ],
    "_posts/Books Notes/純文學/歐美/2020-02-25-L'Etranger(異鄉人).md": [
        "Albert Camus",
        "純文學",
        "存在主義",
        "荒謬",
        "法庭",
    ],
    "_posts/Books Notes/純文學/歐美/2020-03-08-Die Leiden des jungen Werthers((少年維特的煩惱).md": [
        "歌德",
        "純文學",
        "歐美文學",
        "愛情",
        "自殺",
    ],
    "_posts/Books Notes/純文學/歐美/2025-07-17-Pride and Prejudice(傲慢與偏見).md": [
        "Jane Austen",
        "純文學",
        "歐美文學",
        "愛情",
        "階級",
    ],
    "_posts/Books Notes/純文學/歐美/2025-08-12-The Moon and Sixpence(月亮與六便士).md": [
        "毛姆",
        "純文學",
        "歐美文學",
        "高更",
        "藝術",
    ],
    "_posts/Books Notes/純文學/歐美/2025-09-19-The Heart of The Matter(事物的核心).md": [
        "Graham Greene",
        "純文學",
        "歐美文學",
        "西非",
        "信仰",
    ],
    "_posts/Books Notes/純文學/歐美/2025-10-16-The Great Gatsby(大亨小傳).md": [
        "F. Scott Fitzgerald",
        "純文學",
        "歐美文學",
        "美國夢",
        "1920年代",
    ],
    "_posts/Books Notes/純文學/歐美/2025-12-25-Of Mice and Men(人鼠之間).md": [
        "John Steinbeck",
        "純文學",
        "歐美文學",
        "大蕭條",
        "夢想",
    ],
    "_posts/Books Notes/純文學/歐美/2026-01-01-Slaughterhouse-Five(第五號屠宰場).md": [
        "Kurt Vonnegut",
        "純文學",
        "反戰",
        "時間旅行",
        "德勒斯登",
    ],
    "_posts/Books Notes/純文學/歐美/2026-04-23-Sophie’s Choice(蘇菲的抉擇).md": [
        "William Styron",
        "純文學",
        "歐美文學",
        "納粹",
        "創傷",
    ],
    "_posts/Books Notes/青少年文學/2020-02-24-13 Reasons Why(漢娜的遺言).md": [
        "Jay Asher",
        "青少年文學",
        "霸凌",
        "自殺",
        "美國",
    ],
    "_posts/Books Notes/青少年文學/2020-07-14-Ferryman(擺渡人).md": [
        "Claire McFall",
        "青少年文學",
        "奇幻",
        "愛情",
        "來世",
    ],
    "_posts/Books Notes/青少年文學/2025-12-15-The Female of The Species(雌性物種).md": [
        "Mindy McGinnis",
        "青少年文學",
        "性暴力",
        "私刑",
        "復仇",
    ],
    "_posts/Books Notes/青少年文學/2026-01-12-The Absolutely True Diary of a Part-Time Indian(一個印第安少年的超真實日記).md": [
        "Sherman Alexie",
        "青少年文學",
        "原住民",
        "保留區",
        "成長",
    ],
    "_posts/Books Notes/青少年文學/2026-04-21-Untethered Sky(不馴之翼).md": [
        "Fonda Lee",
        "青少年文學",
        "奇幻",
        "鷹獵",
        "成長",
    ],
    "_posts/Books Notes/非文學/2025-07-21-不為人知的都市傳說.md": [
        "都市傳說",
        "暗網",
        "邪教",
        "非虛構",
    ],
    "_posts/Books Notes/非文學/2025-07-30-怖い絵(膽小別看畫).md": [
        "藝術史",
        "中野京子",
        "繪畫",
        "工具書",
    ],
    "_posts/Books Notes/非文學/2025-10-05-Tuesdays with Morrie(最後14堂星期二的課).md": [
        "Mitch Albom",
        "死亡",
        "人生哲學",
        "師生",
        "漸凍人",
    ],
    "_posts/Books Notes/非文學/人文社科/2020-03-15-The Reckoning - Financial Accountability and the Rise and Fall of Nations(大查帳).md": [
        "會計史",
        "財政",
        "複式簿記",
        "歷史",
    ],
    "_posts/Books Notes/非文學/人文社科/2025-09-21-手繪圖解日本史.md": [
        "日本史",
        "圖解",
        "歷史",
        "工具書",
    ],
    "_posts/Books Notes/非文學/人文社科/2025-10-05-無住之島.md": [
        "居住正義",
        "房價",
        "租屋",
        "台灣",
    ],
    "_posts/Books Notes/非文學/人文社科/2025-10-10-Surveillance State - Inside China’s Quest to Launch a New Era of Social Control(監控國家).md": [
        "監控",
        "中國",
        "社會控制",
        "科技",
        "個資",
    ],
    "_posts/Books Notes/非文學/人文社科/2025-12-13-安いニッポン「価格」が示す停滞(廉價日本).md": [
        "日本經濟",
        "通縮",
        "物價",
        "薪資",
    ],
    "_posts/Books Notes/非文學/人文社科/2026-01-07-Primates of Park Avenue(我是一個媽媽，我需要柏金包！).md": [
        "上東區",
        "階級",
        "母職",
        "消費文化",
        "紐約",
    ],
    "_posts/Books Notes/非文學/人文社科/2026-02-04-ドキュメント小説　ケーキの切れない非行少年たちのカルテ(不會切蛋糕的犯罪少年診療實錄).md": [
        "少年非行",
        "智能障礙",
        "宮口幸治",
        "日本",
        "心理",
    ],
    "_posts/Books Notes/非文學/人文社科/2026-04-16-Jak Nakarmić Dyktatora(獨裁者的廚師).md": [
        "獨裁",
        "紀實",
        "極權",
        "廚師",
        "口述歷史",
    ],
    "_posts/Books Notes/非文學/人文社科/2026-05-25-他們就是我們：犯罪心理學家的人性思辨.md": [
        "犯罪心理學",
        "戴伸峰",
        "台灣",
        "性犯罪",
        "高齡犯罪",
    ],
    "_posts/Books Notes/非文學/人文社科/2026-06-12-詐騙社會學.md": [
        "詐騙",
        "社會學",
        "孫中興",
        "哲學",
        "台灣",
    ],
    "_posts/Books Notes/非文學/人文社科/2026-06-15-いい子に育てると犯罪者になります(教出殺人犯).md": [
        "育兒",
        "犯罪心理",
        "岡本茂樹",
        "日本",
        "情緒教育",
    ],
    "_posts/Books Notes/非文學/工具書/2020-02-24-活色生香的希臘神話.md": [
        "希臘神話",
        "神話",
        "工具書",
    ],
    "_posts/Books Notes/非文學/工具書/2022-05-06-Prisoner's Dilemma - John von Neumann, Game Theory, and the Puzzle of the Bomb(囚犯的兩難).md": [
        "賽局理論",
        "馮紐曼",
        "核武",
        "數學",
    ],
    "_posts/Books Notes/非文學/工具書/2024-01-10-日本神話.md": [
        "日本神話",
        "神話",
        "工具書",
        "伊邪那岐",
    ],
    "_posts/Books Notes/非文學/工具書/2024-06-09-北歐神話.md": [
        "北歐神話",
        "神話",
        "工具書",
        "奧丁",
    ],
    "_posts/Books Notes/非文學/工具書/2025-09-13-小說課之王.md": [
        "寫作",
        "許榮哲",
        "小說技巧",
        "工具書",
    ],
    "_posts/Books Notes/非文學/工具書/2025-12-05-ニーチェが京都にやってきて17歳の私に哲学のこと教えてくれた(當失戀的我，遇上尼采).md": [
        "哲學",
        "尼采",
        "日本文學",
        "失戀",
        "入門",
    ],
    "_posts/Books Notes/非文學/工具書/2026-01-12-嫌われる勇気：自己啟発の源流「アド ラー」の教え(被討厭的勇氣：自我啟發之父「阿德勒」的教導).md": [
        "阿德勒",
        "心理學",
        "自我成長",
        "哲學對話",
    ],
    "_posts/Books Notes/非文學/紀實文學/2024-06-11-這才是真實的巴勒斯坦.md": [
        "巴勒斯坦",
        "以巴衝突",
        "紀實",
        "中東",
        "歷史",
    ],
    "_posts/Books Notes/非文學/紀實文學/2025-05-30-烏克蘭的不可能戰爭.md": [
        "烏克蘭",
        "俄烏戰爭",
        "報導者",
        "紀實",
        "戰爭",
    ],
    "_posts/Books Notes/非文學/紀實文學/2026-05-16-マイ・バック・ページある60年代の物語(我愛過的那個時代：當時，我們以為可以改變世界).md": [
        "日本學運",
        "1960年代",
        "反越戰",
        "紀實",
        "新左派",
    ],
}


def format_tags(tags: list[str]) -> str:
    return "tags: [" + ", ".join(tags) + "]"


def apply_tags(path_key: str, tags: list[str]) -> bool:
    file_path = Path("d:/Website") / path_key.replace("/", "\\").replace(
        "_posts\\", "_posts/"
    )
    # Normalize path
    file_path = Path("d:/Website") / Path(path_key).relative_to("_posts").as_posix()
    file_path = Path("d:/Website") / path_key.replace("_posts/", "_posts/")

    rel = path_key.replace("_posts/", "")
    file_path = ROOT.parent / "_posts" / rel.replace("/", "\\")
    if not file_path.exists():
        file_path = Path("d:/Website") / path_key.replace("\\", "/")

    text = file_path.read_text(encoding="utf-8")
    if not re.search(r"^tags:\s*\[\]\s*$", text, re.MULTILINE):
        return False
    new_text = re.sub(
        r"^tags:\s*\[\]\s*$",
        format_tags(tags),
        text,
        count=1,
        flags=re.MULTILINE,
    )
    file_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    updated = 0
    missing = []

    # Normalize keys for lookup (forward slashes, _posts prefix)
    normalized_tags = {
        k.replace("\\", "/"): v for k, v in TAGS.items()
    }

    for f in sorted(ROOT.rglob("*.md")):
        key = f.relative_to(Path("d:/Website")).as_posix()

        text = f.read_text(encoding="utf-8")
        if not re.search(r"^tags:\s*\[\]\s*$", text, re.MULTILINE):
            continue

        tags = normalized_tags.get(key)
        if not tags:
            missing.append(key)
            continue

        if len(tags) < 1 or len(tags) > 5:
            raise ValueError(f"{key}: {len(tags)} tags (need 1-5)")

        new_text = re.sub(
            r"^tags:\s*\[\]\s*$",
            format_tags(tags),
            text,
            count=1,
            flags=re.MULTILINE,
        )
        f.write_text(new_text, encoding="utf-8")
        updated += 1

    result = {"updated": updated, "missing_count": len(missing), "missing": missing}
    Path("d:/Website/tag_apply_result.json").write_text(
        __import__("json").dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Updated: {updated}, Missing: {len(missing)}")


if __name__ == "__main__":
    main()
