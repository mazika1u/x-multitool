# X-MultiTool

[![GitHub](https://img.shields.io/badge/GitHub-mazika1u/x--multitool-blue?logo=github)](https://github.com/mazika1u/x-multitool/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)

**X-MultiTool** は、複数の X (旧Twitter) アカウントを効率的に管理するための Python ライブラリです。非公式APIを利用し、ブラウザ自動化なしでアカウント管理・投稿・リプライなどを簡単に行うことができます。

---

## 📌 特徴

- 複数アカウントを一括管理  
- 投稿・リプライをファイルベースで簡単操作  
- 認証トークンを保存して再ログイン不要  
- バルク投稿やテンプレートリプライに対応  
- ターゲットツイートID管理機能  

---

## ⚙️ 必要環境

- Python 3.10 以上  
- Windows / Linux / MacOS で動作確認済み  
- 推奨: 仮想環境での利用 (`venv` / `conda`)  

---

## 📦 インストール方法

1. リポジトリをクローン

```bash
git clone https://github.com/mazika1u/x-multitool/
cd x-multitool
```

2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

3. 初期設定  
   `config.json` を作成して API キーやアカウント情報を設定できます。  
   （詳しい設定例は下記参照）

---

## 📝 設定例 (`config.json`)

```json
{
  "accounts": [
    {
      "username": "example1",
      "password": "password1",
      "bearer_token": ""
    },
    {
      "username": "example2",
      "password": "password2",
      "bearer_token": ""
    }
  ],
  "default_reply_template": "こんにちは！あなたの投稿を見ました。",
  "log_path": "./logs"
}
```

- `bearer_token` は初回ログイン時に自動生成可能
- `default_reply_template` はリプライのデフォルト文
- `log_path` は操作ログの保存先

---

## 🚀 基本的な使い方

### 1. 投稿 (Tweet)

```python
from x_multitool import XMultiTool

# インスタンス作成
tool = XMultiTool(config_path="config.json")

# 投稿
tool.post("Hello, X from multiple accounts!")
```

- すべてのアカウントで同時投稿可能
- ファイルから読み込んで一括投稿も可

```python
tool.post_from_file("tweets.txt")  # tweets.txt 内の各行を投稿
```

---

### 2. リプライ (Reply)

```python
# 特定のツイートIDにリプライ
tweet_id = "1234567890123456789"
tool.reply(tweet_id, "返信テストです！")
```

- 複数のテンプレートを利用可能
- リプライ対象は `tweet_ids.txt` から一括取得も可

```python
tool.reply_from_file("tweet_ids.txt", "replies.txt")
```

---

### 3. アカウント管理

```python
# アカウント追加
tool.add_account("username", "password")

# 保存されているアカウント一覧
print(tool.list_accounts())
```

- 新規アカウントを追加すると `config.json` に自動反映
- アカウント削除も簡単

```python
tool.remove_account("username")
```

---

### 4. ログとエラー管理

```python
# ログを表示
tool.show_logs()
```

- 投稿・リプライ・エラーをすべてログに記録
- ログの保存先は `config.json` の `log_path` で指定

---

## 📚 応用例

- バルク投稿 & リプライの自動化  
- 定期投稿スケジュールとの組み合わせ  
- 複数アカウントでの統計・管理用スクリプト作成  

```python
# 定期投稿例
import schedule
import time

def job():
    tool.post("毎日の定期投稿テスト")

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## ⚠️ 注意事項

- 非公式APIを使用しているためアカウント停止リスクがあります  
- 商用利用やスパム目的の使用は禁止  
- X の利用規約を守ってください  

---

## 💡 開発者向け

- Python で軽量に設計  
- 拡張可能なモジュール構造  
- ユーザーが自由にテンプレートや機能を追加可能  

---

## 📖 参考リンク

- [公式 GitHub リポジトリ](https://github.com/mazika1u/x-multitool/)  
- [Python 公式サイト](https://www.python.org/)  

---

## ✨ 作者

**mazika1u**  
