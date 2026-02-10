# gasu
# Codex task

## ステータス
- 現状: CLIで動くMVPコアまで実装済み
	- 料金計算ロジック: 実装済み
	- SQLiteスキーマ: 実装済み
	- CLI操作: 検針→請求→入金の基本操作が可能
	- 請求計算テスト: 実装済み
	- 未実装（次フェーズ／READMEに明記）: Django Web画面、請求書/領収書PDF、高齢者向けUI最適化、操作ログ/バックアップ自動化

## 次フェーズ
- Djangoの画面実装（顧客一覧・検針入力・請求一覧）をまず実装します。
	- 目標: Web UIでの基本ワークフロー確認（検針入力→請求生成→入金反映）
	- 以降: PDF出力・運用自動化・アクセシビリティ最適化を順次実装

（この変更はリモートに新ブランチを作成し、PRを作成して進めます）

## 実装済み（このPRで反映された主な内容）
- Django最小骨組み（`web`プロジェクト）と `billing` アプリのスキャフォールド
- モデル: `Customer`, `MeterReading`, `Invoice`, `Payment` の基礎実装
- `Customer` に料金プラン／税率フィールドを追加
- 料金計算ロジックを `billing/tariff.py` に実装（単体テストあり）
- UI: 顧客一覧 / 検針入力 / 請求一覧 のテンプレート（Bootstrapで高齢者向け配慮）
- PDF出力の雛形（WeasyPrintを用いた `invoice_pdf` ビューとテンプレート）
- 開発用管理コマンド `python manage.py create_demo` を追加

## ローカルでの起動手順（開発者向け）
1. 仮想環境を作る（推奨）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. マイグレーションとデモデータ作成

```bash
python manage.py migrate
python manage.py create_demo
```

3. 開発サーバ起動

```bash
python manage.py runserver
# ブラウザで http://127.0.0.1:8000/ を開く
```

注意: `WeasyPrint` はネイティブ依存（cairo, pango, gdk-pixbuf 等）が必要な場合があります。Linuxで不足する場合はパッケージマネージャでインストールしてください。

## テスト実行方法

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

