"""
ガス料金管理システム - Streamlit 版
高齢者にも使いやすいシンプルな UI
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
from decimal import Decimal
import os

# ページ設定
st.set_page_config(
    page_title="ガス料金管理",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for better elderly-friendly UI
st.markdown("""
<style>
    body {
        font-size: 18px;
    }
    .stButton > button {
        font-size: 16px;
        padding: 12px 24px;
        height: auto;
    }
    .stSelectbox, .stNumberInput, .stDateInput, .stTextInput {
        font-size: 14px;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
DB_FILE = "gas_billing.db"

def init_db():
    """データベースを初期化"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Customer テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            basic_fee REAL DEFAULT 0,
            unit_price REAL DEFAULT 0.1,
            tax_rate REAL DEFAULT 0.1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # MeterReading テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS meter_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date DATE NOT NULL,
            value REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Invoice テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date DATE NOT NULL,
            amount REAL NOT NULL,
            paid INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # デモデータが存在しなければ作成
    c.execute('SELECT COUNT(*) FROM customers')
    if c.fetchone()[0] == 0:
        # デモ顧客を作成
        c.execute('''
            INSERT INTO customers (name, phone, address, basic_fee, unit_price, tax_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('デモ顧客 A', '090-1234-5678', '東京都渋谷区', 1500, 150, 0.1))
        
        c.execute('''
            INSERT INTO customers (name, phone, address, basic_fee, unit_price, tax_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('デモ顧客 B', '090-9876-5432', '東京都新宿区', 1500, 150, 0.1))
        
        # デモ検針データを作成
        from datetime import datetime, timedelta
        today = datetime.now().date()
        c.execute('''
            INSERT INTO meter_readings (customer_id, date, value)
            VALUES (?, ?, ?)
        ''', (1, today - timedelta(days=30), 100))
        c.execute('''
            INSERT INTO meter_readings (customer_id, date, value)
            VALUES (?, ?, ?)
        ''', (1, today, 120))
        
        c.execute('''
            INSERT INTO meter_readings (customer_id, date, value)
            VALUES (?, ?, ?)
        ''', (2, today - timedelta(days=30), 50))
        c.execute('''
            INSERT INTO meter_readings (customer_id, date, value)
            VALUES (?, ?, ?)
        ''', (2, today, 75))
    
    conn.commit()
    conn.close()

def get_customers():
    """全顧客を取得"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM customers ORDER BY name')
    customers = [dict(row) for row in c.fetchall()]
    conn.close()
    return customers

def add_customer(name, phone, address, basic_fee, unit_price, tax_rate):
    """顧客を追加"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO customers (name, phone, address, basic_fee, unit_price, tax_rate)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, phone, address, basic_fee, unit_price, tax_rate))
    conn.commit()
    conn.close()

def add_meter_reading(customer_id, reading_date, value):
    """検針を追加"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO meter_readings (customer_id, date, value)
        VALUES (?, ?, ?)
    ''', (customer_id, reading_date, value))
    conn.commit()
    conn.close()

def get_meter_readings(customer_id):
    """顧客の検針履歴を取得（最新順）"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT * FROM meter_readings
        WHERE customer_id = ?
        ORDER BY date DESC
    ''', (customer_id,))
    readings = [dict(row) for row in c.fetchall()]
    conn.close()
    return readings

def calculate_invoice_amount(basic_fee, unit_price, usage, tax_rate):
    """料金を計算"""
    subtotal = Decimal(str(basic_fee)) + Decimal(str(unit_price)) * Decimal(str(usage))
    tax = subtotal * Decimal(str(tax_rate))
    total = subtotal + tax
    return float(subtotal), float(tax), float(total)

