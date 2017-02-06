# Rothello
ROSでオセロ
```
├── myled
    ├── scripts
        ├── othello.py: オセロにまつわるクラス
        ├── main_server.py: プレイヤーからの入力を処理するノード
        └── player.py: プレイヤー情報のノード(引数は"p1" or "p2")
```

## 起動方法
三つのターミナルを使用

```Terminal1
$ roscore
$ [ctrl] + [z]
$ rosrun mypkg main_server.py
```

```Terminal2
$ rosrun mypkg player.py p1
$ #ここからは打ちたい盤面の記号をスペースを入れて打つ(例, 3 d)
```

```Terminal3
$ rosrun mypkg player.py p2
$ #ここからは打ちたい盤面の記号をスペースを入れて打つ(例, 3 d)
```

"your turn"と表示されたらあなたの番です

これを用いてコンピュータのノードも作成可能
