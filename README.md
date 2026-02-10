# gasu ⛽
ガス料金管理システム - 高齢者にも使いやすいシンプル設計

---

## 🚀 クイックスタート（3つの方法）

### ⚡ **最速：Streamlit Cloud で無料・ワンクリック起動**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

**推奨：高齢者にも最適なシンプルな UI**

1. [gasu リポジトリをフォーク](https://github.com/maouM-cmd/gasu/fork)

2. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス

3. **「New app」→「Deploy an app」** を選択

4. フォークしたリポを入力:
   ```
   https://github.com/{your-username}/gasu
   App URL: streamlit_app.py
   ```

5. **Deploy** をクリック → **即座に公開 URL が生成** 🎉

**デモ顧客は自動作成されます**（初回アクセス時は 初期状態）

---

### 🐳 **Docker Compose で一瞬で起動**

```bash
cd /workspaces/gasu
docker-compose up --build
```

ブラウザ: **http://localhost:8000**
1. フォークしたリポを入力:
   ```
   https://github.com/{your-username}/gasu
   App URL: streamlit_app.py
   ```

2. **Deploy** をクリック → **即座に公開 URL が生成** 🎉

---

### 💻 ローカル仮想環境で起動（開発者向け）

```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

ブラウザ: **http://localhost:8501**

---

## 📊 実装済み機能

- ✅ **📊 顧客一覧**: 登録済みの全顧客を表示
- ✅ **👤 顧客登録**: 新規顧客の追加（基本料金・単価・税率設定）
- ✅ **📏 検針入力**: 検針値の記録、日付管理
- ✅ **💵 請求管理**: 自動生成、入金記録、一覧表示
- ✅ **🔄 自動計算**: 検針差分から料金を自動計算
- ✅ **💾 SQLite DB**: ローカルに永続化（クラウド対応）
- ✅ **🎯 高齢者UI**: シンプル・大きなボタン・直感的操作

---

## 📁 ディレクトリ構成

```
gasu/
├── streamlit_app.py           # 🌟 Streamlit メインアプリ
├── requirements-streamlit.txt # Streamlit 用依存
├── .streamlit/
│   └── config.toml           # Streamlit 設定（テーマ等）
│
├── web/                       # Django プロジェクト（代替案）
├── billing/                   # Django アプリ
├── docker-compose.yml         # Docker 設定
└── README.md                  # この ファイル
```

---

## 🔧 Django 版も利用可能

Streamlit の代わりに Django を使う場合：

```bash
# Django 版起動
docker-compose up --build
```

→ ログイン画面有、PDF 生成機能あり、より高度な機能

---

## ローカルでの起動手順（開発者向け・詳細）
1. 仮想環境を作る（推奨）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-streamlit.txt
```

2. Streamlit アプリを起動

```bash
streamlit run streamlit_app.py
```

ブラウザ: **http://localhost:8501** に自動で開きます

---

## 🎯 使途別ガイド

### 親御さん・ユーザー向け
→ **Streamlit Cloud で公開 URL をクリック**（推奨）
- セットアップ不要
- いつでもアクセス可能
- シンプルな操作

### 開発者向け（ローカル開発）
```bash
streamlit run streamlit_app.py
```

### 小規模ビジネス向け（本番環境）
→ **Render.com（クラウド）** または **VPS（自前）**:

```bash
docker-compose up -d
```

---
- ✅ **バックアップ**: DB 自動バックアップ（gzip 圧縮）
- ✅ **テスト**: 料金計算、請求生成、エッジケース（pytest）
- ✅ **Deploy**: Docker/Compose、Gunicorn、Nginx、systemd、PostgreSQL対応

---

## 🧪 テスト実行方法

```bash
pip install -r requirements.txt
pytest -q
```

## Docker での起動（簡易）

```bash
# ビルドして起動
docker compose up --build
# コンテナ内部でマイグレーション
docker compose exec web python manage.py migrate
docker compose exec web python manage.py create_demo
```

## バックアップ
- SQLite を使う場合は `python manage.py backup_db` で `backups/` 配下に gz 圧縮されたダンプが作成されます。


（`tests/test_billing_tariff.py` に料金計算の単体テストがあります）

## 次フェーズ（優先順）
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

## 🌐 Render.com へのワンクリックデプロイ

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


