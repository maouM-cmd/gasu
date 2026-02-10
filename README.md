# ⛽ ガス料金管理システム

**親御さんの顧客管理を簡単に。検針から請求まで、すべてボタン一つ。**

---

## 📱 このアプリでできること

| 機能 | 説明 |
|---|---|
| **👥 顧客管理** | 顧客の名前、住所、電話番号などを保存 |
| **📏 検針入力** | 毎月のガス検針値を日付付きで記録 |
| **🧮 請求自動生成** | 検針差分から自動で料金を計算して請求を作成 |
| **💰 入金管理** | 誰がいつ払ったか、一目で分かる |
| **📊 一覧表示** | 顧客と請求をシンプルに表示 |

---

## 🎯 最初に試す（初心者向け）

### **方法1️⃣：オンラインで今すぐ試す（推奨！ 最も簡単）**

**セットアップ不要。ブラウザだけあれば OK！**

#### ステップ1：GitHub にログイン
- https://github.com にアクセス
- ない場合は新規登録（30秒）

#### ステップ2：このプロジェクトをコピーする
- [このリンクをクリック](https://github.com/maouM-cmd/gasu/fork)
- **「Create fork」をクリック**
- 少し待つ...

#### ステップ3：Streamlit Cloud に登録
- https://streamlit.io/cloud にアクセス
- 「Sign in with GitHub」をクリック
- GitHub でログイン

#### ステップ4：アプリをデプロイする
- 「New app」をクリック
- 以下を入力:
  - **Repository**: `maouM-cmd/gasu` (またはあなたのフォークしたもの)
  - **Branch**: `main`
  - **Main file path**: `streamlit_app.py`
  - **App URL**: 好きな URL（例：`my-gas-app`）
- **「Deploy」をクリック**

#### ステップ5：起動完了！🎉
- 1分待つと、自分だけの URL が出現
- ブックマークして使い続ける

**これで、どこからでもアクセス可能です！**

---

### **方法2️⃣：インストール版（自分のパソコンで動かしたい場合）**

#### 必要なもの
- Windows/Mac/Linux
- Python 3.9 以上（[ダウンロード](https://www.python.org/)）

#### セットアップ（コマンドラインが初めての人）
1. **フォルダを作成**
   ```bash
   mkdir my-gas-app
   cd my-gas-app
   ```

2. **プロジェクトをダウンロード**
   ```bash
   git clone https://github.com/maouM-cmd/gasu.git .
   ```

3. **Python 環境を準備**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # または
   .venv\Scripts\activate     # Windows
   ```

4. **パッケージをインストール**
   ```bash
   pip install -r requirements-streamlit.txt
   ```

5. **アプリを起動**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **ブラウザが自動で開きます**
   - http://localhost:8501

---

## 📊 何が入ってるの？

✅ **顧客一覧**: 登録した全顧客と基本情報  
✅ **顧客登録**: 新しい顧客を追加  
✅ **検針入力**: 毎月の検針値を記録  
✅ **請求管理**: 自動計算→入金記録  
✅ **大きなボタン**: 高齢者でも使いやすい  
✅ **シンプルメニュー**: ゴチャゴチャしない  

---

## 🆚 他の方法との比較

| | **Streamlit Cloud** | **インストール版** |
|---|---|---|
| **セットアップ** | ☁️ 不要 | 💻 20分 |
| **毎月の費用** | 無料 | 無料 |
| **どこからアクセス** | 📱 どこからでも | 💻 そのパソコンのみ |
| **推奨** | 👴👵 親御さん向け | 🧑‍💻 開発者向け |

---

## 🎨 実装済み機能

- ✅ **📊 顧客一覧**: 登録済みの全顧客を表示
- ✅ **👤 顧客登録**: 新規顧客の追加（基本料金・単価・税率設定）
- ✅ **📏 検針入力**: 検針値の記録、日付管理
- ✅ **💵 請求管理**: 自動生成、入金記録、一覧表示
- ✅ **🔄 自動計算**: 検針差分から料金を自動計算
- ✅ **💾 データ保存**: すべてローカルで安全に保存
- ✅ **🎯 高齢者UI**: シンプル・大きなボタン・直感的操作

---

## 💻 ローカル開発（開発者向け）

### 仮想環境セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# または
.venv\Scripts\activate     # Windows

pip install -r requirements-streamlit.txt
```

### Streamlit アプリを起動

```bash
streamlit run streamlit_app.py
```

→ ブラウザ: http://localhost:8501

### Django アプリを起動（詳細機能版）

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

→ ブラウザ: http://127.0.0.1:8000

---

## 📊 使途別ガイド

| 用途 | 推奨方法 | 難易度 |
|---|---|---|
| 親御さん（最初から） | Streamlit Cloud | ⭐ 超簡単 |
| 親御さん（初心者向け） | インストール版 | ⭐☆ 簡単 |
| 開発者（カスタマイズしたい） | ローカル Streamlit | ⭐☆☆ 中程度 |
| 自分で本番環境を構築 | Django + Docker | ⭐☆☆☆ 高度 |

---

## 🧪 テストを実行

```bash
pip install -r requirements.txt
pytest -v
```

成功例：
```
tests/test_billing_tariff.py::test_calculate_invoice_amounts PASSED
tests/test_integration_generate_invoices.py::test_generate_invoices PASSED
```

---

## 🐳 Docker で本番環境をシミュレート

```bash
docker-compose up --build
```

→ http://localhost:8000

---

## 📁 プロジェクト構成

```
gasu/
├── streamlit_app.py             # Streamlit UI（推奨）
├── web/                         # Django プロジェクト
│   ├── settings.py              # 開発設定
│   ├── settings_prod.py         # 本番設定
│   └── wsgi.py                  # WSGI エントリーポイント
├── billing/                     # ビジネスロジック
│   ├── models.py                # データモデル
│   ├── views.py                 # Django ビュー
│   ├── tariff.py                # 料金計算ロジック
│   ├── utils.py                 # ユーティリティ関数
│   └── management/commands/     # 管理コマンド
├── templates/                   # Django HTML テンプレート
├── tests/                       # テストコード
├── deploy/                      # デプロイ設定
│   ├── nginx.conf               # Nginx 設定
│   └── gasu.service             # systemd サービス
├── docker-compose.yml           # Docker Compose 設定
└── requirements.txt             # Python 依存パッケージ
```

---

## 🔧 本番環境へのデプロイ（上級者向け）
1. 顧客作成・編集フローの実装（フォーム／検針の過去データ表示）
2. 請求計算の自動化（検針差分から請求作成）と請求の一括発行ワークフロー
3. PDFレイアウト調整と印刷検証（A4、改ページ、フォント）
4. 運用: バックアップ自動化・監査ログ出力・デプロイ手順

---
更新はブランチ `feature/django-ui-start` に push されています。PR: https://github.com/maouM-cmd/gasu/pull/2

## 運用ガイド

### 自動バックアップの設定

サーバ上で定期的なバックアップを実行するには、crontab を利用できます：

```bash
# 毎日 深夜 2 時にバックアップ実行
0 2 * * * cd /path/to/gasu && python manage.py backup_db
```

または systemd timer:

```ini
[Unit]
Description=GASU Database Backup
After=network.target

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00

[Install]
WantedBy=timers.target
```

### データのセキュリティ

#### バックアップファイルの暗号化

本番環境では、バックアップファイルを暗号化することを推奨します：

```bash
# gpg で暗号化
gpg --symmetric --cipher-algo AES256 backups/db_*.sqlite3.gz

# 復号化
gpg --decrypt backups/db_*.sqlite3.gz.gpg | gunzip > db_restored.sqlite3
```

また、バックアップファイルは 600 権限（所有者のみ読取可）に設定し、別のストレージ（S3、外部ディスク等）に保存することを推奨します。

#### データベースアクセス制御

- **開発環境**: SQLite（ローカル）、認証なし（許容）
- **本番環境**: PostgreSQL への移行を推奨（ユーザ認証、SSL接続、バックアップ等が充実）

```bash
# PostgreSQL への移行例
pip install psycopg2-binary
# settings.py の DATABASES を以下に変更
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'gasu_db',
#        'USER': 'gasu_user',
#        'PASSWORD': '...',
#        'HOST': 'db.example.com',
#        'PORT': '5432',
#    }
# }
```

#### 監査ログ

`billing/models.py` の `AuditLog` モデルですべての重要操作（請求作成、入金確認等）がログされます。管理画面で確認できます。

---


## 本番環境へのデプロイ

### 前提条件
- Ubuntu 20.04 LTS 以上または同等のサーバ
- PostgreSQL 12 以上（推奨）
- Nginx 1.18 以上
- Python 3.9 以上

### 環境構築手順

1. **サーバのセットアップ**

```bash
# パッケージ更新
sudo apt update && sudo apt upgrade -y

# PostgreSQL インストール（例）
sudo apt install -y postgresql postgresql-contrib

# Nginx インストール
sudo apt install -y nginx

# Python 環境
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# その他必要なライブラリ
sudo apt install -y build-essential libpq-dev libcairo2-dev libpango1.0-dev
```

2. **アプリケーション展開**

```bash
# アプリケーションディレクトリ作成
sudo mkdir -p /opt/gasu
cd /opt/gasu

# リポジトリをクローン
sudo git clone https://github.com/your-repo/gasu.git .

# 所有権設定
sudo chown -R gasu:gasu /opt/gasu
```

3. **環境変数設定**

```bash
# .env ファイルを作成
cp .env.example .env

# .env を編集
sudo nano .env
# SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS 等を設定
```

4. **仮想環境と依存インストール**

```bash
cd /opt/gasu

# 仮想環境作成
python3.11 -m venv .venv
source .venv/bin/activate

# 依存インストール（本番向けsettings_prodを使用）
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

5. **PostgreSQL データベース設定**

```bash
# PostgreSQL に接続
sudo -u postgres psql

# ユーザとデータベース作成
CREATE USER gasu_user WITH PASSWORD 'your-password';
CREATE DATABASE gasu_db OWNER gasu_user;
ALTER ROLE gasu_user SET client_encoding TO 'utf8';
ALTER ROLE gasu_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gasu_user SET default_transaction_deferrable TO on;
ALTER ROLE gasu_user SET default_transaction_level TO 'read committed';
\q
```

6. **Django マイグレーション**

```bash
cd /opt/gasu
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=web.settings_prod
python manage.py migrate
python manage.py collectstatic --noinput
```

7. **システムユーザー作成**

```bash
# システムユーザ（gasu）作成
sudo useradd -m -s /bin/bash gasu || true
```

8. **Gunicorn と systemd 設定**

```bash
# systemd service ファイルをコピー
sudo cp deploy/gasu.service /etc/systemd/system/

# service ファイルを編集（パスを確認）
sudo nano /etc/systemd/system/gasu.service

# systemd リロード
sudo systemctl daemon-reload

# サービス有効化・起動
sudo systemctl enable gasu
sudo systemctl start gasu

# ステータス確認
sudo systemctl status gasu
```

9. **Nginx 設定**

```bash
# Nginx 設定をコピー
sudo cp deploy/nginx.conf /etc/nginx/sites-available/gasu

# シンボリックリンク作成
sudo ln -s /etc/nginx/sites-available/gasu /etc/nginx/sites-enabled/

# 既存デフォルト設定を削除（オプション）
sudo rm /etc/nginx/sites-enabled/default

# Nginx 設定をテスト
sudo nginx -t

# Nginx 再起動
sudo systemctl restart nginx
```

10. **SSL 証明書（Let's Encrypt）**

```bash
# Certbot インストール
sudo apt install -y certbot python3-certbot-nginx

# 証明書取得
sudo certbot certonly --nginx -d example.com -d www.example.com

# Nginx 設定で HTTPS を有効化（deploy/nginx.conf の HTTPS セクションをコメント解除）
# その後 nginx -t && systemctl restart nginx
```

11. **バックアップスケジュール設定**

```bash
# Crontab 編集
sudo crontab -e -u gasu

# 毎日 2 時にバックアップ
0 2 * * * cd /opt/gasu && source .venv/bin/activate && python manage.py backup_db

# バックアップファイルを暗号化（オプション）
# 15 2 * * * gpg --symmetric --cipher-algo AES256 /opt/gasu/backups/db_*.sqlite3.gz > /dev/null 2>&1
```

### デプロイ後のチェック

```bash
# ログ確認
sudo tail -f /opt/gasu/logs/error.log

# Gunicorn ステータス確認
sudo systemctl status gasu

# Nginx ステータス確認
sudo systemctl status nginx

# ブラウザでアクセス
# https://example.com
```

###セキュリティ点検リスト

- [ ] `SECRET_KEY` が強力なランダム値に設定されているか
- [ ] `DEBUG = False` に設定されているか
- [ ] `ALLOWED_HOSTS` に本番ドメインを指定しているか
- [ ] PostgreSQL ユーザーで強力なパスワードを使用しているか
- [ ] SSL 証明書が有効か（https:// で接続できるか）
- [ ] バックアップスケジュールが設定されているか
- [ ] ファイアウォール（ufw）で不要なポートを閉じているか
- [ ] 定期的なセキュリティアップデートを行う体制になっているか

### トラブルシューティング

**Gunicorn が起動しない**

```bash
sudo systemctl restart gasu
sudo journalctl -u gasu -n 20
```

**Nginx が接続できない**

```bash
sudo nginx -t
curl -I http://127.0.0.1:8000
```

**データベース接続エラー**

```bash
# .env の DB_* 設定を確認
psql -U gasu_user -d gasu_db -h localhost
```

---

## ❓ よくある質問（Q&A）

### Q: 無料ですか？
**A:** はい、完全無料です。Streamlit Cloud も無料枠があります。

### Q: インターネット接続がないパソコンでも使えますか？
**A:** はい。「インストール版」を選べば、インターネット不要です（セットアップ時のみ必要）。

### Q: データは安全ですか？
**A:** はい。データはあなたのパソコンまたはクラウド上に保存され、外部に送信されません。

### Q: バックアップはどうする？
**A:** 
- **Streamlit Cloud版**: 自動バックアップあり
- **インストール版**: ファイルをコピーするだけ（`gas_billing.db` ファイルをバックアップ）

### Q: スマホでも使えますか？
**A:** はい。Streamlit Cloud版なら、スマホのブラウザ（Safari/Chrome）で使えます。

### Q: 開発者向けの詳細情報は？
**A:** このREADMEの下の方に技術詳細があります。

---

## 🆘 トラブルシューティング

### 問題1：「Python が見つかりません」と言われた
解決策：
1. https://www.python.org/ からダウンロード
2. **「Add Python to PATH」にチェック**を入れてインストール
3. コマンドラインを再起動

### 問題2：Streamlit Cloud でデプロイが失敗した
解決策：
1. ブランチが `main` になっているか確認
2. メインファイルが `streamlit_app.py` か確認
3. 5分待ってみる（デプロイ中かもしれません）

### 問題3：データが消えた
解決策（インストール版）：
- `gas_billing.db` ファイルは？を確認
- なければ、バックアップから復元

### 問題4：ボタンが反応しない
解決策：
1. ページをリロード（F5 キー）
2. ブラウザを変える（Chrome推奨）

---

## 📞 サポート

問題が起きた場合：
1. 上の「トラブルシューティング」を確認
2. GitHub Issues で報告: https://github.com/maouM-cmd/gasu/issues/new

---

## 🔧 開発者向け情報

### ディレクトリ構成

```
gasu/
├── streamlit_app.py            # Streamlit アプリ本体
├── requirements-streamlit.txt  # Python パッケージ一覧
├── .streamlit/
│   └── config.toml            # UI テーマ設定
│
├── web/                        # Django プロジェクト（別UI）
├── billing/                    # ビジネスロジック
├── docker-compose.yml          # Docker 設定
└── README.md                   # このファイル
```

### 技術スタック
- **Web Framework**: Streamlit (フロントエンド) + Django (バックエンド)
- **Database**: SQLite（開発） / PostgreSQL（本番）
- **Language**: Python 3.9+
- **Deployment**: Streamlit Cloud / Render.com / VPS

### ローカル開発

```bash
# Streamlit版
streamlit run streamlit_app.py

# Django版
python manage.py runserver
```

### テスト実行
```bash
pytest -v
```

---

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

---

**🌟 このプロジェクトが役に立ったら、GitHub Star をお願いします！**


### セットアップ（初回のみ）

1. **GitHub アカウント**に本リポジトリをフォーク:  
   https://github.com/maouM-cmd/gasu/fork

2. **Render.com にログイン**:  
   https://render.com

3. **以下のボタンをクリック**:

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/maouM-cmd/gasu)

4. フォームで以下を入力:
   - **Service Name**: `gasu` (任意)
   - **Repository**: `https://github.com/{your-username}/gasu`
   - **Branch**: `feature/django-ui-start` (または `main`)
   - **Build Command**: 自動設定
   - **Start Command**: 自動設定

5. **確認画面で Deploy ボタンをクリック**

6. デプロイが完了すると、自動生成されたURLが表示されます（例: `https://gasu-xxxx.onrender.com`）

### デプロイ後

- ブラウザでURLにアクセス
- ログイン画面が表示されます
- **デモ画面を見たい場合**:
  - プロジェクトのダッシュボードで「Shell」タブを開き、以下を実行:
    ```bash
    python manage.py create_demo
    ```
  - ユーザー: `demo` / パスワード: `demo123`

### トラブルシューティング（Render）

**デプロイが失敗する**

- ダッシュボードの「Logs」タブでエラーを確認
- `requirements.txt` に必要なパッケージが含まれているかチェック

**データベース接続エラー**

- Render が自動生成した PostgreSQL サービスをアプリが正しく参照しているか確認
- `render.yaml` ファイルが存在するか確認

**Render 上での Static Files / Media Files**

- Render では SQLite が永続化されない（コンテナの再起動時に消失）
- 本番運用では環境変数 `DATABASE_URL` で PostgreSQL を使用（自動セットアップ済み）

---


