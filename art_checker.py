# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:11:33 2024

@author: Shane
"""

import os

# Data given
j_colors1 = {
  "quiz_title": "Colors 1",
  "questions": [
    {
      "furigana": "あか",
      "kanji": "赤",
      "translation": "red",
      "image": "GFX/colors/red.png"
    },
    {
      "furigana": "あお",
      "kanji": "青",
      "translation": "blue",
      "image": "GFX/colors/blue.png"
    },
    {
      "furigana": "しろ",
      "kanji": "白",
      "translation": "white",
      "image": "GFX/colors/white.png"
    },
    {
      "furigana": "くろ",
      "kanji": "黒",
      "translation": "black",
      "image": "GFX/colors/black.png"
    },
    {
      "furigana": "みどり",
      "kanji": "緑",
      "translation": "green",
      "image": "GFX/colors/green.png"
    },
  ]
}

j_colors2 = {
  "quiz_title": "Colors 2",
  "questions": [
    {
      "furigana": "きいろ",
      "kanji": "黄色",
      "translation": "yellow",
      "image": "GFX/colors/yellow.png"
    },
    {
      "furigana": "ちゃいろ",
      "kanji": "茶色",
      "translation": "brown",
      "image": "GFX/colors/brown.png"
    },
    {
      "furigana": "むらさき",
      "kanji": "紫",
      "translation": "purple",
      "image": "GFX/colors/purple.png"
    },
    {
      "furigana": "はいいろ",
      "kanji": "灰色",
      "translation": "gray",
      "image": "GFX/colors/gray.png"
    },
    {
      "furigana": "きんいろ",
      "kanji": "金色",
      "translation": "gold",
      "image": "GFX/colors/gold.png"
    }
  ]
}

j_colors3 = {
  "quiz_title": "Colors 3",
  "questions": [
    {
      "furigana": "だいだいいろ",
      "kanji": "橙色",
      "translation": "orange",
      "image": "GFX/colors/orange.png"
    },
    {
      "furigana": "ももいろ",
      "kanji": "桃色",
      "translation": "pink",
      "image": "GFX/colors/pink.png"
    },
    # {
    #   "furigana": "きんいろ",
    #   "kanji": "金色",
    #   "translation": "gold",
    #   "image": "GFX/colors/gold.png"
    # },
    {
      "furigana": "ぎんいろ",
      "kanji": "銀色",
      "translation": "silver",
      "image": "GFX/colors/silver.png"
    },
    {
      "furigana": "こんいろ",
      "kanji": "紺色",
      "translation": "navy blue",
      "image": "GFX/colors/navy_blue.png"
    }
  ]
}

j_colors4 = {
  "quiz_title": "Colors 4",
  "questions": [
    {
      "furigana": "みずいろ",
      "kanji": "水色",
      "translation": "light blue",
      "image": "GFX/colors/light_blue.png"
    },
    {
      "furigana": "しこう",
      "kanji": "紫紅",
      "translation": "crimson",
      "image": "GFX/colors/crimson.png"
    },
    {
      "furigana": "きみどり",
      "kanji": "黄緑",
      "translation": "yellow-green",
      "image": "GFX/colors/yellow_green.png"
    },
    {
      "furigana": "わかくさいろ",
      "kanji": "若草色",
      "translation": "light green",
      "image": "GFX/colors/light_green.png"
    },
    {
      "furigana": "あさぎいろ",
      "kanji": "浅葱色",
      "translation": "light blue-green",
      "image": "GFX/colors/light_blue_green.png"
    }
  ]
}

j_colors5 = {
  "quiz_title": "Colors 5",
  "questions": [
    {
      "furigana": "さくらいろ",
      "kanji": "桜色",
      "translation": "cherry blossom pink",
      "image": "GFX/colors/cherry_blossom_pink.png"
    },
    {
      "furigana": "れんがいろ",
      "kanji": "煉瓦色",
      "translation": "brick red",
      "image": "GFX/colors/brick_red.png"
    },
    {
      "furigana": "おうどいろ",
      "kanji": "黄土色",
      "translation": "ochre",
      "image": "GFX/colors/ochre.png"
    },
    {
      "furigana": "とびいろ",
      "kanji": "鳶色",
      "translation": "dark reddish-brown",
      "image": "GFX/colors/dark_reddish_brown.png"
    },
    {
      "furigana": "ぶどういろ",
      "kanji": "葡萄色",
      "translation": "grape color",
      "image": "GFX/colors/grape.png"
    }
  ]
}

j_colors6 = {
  "quiz_title": "Color Sentences 1",
  "questions": [
    {
      "furigana": "あかいねこです",
      "kanji": "赤い猫です",
      "translation": "It is a red cat.",
      "image": "GFX/colors/red.png"
    },
    {
      "furigana": "あおいねこです",
      "kanji": "青い猫です",
      "translation": "It is a blue cat.",
      "image": "GFX/colors/blue.png"
    },
    {
      "furigana": "しろいねこです",
      "kanji": "白い猫です",
      "translation": "It is a white cat.",
      "image": "GFX/colors/white.png"
    },
    {
      "furigana": "くろいねこです",
      "kanji": "黒い猫です",
      "translation": "It is a black cat.",
      "image": "GFX/colors/black.png"
    },
    {
      "furigana": "みどりのねこです",
      "kanji": "緑の猫です",
      "translation": "It is a green cat.",
      "image": "GFX/colors/green.png"
    }
  ]
}

j_colors7 = {
  "quiz_title": "Color Sentences 2",
  "questions": [
    {
      "furigana": "きいろいねこです",
      "kanji": "黄色い猫です",
      "translation": "It is a yellow cat.",
      "image": "GFX/colors/yellow.png"
    },
    {
      "furigana": "ちゃいろいねこです",
      "kanji": "茶色い猫です",
      "translation": "It is a brown cat.",
      "image": "GFX/colors/brown.png"
    },
    {
      "furigana": "むらさきのねこです",
      "kanji": "紫の猫です",
      "translation": "It is a purple cat.",
      "image": "GFX/colors/purple.png"
    },
    {
      "furigana": "はいいろのねこです",
      "kanji": "灰色の猫です",
      "translation": "It is a gray cat.",
      "image": "GFX/colors/gray.png"
    },
    {
      "furigana": "きんいろのねこです",
      "kanji": "金色の猫です",
      "translation": "It is a gold cat.",
      "image": "GFX/colors/gold.png"
    }
  ]
}

j_colors8 = {
  "quiz_title": "Color Sentences 3",
  "questions": [
    {
      "furigana": "だいだいいろのねこです",
      "kanji": "橙色の猫です",
      "translation": "It is an orange cat.",
      "image": "GFX/colors/orange.png"
    },
    {
      "furigana": "ももいろのねこです",
      "kanji": "桃色の猫です",
      "translation": "It is a pink cat.",
      "image": "GFX/colors/pink.png"
    },
    {
      "furigana": "きんいろのねこです",
      "kanji": "金色の猫です",
      "translation": "It is a gold cat.",
      "image": "GFX/colors/gold.png"
    },
    {
      "furigana": "ぎんいろのねこです",
      "kanji": "銀色の猫です",
      "translation": "It is a silver cat.",
      "image": "GFX/colors/silver.png"
    },
    {
      "furigana": "こんいろのねこです",
      "kanji": "紺色の猫です",
      "translation": "It is a navy blue cat.",
      "image": "GFX/colors/navy_blue.png"
    }
  ]
}

j_colors9 = {
  "quiz_title": "Color Sentences 4",
  "questions": [
    {
      "furigana": "みずいろのねこです",
      "kanji": "水色の猫です",
      "translation": "It is a light blue cat.",
      "image": "GFX/colors/light_blue.png"
    },
    {
      "furigana": "しこうのねこです",
      "kanji": "紫紅の猫です",
      "translation": "It is a crimson cat.",
      "image": "GFX/colors/crimson.png"
    },
    {
      "furigana": "きみどりのねこです",
      "kanji": "黄緑の猫です",
      "translation": "It is a yellow-green cat.",
      "image": "GFX/colors/yellow_green.png"
    },
    {
      "furigana": "わかくさいろのねこです",
      "kanji": "若草色の猫です",
      "translation": "It is a light green cat.",
      "image": "GFX/colors/light_green.png"
    },
    {
      "furigana": "あさぎいろのねこです",
      "kanji": "浅葱色の猫です",
      "translation": "It is a light blue-green cat.",
      "image": "GFX/colors/light_blue_green.png"
    }
  ]
}

j_colors10 = {
  "quiz_title": "Color Sentences 5",
  "questions": [
    {
      "furigana": "さくらいろのねこです",
      "kanji": "桜色の猫です",
      "translation": "It is a cherry blossom pink cat.",
      "image": "GFX/colors/cherry_blossom_pink.png"
    },
    {
      "furigana": "れんがいろのねこです",
      "kanji": "煉瓦色の猫です",
      "translation": "It is a brick red cat.",
      "image": "GFX/colors/brick_red.png"
    },
    {
      "furigana": "おうどいろのねこです",
      "kanji": "黄土色の猫です",
      "translation": "It is an ochre cat.",
      "image": "GFX/colors/ochre.png"
    },
    {
      "furigana": "とびいろのねこです",
      "kanji": "鳶色の猫です",
      "translation": "It is a dark reddish-brown cat.",
      "image": "GFX/colors/dark_reddish_brown.png"
    },
    {
      "furigana": "ぶどういろのねこです",
      "kanji": "葡萄色の猫です",
      "translation": "It is a grape-colored cat.",
      "image": "GFX/colors/grape.png"
    }
  ]
}

j_body_parts1 = {
  "quiz_title": "Body Parts 1",
  "questions": [
    {
      "furigana": "みみ",
      "kanji": "耳",
      "translation": "ear",
      "image": "GFX/body_parts/ear.png"
    },
    {
      "furigana": "くち",
      "kanji": "口",
      "translation": "mouth",
      "image": "GFX/body_parts/mouth.png"
    },
    {
      "furigana": "て",
      "kanji": "手",
      "translation": "hand",
      "image": "GFX/body_parts/hand.png"
    },
    {
      "furigana": "あし",
      "kanji": "足",
      "translation": "foot",
      "image": "GFX/body_parts/foot.png"
    },
    {
      "furigana": "め",
      "kanji": "目",
      "translation": "eye",
      "image": "GFX/body_parts/eye.png"
    }
  ]
}

j_body_parts2 = {
  "quiz_title": "Body Parts 2",
  "questions": [
    {
      "furigana": "あたま",
      "kanji": "頭",
      "translation": "head",
      "image": "GFX/body_parts/head.png"
    },
    {
      "furigana": "はな",
      "kanji": "鼻",
      "translation": "nose",
      "image": "GFX/body_parts/nose.png"
    },
    {
      "furigana": "かみ",
      "kanji": "髪",
      "translation": "hair",
      "image": "GFX/body_parts/hair.png"
    },
    {
      "furigana": "かお",
      "kanji": "顔",
      "translation": "face",
      "image": "GFX/body_parts/face.png"
    },
    {
      "furigana": "ゆび",
      "kanji": "指",
      "translation": "finger",
      "image": "GFX/body_parts/finger.png"
    }
  ]
}

j_body_parts3 = {
  "quiz_title": "Body Parts 3",
  "questions": [
    {
      "furigana": "かた",
      "kanji": "肩",
      "translation": "shoulder",
      "image": "GFX/body_parts/shoulder.png"
    },
    {
      "furigana": "ひじ",
      "kanji": "",
      "translation": "elbow",
      "image": "GFX/body_parts/elbow.png"
    },
    {
      "furigana": "ひざ",
      "kanji": "",
      "translation": "knee",
      "image": "GFX/body_parts/knee.png"
    },
    {
      "furigana": "むね",
      "kanji": "胸",
      "translation": "chest",
      "image": "GFX/body_parts/chest.png"
    },
    {
      "furigana": "せなか",
      "kanji": "背中",
      "translation": "back",
      "image": "GFX/body_parts/back.png"
    }
  ]
}

j_body_parts4 = {
  "quiz_title": "Body Parts 4",
  "questions": [
    {
      "furigana": "くび",
      "kanji": "首",
      "translation": "neck",
      "image": "GFX/body_parts/neck.png"
    },
    {
      "furigana": "おなか",
      "kanji": "お腹",
      "translation": "stomach",
      "image": "GFX/body_parts/stomach.png"
    },
    {
      "furigana": "こし",
      "kanji": "腰",
      "translation": "waist",
      "image": "GFX/body_parts/waist.png"
    },
    {
      "furigana": "うで",
      "kanji": "腕",
      "translation": "arm",
      "image": "GFX/body_parts/arm.png"
    },
    {
      "furigana": "あご",
      "kanji": "顔",
      "translation": "chin",
      "image": "GFX/body_parts/chin.png"
    }
  ]
}

j_body_parts5 = {
  "quiz_title": "Body Parts 5",
  "questions": [
    {
      "furigana": "ほほ",
      "kanji": "",
      "translation": "cheek",
      "image": "GFX/body_parts/cheek.png"
    },
    {
      "furigana": "あごひげ",
      "kanji": "",
      "translation": "beard",
      "image": "GFX/body_parts/beard.png"
    },
    {
      "furigana": "まゆげ",
      "kanji": "",
      "translation": "eyebrow",
      "image": "GFX/body_parts/eyebrow.png"
    },
    {
      "furigana": "まつげ",
      "kanji": "",
      "translation": "eyelash",
      "image": "GFX/body_parts/eyelash.png"
    },
    {
      "furigana": "くちびる",
      "kanji": "",
      "translation": "lip",
      "image": "GFX/body_parts/lip.png"
    }
  ]
}

j_adjectives1 = {
  "quiz_title": "Simple Adjectives",
  "questions": [
    {
      "furigana": "おおきい",
      "kanji": "大きい",
      "translation": "large",
      "image": "GFX/adjectives/large.png"
    },
    {
      "furigana": "ちいさい",
      "kanji": "小さい",
      "translation": "small",
      "image": "GFX/adjectives/small.png"
    },
    {
      "furigana": "ながい",
      "kanji": "長い",
      "translation": "long",
      "image": "GFX/adjectives/long.png"
    },
    {
      "furigana": "みじかい",
      "kanji": "短い",
      "translation": "short",
      "image": "GFX/adjectives/short.png"
    },
    {
      "furigana": "はやい",
      "kanji": "速い",
      "translation": "fast",
      "image": "GFX/adjectives/fast.png"
    }
  ]
}

j_animals1 = {
  "quiz_title": "Animals",
  "questions": [
    {
      "kanji": "犬",
      "furigana": "いぬ",
      "translation": "dog",
      "image": "GFX/animals/dog.png"
    },
    {
      "kanji": "猫",
      "furigana": "ねこ",
      "translation": "cat",
      "image": "GFX/animals/cat.png"
    },
    {
      "kanji": "象",
      "furigana": "ぞう",
      "translation": "elephant",
      "image": "GFX/animals/elephant.png"
    },
    {
      "kanji": "魚",
      "furigana": "さかな",
      "translation": "fish",
      "image": "GFX/animals/fish.png"
    },
    {
      "kanji": "鶏",
      "furigana": "にわとり",
      "translation": "chicken",
      "image": "GFX/animals/chicken.png"
    }
  ]
}

j_animals2 = {
  "quiz_title": "Animals 2",
  "questions": [
    {
      "kanji": "馬",
      "furigana": "うま",
      "translation": "horse",
      "image": "GFX/animals/horse.png"
    },
    {
      "kanji": "鳥",
      "furigana": "とり",
      "translation": "bird",
      "image": "GFX/animals/bird.png"
    },
    {
      "kanji": "牛",
      "furigana": "うし",
      "translation": "cow",
      "image": "GFX/animals/cow.png"
    },
    {
      "kanji": "豚",
      "furigana": "ぶた",
      "translation": "pig",
      "image": "GFX/animals/pig.png"
    },
    {
      "kanji": "狐",
      "furigana": "きつね",
      "translation": "fox",
      "image": "GFX/animals/fox.png"
    }
  ]
}

j_animals3 = {
  "quiz_title": "Animals 3",
  "questions": [
    {
      "kanji": "亀",
      "furigana": "かめ",
      "translation": "turtle",
      "image": "GFX/animals/turtle.png"
    },
    {
      "kanji": "狼",
      "furigana": "おおかみ",
      "translation": "wolf",
      "image": "GFX/animals/wolf.png"
    },
    {
      "kanji": "鼠",
      "furigana": "ねずみ",
      "translation": "mouse/rat",
      "image": "GFX/animals/mouse.png"
    },
    {
      "kanji": "蛇",
      "furigana": "へび",
      "translation": "snake",
      "image": "GFX/animals/snake.png"
    },
    {
      "kanji": "鴨",
      "furigana": "かも",
      "translation": "duck",
      "image": "GFX/animals/duck.png"
    }
  ]
}

j_animals4 = {
  "quiz_title": "Animals 4",
  "questions": [
    {
      "kanji": "虎",
      "furigana": "とら",
      "translation": "tiger",
      "image": "GFX/animals/tiger.png"
    },
    {
      "kanji": "豹",
      "furigana": "ひょう",
      "translation": "leopard",
      "image": "GFX/animals/leopard.png"
    },
    {
      "kanji": "キリン",
      "furigana": "きりん",
      "translation": "giraffe",
      "image": "GFX/animals/giraffe.png"
    },
    {
      "kanji": "ラクダ",
      "furigana": "らくだ",
      "translation": "camel",
      "image": "GFX/animals/camel.png"
    },
    {
      "kanji": "パンダ",
      "furigana": "ぱんだ",
      "translation": "panda",
      "image": "GFX/animals/panda.png"
    }
  ]
}

j_animals5 = {
  "quiz_title": "Animals 5",
  "questions": [
    {
      "kanji": "ゴリラ",
      "furigana": "ごりら",
      "translation": "gorilla",
      "image": "GFX/animals/gorilla.png"
    },
    {
      "kanji": "ペンギン",
      "furigana": "ぺんぎん",
      "translation": "penguin",
      "image": "GFX/animals/penguin.png"
    },
    {
      "kanji": "シマウマ",
      "furigana": "しまうま",
      "translation": "zebra",
      "image": "GFX/animals/zebra.png"
    },
    {
      "kanji": "ハリネズミ",
      "furigana": "はりねずみ",
      "translation": "hedgehog",
      "image": "GFX/animals/hedgehog.png"
    },
    {
      "kanji": "イルカ",
      "furigana": "いるか",
      "translation": "dolphin",
      "image": "GFX/animals/dolphin.png"
    }
  ]
}

j_animals6 = {
  "quiz_title": "Animals 6",
  "questions": [
    {
      "kanji": "獅子",
      "furigana": "ライオン",
      "translation": "lion",
      "image": "GFX/animals/lion.png"
    },
    {
      "kanji": "烏",
      "furigana": "からす",
      "translation": "crow",
      "image": "GFX/animals/crow.png"
    },
    {
      "kanji": "鯨",
      "furigana": "くじら",
      "translation": "whale",
      "image": "GFX/animals/whale.png"
    },
    {
      "kanji": "烏賊",
      "furigana": "イカ",
      "translation": "squid",
      "image": "GFX/animals/squid.png"
    },
    {
      "kanji": "蛸",
      "furigana": "タコ",
      "translation": "octopus",
      "image": "GFX/animals/octopus.png"
    }
  ]
}

j_animals7 = {
  "quiz_title": "Animals 7",
  "questions": [
    {
      "kanji": "羊",
      "furigana": "ひつじ",
      "translation": "sheep",
      "image": "GFX/animals/sheep.png"
    },
    {
      "kanji": "鹿",
      "furigana": "しか",
      "translation": "deer",
      "image": "GFX/animals/deer.png"
    },
    {
      "kanji": "熊",
      "furigana": "くま",
      "translation": "bear",
      "image": "GFX/animals/bear.png"
    },
    {
      "kanji": "猿",
      "furigana": "さる",
      "translation": "monkey",
      "image": "GFX/animals/monkey.png"
    },
    {
      "kanji": "兎",
      "furigana": "うさぎ",
      "translation": "rabbit",
      "image": "GFX/animals/rabbit.png"
    }
  ]
}

j_animals8 = {
  "quiz_title": "Animals 8",
  "questions": [
    {
      "kanji": "カバ",
      "furigana": "かば",
      "translation": "hippopotamus",
      "image": "GFX/animals/hippopotamus.png"
    },
    {
      "kanji": "ワニ",
      "furigana": "わに",
      "translation": "crocodile",
      "image": "GFX/animals/crocodile.png"
    },
    {
      "kanji": "鷹",
      "furigana": "たか",
      "translation": "hawk",
      "image": "GFX/animals/hawk.png"
    },
    {
      "kanji": "フクロウ",
      "furigana": "ふくろう",
      "translation": "owl",
      "image": "GFX/animals/owl.png"
    },
    {
      "kanji": "コアラ",
      "furigana": "こあら",
      "translation": "koala",
      "image": "GFX/animals/koala.png"
    }
  ]
}

j_animals9 = {
  "quiz_title": "Animals 9",
  "questions": [
    {
      "kanji": "リス",
      "furigana": "りす",
      "translation": "squirrel",
      "image": "GFX/animals/squirrel.png"
    },
    {
      "kanji": "ハムスター",
      "furigana": "はむすたー",
      "translation": "hamster",
      "image": "GFX/animals/hamster.png"
    },
    {
      "kanji": "蟻",
      "furigana": "あり",
      "translation": "ant",
      "image": "GFX/animals/ant.png"
    },
    {
      "kanji": "蜂",
      "furigana": "はち",
      "translation": "bee",
      "image": "GFX/animals/bee.png"
    },
    {
      "kanji": "蛙",
      "furigana": "かえる",
      "translation": "frog",
      "image": "GFX/animals/frog.png"
    }
  ]
}

j_family1 = {
  "quiz_title": "Family Relations",
  "questions": [
    {
      "furigana": "はは",
      "kanji": "母",
      "translation": "my mother",
      "image": "GFX/family/mother.png"
    },
    {
      "furigana": "ちち",
      "kanji": "父",
      "translation": "my father",
      "image": "GFX/family/father.png"
    },
    {
      "furigana": "あに",
      "kanji": "兄",
      "translation": "my older brother",
      "image": "GFX/family/older_brother.png"
    },
    {
      "furigana": "おとうと",
      "kanji": "弟",
      "translation": "my younger brother",
      "image": "GFX/family/younger_brother.png"
    },
    {
      "furigana": "あね",
      "kanji": "姉",
      "translation": "my older sister",
      "image": "GFX/family/older_sister.png"
    },
    {
      "furigana": "いもうと",
      "kanji": "妹",
      "translation": "my younger sister",
      "image": "GFX/family/younger_sister.png"
    }
  ]
}

j_family2 = {
  "quiz_title": "Family Relations - Out-Group",
  "questions": [
    {
      "furigana": "おかあさん",
      "kanji": "お母さん",
      "translation": "your mother",
      "image": "GFX/family/mother.png"
    },
    {
      "furigana": "おとうさん",
      "kanji": "お父さん",
      "translation": "your father",
      "image": "GFX/family/father.png"
    },
    {
      "furigana": "おにいさん",
      "kanji": "お兄さん",
      "translation": "your older brother",
      "image": "GFX/family/older_brother.png"
    },
    {
      "furigana": "おとうとさん",
      "kanji": "弟さん",
      "translation": "your younger brother",
      "image": "GFX/family/younger_brother.png"
    },
    {
      "furigana": "おねえさん",
      "kanji": "お姉さん",
      "translation": "your older sister",
      "image": "GFX/family/older_sister.png"
    },
    {
      "furigana": "いもうとさん",
      "kanji": "妹さん",
      "translation": "your younger sister",
      "image": "GFX/family/younger_sister.png"
    }
  ]
}

j_family3 = {
  "quiz_title": "Family Relations 2",
  "questions": [
    {
      "furigana": "そふ",
      "kanji": "祖父",
      "translation": "my grandfather",
      "image": "GFX/family/grandfather.png"
    },
    {
      "furigana": "そぼ",
      "kanji": "祖母",
      "translation": "my grandmother",
      "image": "GFX/family/grandmother.png"
    },
    {
      "furigana": "おじ",
      "kanji": "叔父",
      "translation": "my uncle",
      "image": "GFX/family/uncle.png"
    },
    {
      "furigana": "おば",
      "kanji": "叔母",
      "translation": "my aunt",
      "image": "GFX/family/aunt.png"
    },
    {
      "furigana": "いとこ",
      "kanji": "従兄弟",
      "translation": "my cousin",
      "image": "GFX/family/cousin.png"
    }
  ]
}

j_family4 = {
  "quiz_title": "Family Relationships 2 - Outgroup",
  "questions": [
    {
      "furigana": "おじいさん",
      "kanji": "お祖父さん",
      "translation": "your grandfather",
      "image": "GFX/family/grandfather.png"
    },
    {
      "furigana": "おばあさん",
      "kanji": "お祖母さん",
      "translation": "your grandmother",
      "image": "GFX/family/grandmother.png"
    },
    {
      "furigana": "おじさん",
      "kanji": "叔父さん",
      "translation": "your uncle",
      "image": "GFX/family/uncle.png"
    },
    {
      "furigana": "おばさん",
      "kanji": "叔母さん",
      "translation": "your aunt",
      "image": "GFX/family/aunt.png"
    },
    {
      "furigana": "いとこさん",
      "kanji": "従兄弟さん",
      "translation": "your cousin",
      "image": "GFX/family/cousin.png"
    }
  ]
}

# Note: family relation 3 out group is the same as in group
j_family5 = {
  "quiz_title": "Family Relations 3",
  "questions": [
    {
      "furigana": "そうそふ",
      "kanji": "曽祖父",
      "translation": "my great-grandfather",
      "image": "GFX/family/great_grandfather.png"
    },
    {
      "furigana": "そうそぼ",
      "kanji": "曽祖母",
      "translation": "my great-grandmother",
      "image": "GFX/family/great_grandmother.png"
    },
    {
      "furigana": "ぎふ",
      "kanji": "義父",
      "translation": "my father-in-law",
      "image": "GFX/family/father_in_law.png"
    },
    {
      "furigana": "ぎぼ",
      "kanji": "義母",
      "translation": "my mother-in-law",
      "image": "GFX/family/mother_in_law.png"
    },
    {
      "furigana": "ぎけい",
      "kanji": "義兄",
      "translation": "my older brother-in-law",
      "image": "GFX/family/older_brother_in_law.png"
    },
    {
      "furigana": "ぎてい",
      "kanji": "義弟",
      "translation": "my younger brother-in-law",
      "image": "GFX/family/younger_brother_in_law.png"
    }
  ]
}

j_family6 = {
  "quiz_title": "Family Relations - 4",
  "questions": [
    {
      "furigana": "ぎし",
      "kanji": "義姉",
      "translation": "my older sister-in-law",
      "image": "GFX/family/older_sister_in_law.png"
    },
    {
      "furigana": "ぎまい",
      "kanji": "義妹",
      "translation": "my younger sister-in-law",
      "image": "GFX/family/younger_sister_in_law.png"
    },
    {
      "furigana": "おい",
      "kanji": "甥",
      "translation": "my nephew",
      "image": "GFX/family/nephew.png"
    },
    {
      "furigana": "めい",
      "kanji": "姪",
      "translation": "my niece",
      "image": "GFX/family/niece.png"
    },
    {
      "furigana": "おっと",
      "kanji": "夫",
      "translation": "my husband",
      "image": "GFX/family/husband.png"
    },
    {
      "furigana": "つま",
      "kanji": "妻",
      "translation": "my wife",
      "image": "GFX/family/wife.png"
    }
  ]
}

j_family7 = {
  "quiz_title": "Family Relations 4 - Out Group",
  "questions": [
    {
      "furigana": "おねえさん",
      "kanji": "お姉さん",
      "translation": "your older sister-in-law",
      "image": "GFX/family/older_sister_in_law.png"
    },
    {
      "furigana": "いもうとさん",
      "kanji": "妹さん",
      "translation": "your younger sister-in-law",
      "image": "GFX/family/younger_sister_in_law.png"
    },
    {
      "furigana": "おいごさん",
      "kanji": "甥御さん",
      "translation": "your nephew",
      "image": "GFX/family/nephew.png"
    },
    {
      "furigana": "めいごさん",
      "kanji": "姪御さん",
      "translation": "your niece",
      "image": "GFX/family/niece.png"
    },
    {
      "furigana": "ごしゅじん",
      "kanji": "ご主人",
      "translation": "your husband",
      "image": "GFX/family/husband.png"
    },
    {
      "furigana": "おくさん",
      "kanji": "奥さん",
      "translation": "your wife",
      "image": "GFX/family/wife.png"
    }
  ]
}

j_fruits1 = {
  "quiz_title": "Fruits",
  "questions": [
    {
      "kanji": "りんご",
      "furigana": "りんご",
      "translation": "apple",
      "image": "GFX/fruits/apple.png"
    },
    {
      "kanji": "みかん",
      "furigana": "みかん",
      "translation": "mandarin orange",
      "image": "GFX/fruits/mandarin_orange.png"
    },
    {
      "kanji": "ぶどう",
      "furigana": "ぶどう",
      "translation": "grape",
      "image": "GFX/fruits/grape.png"
    },
    {
      "kanji": "もも",
      "furigana": "もも",
      "translation": "peach",
      "image": "GFX/fruits/peach.png"
    },
    {
      "kanji": "柿",
      "furigana": "かき",
      "translation": "persimmon",
      "image": "GFX/fruits/persimmon.png"
    }
  ]
}

j_fruits2 = {
  "quiz_title": "Fruits 2",
  "questions": [
    {
      "kanji": "梨",
      "furigana": "なし",
      "translation": "pear",
      "image": "GFX/fruits/pear.png"
    },
    {
      "kanji": "スイカ",
      "furigana": "スイカ",
      "translation": "watermelon",
      "image": "GFX/fruits/watermelon.png"
    },
    {
      "kanji": "メロン",
      "furigana": "メロン",
      "translation": "melon",
      "image": "GFX/fruits/melon.png"
    },
    {
      "kanji": "バナナ",
      "furigana": "バナナ",
      "translation": "banana",
      "image": "GFX/fruits/banana.png"
    },
    {
      "kanji": "苺",
      "furigana": "いちご",
      "translation": "strawberry",
      "image": "GFX/fruits/strawberry.png"
    }
  ]
}

j_fruits3 = {
  "quiz_title": "Fruits 3",
  "questions": [
    {
      "kanji": "キウイ",
      "furigana": "キウイ",
      "translation": "kiwi",
      "image": "GFX/fruits/kiwi.png"
    },
    {
      "kanji": "パイナップル",
      "furigana": "パイナップル",
      "translation": "pineapple",
      "image": "GFX/fruits/pineapple.png"
    },
    {
      "kanji": "さくらんぼ",
      "furigana": "さくらんぼ",
      "translation": "cherry",
      "image": "GFX/fruits/cherry.png"
    },
    {
      "kanji": "柚子",
      "furigana": "ゆず",
      "translation": "yuzu",
      "image": "GFX/fruits/yuzu.png"
    },
    {
      "kanji": "ブルーベリー",
      "furigana": "ブルーベリー",
      "translation": "blueberry",
      "image": "GFX/fruits/blueberry.png"
    }
  ]
}

j_fruits4 = {
  "quiz_title": "Fruits 4",
  "questions": [
    {
      "kanji": "ライチ",
      "furigana": "ライチ",
      "translation": "lychee",
      "image": "GFX/fruits/lychee.png"
    },
    {
      "kanji": "アンズ",
      "furigana": "アンズ",
      "translation": "apricot",
      "image": "GFX/fruits/apricot.png"
    },
    {
      "kanji": "梅",
      "furigana": "うめ",
      "translation": "plum",
      "image": "GFX/fruits/plum.png"
    },
    {
      "kanji": "グレープフルーツ",
      "furigana": "グレープフルーツ",
      "translation": "grapefruit",
      "image": "GFX/fruits/grapefruit.png"
    },
    {
      "kanji": "ドラゴンフルーツ",
      "furigana": "ドラゴンフルーツ",
      "translation": "dragon fruit",
      "image": "GFX/fruits/dragon_fruit.png"
    }
  ]
}

j_fruits5 = {
  "quiz_title": "Fruits 5",
  "questions": [
    {
      "kanji": "パッションフルーツ",
      "furigana": "パッションフルーツ",
      "translation": "passion fruit",
      "image": "GFX/fruits/passion_fruit.png"
    },
    {
      "kanji": "いちじく",
      "furigana": "いちじく",
      "translation": "fig",
      "image": "GFX/fruits/fig.png"
    },
    {
      "kanji": "ザクロ",
      "furigana": "ザクロ",
      "translation": "pomegranate",
      "image": "GFX/fruits/pomegranate.png"
    },
    {
      "kanji": "びわ",
      "furigana": "びわ",
      "translation": "loquat",
      "image": "GFX/fruits/loquat.png"
    },
    {
      "kanji": "マンゴー",
      "furigana": "マンゴー",
      "translation": "mango",
      "image": "GFX/fruits/mango.png"
    }
  ]
}

j_greetings1 = {
  "quiz_title": "Greetings",
  "questions": [
    {
      "kanji": "お早う",
      "furigana": "おはよう",
      "translation": "Good morning",
      "image": ""
    },
    {
      "kanji": "今日は",
      "furigana": "こんにちは",
      "translation": "Good day",
      "image": ""
    },
    {
      "kanji": "今晩は",
      "furigana": "こんばんは",
      "translation": "Good evening",
      "image": ""
    },
    {
      "kanji": "お休み",
      "furigana": "おやすみ",
      "translation": "Good night",
      "image": ""
    },
    {
      "kanji": "頂きます",
      "furigana": "いただきます",
      "translation": "I humbly receive",
      "image": ""
    }
  ]
}

j_greetings2 = {
  "quiz_title": "Greetings 2",
  "questions": [
    {
      "kanji": "有難う",
      "furigana": "ありがとう",
      "translation": "Thank you",
      "image": ""
    },
    {
      "kanji": "さようなら",
      "furigana": "さようなら",
      "translation": "Goodbye",
      "image": ""
    },
    {
      "kanji": "お疲れ様",
      "furigana": "おつかれさま",
      "translation": "Thank you for your hard work",
      "image": ""
    },
    {
      "kanji": "行ってきます",
      "furigana": "いってきます",
      "translation": "I'm off (and will return)",
      "image": ""
    },
    {
      "kanji": "行ってらっしゃい",
      "furigana": "いってらっしゃい",
      "translation": "Please go and come back",
      "image": ""
    }
  ]
}

j_greetings3 = {
  "quiz_title": "Greetings 3",
  "questions": [
    {
      "kanji": "ただいま",
      "furigana": "ただいま",
      "translation": "I'm home",
      "image": ""
    },
    {
      "kanji": "お帰り",
      "furigana": "おかえり",
      "translation": "Welcome back",
      "image": ""
    },
    {
      "kanji": "ご馳走様",
      "furigana": "ごちそうさま",
      "translation": "Thank you for the meal (after eating)",
      "image": ""
    },
    {
      "kanji": "よろしくお願いします",
      "furigana": "よろしくおねがいします",
      "translation": "Please take care of this / Nice to meet you",
      "image": ""
    },
    {
      "kanji": "お元気ですか",
      "furigana": "おげんきですか",
      "translation": "How are you?",
      "image": ""
    }
  ]
}

j_one_piece1 = {
  "quiz_title": "One Piece",
  "questions": [
    {
      "furigana": "かいぞく",
      "kanji": "海賊",
      "translation": "pirate",
      "image": "GFX/one_piece/pirate.png"
    },
    {
      "furigana": "ふね",
      "kanji": "船",
      "translation": "ship",
      "image": "GFX/one_piece/ship.png"
    },
    {
      "furigana": "うみ",
      "kanji": "海",
      "translation": "ocean",
      "image": "GFX/one_piece/ocean.png"
    },
    {
      "furigana": "しま",
      "kanji": "島",
      "translation": "island",
      "image": "GFX/one_piece/island.png"
    },
    {
      "furigana": "ちず",
      "kanji": "地図",
      "translation": "map",
      "image": "GFX/one_piece/map.png"
    }
  ]
}

j_one_piece2 = {
  "quiz_title": "One Piece 2",
  "questions": [
    {
      "furigana": "たから",
      "kanji": "宝",
      "translation": "treasure",
      "image": "GFX/one_piece/treasure.png"
    },
    {
      "furigana": "ぼうけん",
      "kanji": "冒険",
      "translation": "adventure",
      "image": "GFX/one_piece/adventure.png"
    },
    {
      "furigana": "けん",
      "kanji": "剣",
      "translation": "sword",
      "image": "GFX/one_piece/sword.png"
    },
    {
      "furigana": "おれ",
      "kanji": "俺",
      "translation": "I/me (casual/rude)",
      "image": "GFX/one_piece/ore.png"
    },
    {
      "furigana": "まったく",
      "kanji": "全く",
      "translation": "jeez",
      "image": "GFX/one_piece/mattaku.png"
    }
  ]
}

j_one_piece3 = {
  "quiz_title": "One Piece 3",
  "questions": [
    {
      "furigana": "せんちょう",
      "kanji": "船長",
      "translation": "captain",
      "image": "GFX/one_piece/captain.png"
    },
    {
      "furigana": "のりくみいん",
      "kanji": "乗組員",
      "translation": "crew",
      "image": "GFX/one_piece/crew.png"
    },
    {
      "furigana": "なかま",
      "kanji": "仲間",
      "translation": "friend/companion",
      "image": "GFX/one_piece/friend.png"
    },
    {
      "furigana": "かいぐん",
      "kanji": "海軍",
      "translation": "navy",
      "image": "GFX/one_piece/navy.png"
    },
    {
      "furigana": "あくまのみ",
      "kanji": "悪魔の実",
      "translation": "Devil Fruit",
      "image": "GFX/one_piece/devil_fruit.png"
    }
  ]
}

j_one_piece4 = {
  "quiz_title": "One Piece 4",
  "questions": [
    {
      "furigana": "せんい",
      "kanji": "船医",
      "translation": "ship doctor",
      "image": "GFX/one_piece/ship_doctor.png"
    },
    {
      "furigana": "けんし",
      "kanji": "剣士",
      "translation": "swordsman",
      "image": "GFX/one_piece/swordsman.png"
    },
    {
      "furigana": "かいぞくおう",
      "kanji": "海賊王",
      "translation": "Pirate King",
      "image": "GFX/one_piece/pirate_king.png"
    },
    {
      "furigana": "ぼうけんしゃ",
      "kanji": "冒険者",
      "translation": "adventurer",
      "image": "GFX/one_piece/adventurer.png"
    },
    {
      "furigana": "たからのちず",
      "kanji": "宝の地図",
      "translation": "treasure map",
      "image": "GFX/one_piece/treasure_map.png"
    }
  ]
}

j_self_introduction1 = {
  "quiz_title": "Self-Introduction Vocabulary",
  "questions": [
    {
      "kanji": "私",
      "furigana": "わたし",
      "translation": "I (formal/polite)",
      "image": ""
    },
    {
      "kanji": "の",
      "furigana": "の",
      "translation": "possessive particle",
      "image": ""
    },
    {
      "kanji": "名前",
      "furigana": "なまえ",
      "translation": "name",
      "image": ""
    },
    {
      "kanji": "は",
      "furigana": "は",
      "translation": "topic marker particle",
      "image": ""
    },
    {
      "kanji": "です",
      "furigana": "です",
      "translation": "is/are",
      "image": ""
    },
    {
      "kanji": "から",
      "furigana": "から",
      "translation": "from",
      "image": ""
    }
  ]
}

j_self_introduction2 = {
  "quiz_title": "Self-Introduction Vocabulary",
  "questions": [
    {
      "kanji": "来ました",
      "furigana": "きました",
      "translation": "came (from)",
      "image": ""
    },
    {
      "kanji": "歳",
      "furigana": "さい",
      "translation": "years old",
      "image": ""
    },
    {
      "kanji": "趣味",
      "furigana": "しゅみ",
      "translation": "hobby",
      "image": ""
    },
    {
      "kanji": "どうぞ",
      "furigana": "どうぞ",
      "translation": "please",
      "image": ""
    },
    {
      "kanji": "よろしく",
      "furigana": "よろしく",
      "translation": "well",
      "image": ""
    },
    {
      "kanji": "お願いします",
      "furigana": "おねがいします",
      "translation": "please (polite request)",
      "image": ""
    }
  ]
}

j_self_introduction3 = {
  "quiz_title": "Self-Introduction",
  "questions": [
    {
      "kanji": "私の名前は___です",
      "furigana": "わたしのなまえは___です",
      "translation": "My name is ___",
      "image": ""
    },
    {
      "kanji": "___から来ました",
      "furigana": "___からきました",
      "translation": "I am from ___",
      "image": ""
    },
    {
      "kanji": "___歳です",
      "furigana": "___さいです",
      "translation": "I am ___ years old",
      "image": ""
    },
    {
      "kanji": "趣味は___です",
      "furigana": "しゅみは___です",
      "translation": "My hobby is ___",
      "image": ""
    },
    {
      "kanji": "どうぞよろしくお願いします",
      "furigana": "どうぞよろしくおねがいします",
      "translation": "Please take care of me / Nice to meet you",
      "image": ""
    }
  ]
}

j_self_introduction4 = {
  "quiz_title": "Self-Introduction 2 Vocabulary",
  "questions": [
    {
      "kanji": "住んでいます",
      "furigana": "すんでいます",
      "translation": "live (currently living)",
      "image": ""
    },
    {
      "kanji": "に",
      "furigana": "に",
      "translation": "location particle (in, at)",
      "image": ""
    },
    {
      "kanji": "で",
      "furigana": "で",
      "translation": "location particle (at, in; used for actions)",
      "image": ""
    },
    {
      "kanji": "働いています",
      "furigana": "はたらいています",
      "translation": "working (currently working)",
      "image": ""
    },
    {
      "kanji": "勉強しています",
      "furigana": "べんきょうしています",
      "translation": "studying (currently studying)",
      "image": ""
    }
  ]
}

j_self_introduction5 = {
  "quiz_title": "Self-Introduction 2 Vocabulary",
  "questions": [
    {
      "kanji": "家族",
      "furigana": "かぞく",
      "translation": "family",
      "image": ""
    },
    {
      "kanji": "人",
      "furigana": "にん",
      "translation": "people (counter for people)",
      "image": ""
    },
    {
      "kanji": "好きな",
      "furigana": "すきな",
      "translation": "favorite, liked",
      "image": ""
    },
    {
      "kanji": "食べ物",
      "furigana": "たべもの",
      "translation": "food",
      "image": ""
    }
  ]
}

j_self_introduction6 = {
  "quiz_title": "Self-Introduction 2",
  "questions": [
    {
      "kanji": "___に住んでいます",
      "furigana": "___にすんでいます",
      "translation": "I live in ___",
      "image": ""
    },
    {
      "kanji": "___で働いています",
      "furigana": "___ではたらいています",
      "translation": "I work at ___",
      "image": ""
    },
    {
      "kanji": "___を勉強しています",
      "furigana": "___をべんきょうしています",
      "translation": "I am studying ___",
      "image": ""
    },
    {
      "kanji": "家族は___人です",
      "furigana": "かぞくは___にんです",
      "translation": "There are ___ people in my family",
      "image": ""
    },
    {
      "kanji": "好きな食べ物は___です",
      "furigana": "すきなたべものは___です",
      "translation": "My favorite food is ___",
      "image": ""
    }
  ]
}

j_nouns1 = {
  "quiz_title": "Simple Nouns",
  "questions": [
    {
      "furigana": "やま",
      "kanji": "山",
      "translation": "mountain",
      "image": "GFX/nouns/mountain.png"
    },
    {
      "furigana": "かわ",
      "kanji": "川",
      "translation": "river",
      "image": "GFX/nouns/river.png"
    },
    {
      "furigana": "ひ",
      "kanji": "火",
      "translation": "fire",
      "image": "GFX/nouns/fire.png"
    },
    {
      "furigana": "いぬ",
      "kanji": "犬",
      "translation": "dog",
      "image": "GFX/nouns/dog.png"
    },
    {
      "furigana": "ひと",
      "kanji": "人",
      "translation": "person",
      "image": "GFX/nouns/person.png"
    }
  ]
}

j_nouns2 = {
  "quiz_title": "Simple Nouns - Part 2",
  "questions": [
    {
      "furigana": "いと",
      "kanji": "糸",
      "translation": "thread",
      "image": "GFX/nouns/thread.png"
    },
    {
      "furigana": "いし",
      "kanji": "石",
      "translation": "stone",
      "image": "GFX/nouns/stone.png"
    },
    {
      "furigana": "たけ",
      "kanji": "竹",
      "translation": "bamboo",
      "image": "GFX/nouns/bamboo.png"
    },
    {
      "furigana": "かい",
      "kanji": "貝",
      "translation": "shellfish",
      "image": "GFX/nouns/shellfish.png"
    },
    {
      "furigana": "くるま",
      "kanji": "車",
      "translation": "vehicle",
      "image": "GFX/nouns/vehicle.png"
    }
  ]
}

j_nouns3 = {
  "quiz_title": "Simple Nouns - Part 3",
  "questions": [
    {
      "furigana": "きん",
      "kanji": "金",
      "translation": "gold",
      "image": "GFX/nouns/gold_money.png"
    },
    {
      "furigana": "あめ",
      "kanji": "雨",
      "translation": "rain",
      "image": "GFX/nouns/rain.png"
    },
    {
      "furigana": "つき",
      "kanji": "月",
      "translation": "moon",
      "image": "GFX/nouns/moon.png"
    },
    {
      "furigana": "ひ",
      "kanji": "日",
      "translation": "sun",
      "image": "GFX/nouns/sun.png"
    },
    {
      "furigana": "みず",
      "kanji": "水",
      "translation": "water",
      "image": "GFX/nouns/water.png"
    },
    {
      "furigana": "つち",
      "kanji": "土",
      "translation": "earth",
      "image": "GFX/nouns/earth.png"
    }
  ]
}

j_nouns4 = {
  "quiz_title": "Simple Nouns 4",
  "questions": [
    {
      "furigana": "き",
      "kanji": "木",
      "translation": "tree",
      "image": "GFX/nouns/tree.png"
    },
    {
      "furigana": "た",
      "kanji": "田",
      "translation": "rice field",
      "image": "GFX/nouns/rice_field.png"
    },
    {
      "furigana": "はな",
      "kanji": "花",
      "translation": "flower",
      "image": "GFX/nouns/flower.png"
    },
    {
      "furigana": "むし",
      "kanji": "虫",
      "translation": "insect",
      "image": "GFX/nouns/insect.png"
    },
    {
      "furigana": "こ",
      "kanji": "子",
      "translation": "child",
      "image": "GFX/nouns/child.png"
    }
  ]
}

j_time1 = {
  "quiz_title": "Time 1",
  "questions": [
    {
      "furigana": "ことし",
      "kanji": "今年",
      "translation": "this year",
      "image": ""
    },
    {
      "furigana": "ねん",
      "kanji": "年",
      "translation": "year",
      "image": ""
    },
    {
      "furigana": "こんげつ",
      "kanji": "今月",
      "translation": "this month",
      "image": ""
    },
    {
      "furigana": "きょう",
      "kanji": "今日",
      "translation": "today",
      "image": ""
    },
    {
      "furigana": "じ",
      "kanji": "時",
      "translation": "hour",
      "image": ""
    },
    {
      "furigana": "ふん",
      "kanji": "分",
      "translation": "minute",
      "image": ""
    },
    {
      "furigana": "ごぜん",
      "kanji": "午前",
      "translation": "A.M.",
      "image": ""
    }
  ]
}

j_time2 = {
  "quiz_title": "Time 2",
  "questions": [
    {
      "furigana": "こんしゅう",
      "kanji": "今週",
      "translation": "this week",
      "image": ""
    },
    {
      "furigana": "せんしゅう",
      "kanji": "先週",
      "translation": "last week",
      "image": ""
    },
    {
      "furigana": "らいしゅう",
      "kanji": "来週",
      "translation": "next week",
      "image": ""
    },
    {
      "furigana": "せんげつ",
      "kanji": "先月",
      "translation": "last month",
      "image": ""
    },
    {
      "furigana": "らいげつ",
      "kanji": "来月",
      "translation": "next month",
      "image": ""
    }
  ]
}

j_time3 = {
  "quiz_title": "Time 3",
  "questions": [
    {
      "furigana": "きのう",
      "kanji": "昨日",
      "translation": "yesterday",
      "image": ""
    },
    {
      "furigana": "あした",
      "kanji": "明日",
      "translation": "tomorrow",
      "image": ""
    },
    {
      "furigana": "つき",
      "kanji": "月",
      "translation": "month",
      "image": ""
    },
    {
      "furigana": "ひ",
      "kanji": "日",
      "translation": "day",
      "image": ""
    },
    {
      "furigana": "ごご",
      "kanji": "午後",
      "translation": "P.M.",
      "image": ""
    }
  ]
}

j_time4 = {
  "quiz_title": "Time 4",
  "questions": [
    {
      "furigana": "あさって",
      "kanji": "明後日",
      "translation": "the day after tomorrow",
      "image": ""
    },
    {
      "furigana": "おととい",
      "kanji": "一昨日",
      "translation": "the day before yesterday",
      "image": ""
    },
    {
      "furigana": "まいにち",
      "kanji": "毎日",
      "translation": "every day",
      "image": ""
    },
    {
      "furigana": "まいしゅう",
      "kanji": "毎週",
      "translation": "every week",
      "image": ""
    },
    {
      "furigana": "まいつき",
      "kanji": "毎月",
      "translation": "every month",
      "image": ""
    },
    {
      "furigana": "まいとし",
      "kanji": "毎年",
      "translation": "every year",
      "image": ""
    }
  ]
}

j_time5 = {
  "quiz_title": "Time 5",
  "questions": [
    {
      "furigana": "しあさって",
      "kanji": "明明後日",
      "translation": "two days after tomorrow",
      "image": ""
    },
    {
      "furigana": "さきおととい",
      "kanji": "一昨昨日",
      "translation": "three days ago",
      "image": ""
    },
    {
      "furigana": "せんせんしゅう",
      "kanji": "先々週",
      "translation": "the week before last",
      "image": ""
    },
    {
      "furigana": "さらいしゅう",
      "kanji": "再来週",
      "translation": "the week after next",
      "image": ""
    }
  ]
}

j_time6 = {
  "quiz_title": "Time 6",
  "questions": [
    {
      "furigana": "とき",
      "kanji": "時",
      "translation": "time, moment, occasion",
      "image": ""
    },
    {
      "furigana": "じだい",
      "kanji": "時代",
      "translation": "era, period",
      "image": ""
    },
    {
      "furigana": "きかん",
      "kanji": "期間",
      "translation": "period, term, interval",
      "image": ""
    },
    {
      "furigana": "きげん",
      "kanji": "期限",
      "translation": "deadline, time limit",
      "image": ""
    },
    {
      "furigana": "きゅうじつ",
      "kanji": "休日",
      "translation": "holiday, day off",
      "image": ""
    }
  ]
}

j_time7 = {
  "quiz_title": "Time 7",
  "questions": [
    {
      "furigana": "しゅん",
      "kanji": "瞬",
      "translation": "moment",
      "image": ""
    },
    {
      "furigana": "しゅんかん",
      "kanji": "瞬間",
      "translation": "instant",
      "image": ""
    },
    {
      "furigana": "しゅんじ",
      "kanji": "瞬時",
      "translation": "immediate, in an instant",
      "image": ""
    },
    {
      "furigana": "しゅんかんてき",
      "kanji": "瞬間的",
      "translation": "momentary",
      "image": ""
    }
  ]
}

j_vegtables1 = {
  "quiz_title": "Vegetables",
  "questions": [
    {
      "kanji": "大根",
      "furigana": "だいこん",
      "translation": "daikon radish",
      "image": "GFX/vegetables/daikon.png"
    },
    {
      "kanji": "人参",
      "furigana": "にんじん",
      "translation": "carrot",
      "image": "GFX/vegetables/carrot.png"
    },
    {
      "kanji": "キャベツ",
      "furigana": "キャベツ",
      "translation": "cabbage",
      "image": "GFX/vegetables/cabbage.png"
    },
    {
      "kanji": "ほうれん草",
      "furigana": "ほうれんそう",
      "translation": "spinach",
      "image": "GFX/vegetables/spinach.png"
    },
    {
      "kanji": "茄子",
      "furigana": "なす",
      "translation": "eggplant",
      "image": "GFX/vegetables/eggplant.png"
    }
  ]
}

j_vegtables2 = {
  "quiz_title": "Vegetables 2",
  "questions": [
    {
      "kanji": "玉ねぎ",
      "furigana": "たまねぎ",
      "translation": "onion",
      "image": "GFX/vegetables/onion.png"
    },
    {
      "kanji": "じゃがいも",
      "furigana": "じゃがいも",
      "translation": "potato",
      "image": "GFX/vegetables/potato.png"
    },
    {
      "kanji": "ピーマン",
      "furigana": "ピーマン",
      "translation": "green pepper",
      "image": "GFX/vegetables/green_pepper.png"
    },
    {
      "kanji": "白菜",
      "furigana": "はくさい",
      "translation": "napa cabbage",
      "image": "GFX/vegetables/napa_cabbage.png"
    },
    {
      "kanji": "とうもろこし",
      "furigana": "とうもろこし",
      "translation": "corn",
      "image": "GFX/vegetables/corn.png"
    }
  ]
}

j_vegtables3 = {
  "quiz_title": "Vegetables 3",
  "questions": [
    {
      "kanji": "さつまいも",
      "furigana": "さつまいも",
      "translation": "sweet potato",
      "image": "GFX/vegetables/sweet_potato.png"
    },
    {
      "kanji": "しょうが",
      "furigana": "しょうが",
      "translation": "ginger",
      "image": "GFX/vegetables/ginger.png"
    },
    {
      "kanji": "れんこん",
      "furigana": "れんこん",
      "translation": "lotus root",
      "image": "GFX/vegetables/lotus_root.png"
    },
    {
      "kanji": "ネギ",
      "furigana": "ネギ",
      "translation": "green onion",
      "image": "GFX/vegetables/green_onion.png"
    },
    {
      "kanji": "きゅうり",
      "furigana": "きゅうり",
      "translation": "cucumber",
      "image": "GFX/vegetables/cucumber.png"
    }
  ]
}

j_vegtables4 = {
  "quiz_title": "Vegetables 4",
  "questions": [
    {
      "kanji": "ブロッコリー",
      "furigana": "ブロッコリー",
      "translation": "broccoli",
      "image": "GFX/vegetables/broccoli.png"
    },
    {
      "kanji": "カリフラワー",
      "furigana": "カリフラワー",
      "translation": "cauliflower",
      "image": "GFX/vegetables/cauliflower.png"
    },
    {
      "kanji": "アスパラガス",
      "furigana": "アスパラガス",
      "translation": "asparagus",
      "image": "GFX/vegetables/asparagus.png"
    },
    {
      "kanji": "かぼちゃ",
      "furigana": "かぼちゃ",
      "translation": "pumpkin",
      "image": "GFX/vegetables/pumpkin.png"
    },
    {
      "kanji": "ししとう",
      "furigana": "ししとう",
      "translation": "shishito pepper",
      "image": "GFX/vegetables/shishito_pepper.png"
    }
  ]
}

j_vegtables5 = {
  "quiz_title": "Vegetables 5",
  "questions": [
    {
      "kanji": "ごぼう",
      "furigana": "ごぼう",
      "translation": "burdock root",
      "image": "GFX/vegetables/burdock_root.png"
    },
    {
      "kanji": "にんにく",
      "furigana": "にんにく",
      "translation": "garlic",
      "image": "GFX/vegetables/garlic.png"
    },
    {
      "kanji": "さやえんどう",
      "furigana": "さやえんどう",
      "translation": "snow pea",
      "image": "GFX/vegetables/snow_pea.png"
    },
    {
      "kanji": "たけのこ",
      "furigana": "たけのこ",
      "translation": "bamboo shoot",
      "image": "GFX/vegetables/bamboo_shoot.png"
    },
    {
      "kanji": "春菊",
      "furigana": "しゅんぎく",
      "translation": "chrysanthemum greens",
      "image": "GFX/vegetables/chrysanthemum_greens.png"
    }
  ]
}

j_verbs1 = {
  "quiz_title": "Simple Verbs",
  "questions": [
    {
      "furigana": "たべる",
      "kanji": "食べる",
      "translation": "eat",
      "image": "GFX/verbs/eat.png"
    },
    {
      "furigana": "のむ",
      "kanji": "飲む",
      "translation": "drink",
      "image": "GFX/verbs/drink.png"
    },
    {
      "furigana": "みる",
      "kanji": "見る",
      "translation": "look",
      "image": "GFX/verbs/look.png"
    },
    {
      "furigana": "きく",
      "kanji": "聞く",
      "translation": "hear",
      "image": "GFX/verbs/hear.png"
    },
    {
      "furigana": "いう",
      "kanji": "言う",
      "translation": "say",
      "image": "GFX/verbs/say.png"
    }
  ]
}

j_song_sanpo1 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 1a)",
  "questions": [
    {
      "furigana": "あるこう　あるこう",
      "kanji": "歩こう 歩こう",
      "translation": "Let's walk, let's walk",
      "image": ""
    },
    {
      "furigana": "わたしはげんき",
      "kanji": "私は元気",
      "translation": "I'm feeling good",
      "image": ""
    },
    {
      "furigana": "あるくの　だいすき",
      "kanji": "歩くの 大好き",
      "translation": "I love walking",
      "image": ""
    },
    {
      "furigana": "どんどんいこう",
      "kanji": "どんどん行こう",
      "translation": "Let's keep going forward",
      "image": ""
    },
    {
      "furigana": "さかみち　トンネル",
      "kanji": "坂道 トンネル",
      "translation": "Uphill road, tunnel",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo2 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 1b)",
  "questions": [
    {
      "furigana": "くさっぱら",
      "kanji": "草っぱら",
      "translation": "Grassy field",
      "image": ""
    },
    {
      "furigana": "いっぽんばしに",
      "kanji": "一本橋に",
      "translation": "Single log bridge",
      "image": ""
    },
    {
      "furigana": "でこぼこじゃりみち",
      "kanji": "でこぼこ砂利道",
      "translation": "Bumpy gravel path",
      "image": ""
    },
    {
      "furigana": "くものすくぐって",
      "kanji": "蜘蛛の巣くぐって",
      "translation": "Passing through spider webs",
      "image": ""
    },
    {
      "furigana": "くだりみち",
      "kanji": "下り道",
      "translation": "Downhill road",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo3 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 2a)",
  "questions": [
    {
      "furigana": "くりかえし",
      "kanji": "繰り返し",
      "translation": "Repeat",
      "image": ""
    },
    {
      "furigana": "みつばち　ぶんぶん",
      "kanji": "蜜蜂 ブンブン",
      "translation": "Buzzing bees",
      "image": ""
    },
    {
      "furigana": "はなばたけ",
      "kanji": "花畑",
      "translation": "Flower field",
      "image": ""
    },
    {
      "furigana": "ひなたにとかげ",
      "kanji": "日向にトカゲ",
      "translation": "Lizards in the sunlight",
      "image": ""
    },
    {
      "furigana": "へびはひるね",
      "kanji": "蛇は昼寝",
      "translation": "Snake is napping",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo4 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 2b)",
  "questions": [
    {
      "furigana": "ばったがとんで",
      "kanji": "バッタが飛んで",
      "translation": "Grasshoppers flying",
      "image": ""
    },
    {
      "furigana": "まがりみち",
      "kanji": "曲がり道",
      "translation": "Winding road",
      "image": ""
    },
    {
      "furigana": "くりかえし",
      "kanji": "繰り返し",
      "translation": "Repeat",
      "image": ""
    },
    {
      "furigana": "きつねも　たぬきも",
      "kanji": "狐も 狸も",
      "translation": "Foxes and tanuki",
      "image": ""
    },
    {
      "furigana": "でておいで",
      "kanji": "出ておいで",
      "translation": "Come on out",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo5 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 3a)",
  "questions": [
    {
      "furigana": "きつねも　たぬきも",
      "kanji": "狐も 狸も",
      "translation": "Foxes and tanuki",
      "image": ""
    },
    {
      "furigana": "でておいで",
      "kanji": "出ておいで",
      "translation": "Come on out",
      "image": ""
    },
    {
      "furigana": "たんけんしよう",
      "kanji": "探検しよう",
      "translation": "Let's explore",
      "image": ""
    },
    {
      "furigana": "はやしのおくまで",
      "kanji": "林の奥まで",
      "translation": "Deep into the forest",
      "image": ""
    },
    {
      "furigana": "ともだちたくさん",
      "kanji": "友達たくさん",
      "translation": "Lots of friends",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_sanpo6 = {
  "quiz_title": "Japanese Song Lyrics: Sanpo (Part 3b)",
  "questions": [
    {
      "furigana": "うれしいな!",
      "kanji": "嬉しいな!",
      "translation": "I'm so happy!",
      "image": ""
    },
    {
      "furigana": "ともだちたくさん",
      "kanji": "友達たくさん",
      "translation": "Lots of friends",
      "image": ""
    },
    {
      "furigana": "うれしいな!",
      "kanji": "嬉しいな!",
      "translation": "I'm so happy!",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=DoDJX9pPFLY"
}

j_song_zou_san1 = {
  "quiz_title": "Zou-san Vocabulary (Part 1)",
  "questions": [
    {
      "furigana": "ぞうさん",
      "kanji": "象さん",
      "translation": "elephant",
      "image": ""
    },
    {
      "furigana": "おはな",
      "kanji": "お鼻",
      "translation": "nose, trunk",
      "image": ""
    },
    {
      "furigana": "かあさん",
      "kanji": "母さん",
      "translation": "mother",
      "image": ""
    },
    {
      "furigana": "ながい",
      "kanji": "長い",
      "translation": "long",
      "image": ""
    },
    {
      "furigana": "だれ",
      "kanji": "誰",
      "translation": "Who?",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=WguFpvqRSRY"  # Add URL here
}

j_song_zou_san2 = {
  "quiz_title": "Zou-san Vocabulary (Part 2)",
  "questions": [
    {
      "furigana": "すき",
      "kanji": "好き",
      "translation": "like, love",
      "image": ""
    },
    {
      "furigana": "あのね",
      "kanji": "あのね",
      "translation": "well, you see...",
      "image": ""
    },
    {
      "furigana": "そうよ",
      "kanji": "そうよ",
      "translation": "That's right!",
      "image": ""
    }
  ],
  "URL": "https://www.youtube.com/watch?v=WguFpvqRSRY"  # Add URL here
}

# Function to check all variables starting with a prefix and count missing image files
def check_all_image_files(prefix="j_"):
    missing_count = 0  # Initialize a counter for missing assets

    for var_name, data in globals().items():
        if var_name.startswith(prefix) and isinstance(data, dict) and "questions" in data:
            print(f"\nChecking images in: {data['quiz_title']}")
            for question in data["questions"]:
                if question["image"]:  # Skip if image path is empty
                    base_path = question["image"].rsplit('.', 1)[0]  # Remove file extension
                    png_file = f"{base_path}.png"
                    jpg_file = f"{base_path}.jpg"

                    png_exists = os.path.isfile(png_file)
                    jpg_exists = os.path.isfile(jpg_file)

                    # Display which file is found, or if it's missing
                    if not (png_exists or jpg_exists):
                        print(f"Missing file for {question['translation']} (expected at {png_file} or {jpg_file})")
                        missing_count += 1  # Increment the counter if the file is missing
                else:
                    print(f"No image specified for {question['translation']}")

    # Print total number of missing assets at the end
    print(f"\nTotal number of missing art assets: {missing_count}")

# Run the function to check all relevant variables
check_all_image_files()