def generate_invoices():
    """検針差分から請求を生成"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    customers = get_customers()
    created_count = 0
    
    for customer in customers:
        readings = get_meter_readings(customer['id'])
        if len(readings) < 2:
            continue
        
        # 最新と前回の検針
        latest = readings[0]
        previous = readings[1]
        
        usage = max(0, float(latest['value']) - float(previous['value']))
        
        if usage < 0:
            continue  # 消費量がマイナスはスキップ
        
        subtotal, tax, total = calculate_invoice_amount(
            customer['basic_fee'],
            customer['unit_price'],
            usage,
            customer['tax_rate']
        )
        
        # 既に同じ日が請求されていないか確認
        c.execute('''
            SELECT COUNT(*) FROM invoices
            WHERE customer_id = ? AND date = ?
        ''', (customer['id'], latest['date']))
        
        if c.fetchone()[0] == 0:
            c.execute('''
                INSERT INTO invoices (customer_id, date, amount)
                VALUES (?, ?, ?)
            ''', (customer['id'], latest['date'], total))
            created_count += 1
    
    conn.commit()
    conn.close()
    return created_count

def get_invoices():
    """全請求を取得"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT i.*, c.name
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        ORDER BY i.date DESC
    ''')
    invoices = [dict(row) for row in c.fetchall()]
    conn.close()
    return invoices

def mark_invoice_paid(invoice_id):
    """請求を入金済みに変更"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE invoices SET paid = 1 WHERE id = ?', (invoice_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Sidebar navigation
st.sidebar.title("📋 メニュー")
page = st.sidebar.radio(
    "選択してください",
    ["📊 顧客一覧", "👤 顧客登録", "📏 検針入力", "💵 請求管理"]
)

# ============================================
# ページ 1: 顧客一覧
# ============================================
if page == "📊 顧客一覧":
    st.title("📊 顧客一覧")
    
    customers = get_customers()
    
    if customers:
        df = pd.DataFrame(customers)
        df = df[['name', 'phone', 'address', 'basic_fee', 'unit_price']]
        df.columns = ['名前', '電話番号', '住所', '基本料金', '単価']
        
        st.dataframe(df, use_container_width=True)
        
        st.info(f"👥 登録されている顧客: **{len(customers)} 件**")
    else:
        st.warning("顧客がまだ登録されていません")
        st.info("📝 左のメニューから「顧客登録」を選択して、最初の顧客を追加してください")

# ============================================
# ページ 2: 顧客登録
# ============================================
elif page == "👤 顧客登録":
    st.title("👤 新規顧客登録")
    
    with st.form("customer_form"):
        name = st.text_input("👤 顧客名", placeholder="例：田中太郎", key="name_input")
        phone = st.text_input("☎️ 電話番号", placeholder="例：090-1234-5678", key="phone_input")
        address = st.text_area("📍 住所", placeholder="例：東京都渋谷区...", height=80, key="address_input")
        
        col1, col2 = st.columns(2)
        with col1:
            basic_fee = st.number_input("💵 基本料金（円）", value=0, min_value=0, key="basic_fee_input")
        with col2:
            unit_price = st.number_input("📊 単価（円/m³）", value=0, min_value=0, key="unit_price_input")
        
        tax_rate = st.slider("📈 税率（%）", 0, 20, 10) / 100
        
        submitted = st.form_submit_button("✅ 顧客を登録", use_container_width=True)
        
        if submitted:
            if name:
                add_customer(name, phone, address, basic_fee, unit_price, tax_rate)
                st.success(f"✅ {name} を登録しました！")
                st.rerun()
            else:
                st.error("❌ 顧客名を入力してください")

# ============================================
# ページ 3: 検針入力
# ============================================
elif page == "📏 検針入力":
    st.title("📏 検針入力")
    
    customers = get_customers()
    
    if customers:
        customer_names = {c['id']: c['name'] for c in customers}
        customer_id = st.selectbox(
            "👤 顧客を選択",
            options=[c['id'] for c in customers],
            format_func=lambda x: customer_names[x],
            key="meter_customer"
        )
        
        if customer_id:
            with st.form("meter_form"):
                reading_date = st.date_input("📅 日付", value=date.today(), key="meter_date")
                value = st.number_input("📊 検針値（m³）", value=0, min_value=0, key="meter_value")
                
                submitted = st.form_submit_button("✅ 検針を入力", use_container_width=True)
                
                if submitted:
                    add_meter_reading(customer_id, reading_date, value)
                    st.success("✅ 検針を記録しました！")
                    st.rerun()
            
            # 検針履歴表示
            st.subheader("📋 検針履歴")
            readings = get_meter_readings(customer_id)
            if readings:
                df = pd.DataFrame(readings)
                df = df[['date', 'value']]
                df.columns = ['日付', '検針値（m³）']
                st.dataframe(df, use_container_width=True)
            else:
                st.info("検針履歴がありません")
    else:
        st.warning("👥 先に顧客を登録してください")

# ============================================
# ページ 4: 請求管理
# ============================================
elif page == "💵 請求管理":
    st.title("💵 請求管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 請求を自動生成", use_container_width=True):
            created = generate_invoices()
            if created > 0:
                st.success(f"✅ {created} 件の請求を生成しました！")
                st.rerun()
            else:
                st.info("新しい請求はありません")
    
    with col2:
        if st.button("🔃 更新", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # 請求一覧
    st.subheader("📋 請求一覧")
    invoices = get_invoices()
    
    if invoices:
        for inv in invoices:
            status = "✅ 入金済み" if inv['paid'] else "❌ 未入金"
            status_color = "green" if inv['paid'] else "red"
            
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"👤 **{inv['name']}**")
            with col2:
                st.write(f"📅 {inv['date']}")
            with col3:
                st.write(f"💰 ¥{inv['amount']:,.0f}")
            with col4:
                if not inv['paid']:
                    if st.button(f"✅", key=f"pay_{inv['id']}", use_container_width=True):
                        mark_invoice_paid(inv['id'])
                        st.success("入金記録しました")
                        st.rerun()
                else:
                    st.write("✅")
    else:
        st.info("請求がまだ生成されていません")

# Footer
st.divider()
st.caption("⛽ ガス料金管理システム v1.0 - Streamlit Edition")
