# RoleManager
[![LANGUAGE](https://img.shields.io/badge/Python-3.7.3-blue.svg)](https://docs.python.org/3/)

Discord の役職をコマンドで操作できる Bot

## 操作方法

### 役職一覧
- 自分が付与・剥奪できる役職を一覧表示する

```
!role list
```

### 役職を作成
- 鯖で役職管理権限を持っていない人はエラーか帰ってくる
- 作成された役職に権限は一切つかない
- どの役職の上に役職を置くかは環境変数で指定

```
!role create hoge
```

### 役職をつける
- 自分が持っている一番上の役職より下の役職しかいじれない

```
!role get hoge
```

### 役職を剥がす
- 自分が持っている一番上の役職より下の役職しかいじれない

```
!role remove hoge
```

### 役職を削除する
- 鯖で役職管理権限を持っていない人はエラーか帰ってくる

```
!role delete hoge
```

## Dependencies
- [Discord.py](https://github.com/Rapptz/discord.py)

## LICENSE
See [LICENSE](./LICENSE)

Copyright 2019 OldBigBuddha
