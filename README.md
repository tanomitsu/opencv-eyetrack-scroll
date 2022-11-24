# 実行環境
## 前提条件
- `poetry`のインストールを前提としています。
- `poetry`を使うことができない場合、`pip`でも可能です。

## 実行準備(パッケージのインストール)
### `poetry`を使う場合
```bash
$ make init
```

### `pip`を使う場合
```bash
$ pip install -r requirements.txt
```

# 実行方法
## `poetry`を使う場合
```bash
$ poetry shell
$ make run
```

## それ以外の場合
```bash
$ make run
```
