import io
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔄", layout="wide")

# ---------- Custom CSS for Colorful Design ----------
st.markdown("""
    <style>
        /* Background Gradient for entire app */
        .stApp {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Header */
        .gradient-bg {
            background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 25px;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-bottom: 30px;
            box-shadow: 0 8px 30px rgb(255 75 43 / 0.5);
            user-select: none;
        }
        .gradient-bg h1 {
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 0.2rem;
            letter-spacing: 0.1em;
            text-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
        .gradient-bg h2 {
            font-weight: 600;
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            opacity: 0.9;
            text-shadow: 0 1px 3px rgba(0,0,0,0.25);
        }
        .gradient-bg p {
            font-weight: 400;
            font-size: 1rem;
            opacity: 0.8;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }
        /* Metric Cards */
        .metric-card {
            border-radius: 25px;
            padding: 25px 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
            margin: 10px;
            text-align: center;
            cursor: default;
            user-select: none;
            font-weight: 700;
            font-size: 2.5rem;
            color: white;
            letter-spacing: 0.05em;
            text-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }
        .metric-red {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
        }
        .metric-green {
            background: linear-gradient(45deg, #43cea2, #185a9d);
        }
        .metric-blue {
            background: linear-gradient(45deg, #36d1dc, #5b86e5);
        }
        .metric-purple {
            background: linear-gradient(45deg, #7b2ff7, #f107a3);
        }
        .metric-card p {
            font-size: 1.1rem;
            margin-top: 8px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            opacity: 0.9;
        }
        /* Sidebar */
        .sidebar-content {
            background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 25px 20px;
            border-radius: 20px;
            margin: 10px 0 20px 0;
            box-shadow: 0 6px 20px rgb(0 0 0 / 0.1);
            color: #0c4a6e;
            font-weight: 600;
            user-select: none;
        }
        .sidebar-content h3 {
            color: #2563eb;
            margin-bottom: 15px;
            font-size: 1.3rem;
            text-align: center;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        /* Filters Section */
        .filters-section {
            background: linear-gradient(45deg, #dbeafe, #bfdbfe);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            border-left: 6px solid #3b82f6;
            box-shadow: 0 4px 15px rgb(59 130 246 / 0.3);
            color: #1e40af;
            font-weight: 600;
        }
        /* Error and Success Messages */
        .error-msg {
            background: linear-gradient(45deg, #fee2e2, #fecaca);
            border: 1px solid #f87171;
            color: #b91c1c;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            font-weight: 700;
            box-shadow: 0 4px 15px rgb(220 38 38 / 0.3);
            user-select: none;
        }
        .success-msg {
            background: linear-gradient(45deg, #d1fae5, #a7f3d0);
            border: 1px solid #34d399;
            color: #047857;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            font-weight: 700;
            box-shadow: 0 4px 15px rgb(34 197 94 / 0.3);
            user-select: none;
        }
        /* Data Editor Table */
        .stDataFrame table {
            border-radius: 15px !important;
            overflow: hidden !important;
            box-shadow: 0 8px 30px rgb(0 0 0 / 0.15) !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            background: white !important;
            color: #1e293b !important;
            font-weight: 600 !important;
        }
        .stDataFrame thead tr {
            background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
        }
        .stDataFrame tbody tr:hover {
            background-color: #bfdbfe !important;
            cursor: pointer !important;
        }
        /* Selectbox and Inputs */
        div[role="combobox"] > div > input {
            font-weight: 600 !important;
            color: #1e293b !important;
        }
        /* Download Button */
        button[title="Download file"] {
            background: linear-gradient(45deg, #7b2ff7, #f107a3);
            color: white;
            font-weight: 700;
            border-radius: 15px;
            padding: 10px 20px;
            box-shadow: 0 8px 30px rgb(241 7 163 / 0.5);
            transition: background 0.3s ease;
        }
        button[title="Download file"]:hover {
            background: linear-gradient(45deg, #f107a3, #7b2ff7);
            box-shadow: 0 12px 40px rgb(123 47 247 / 0.7);
        }
        /* Footer */
        footer {
            text-align: center;
            margin-top: 40px;
            font-weight: 600;
            color: #e0e7ff;
            user-select: none;
        }
        /* Responsive tweaks */
        @media (max-width: 768px) {
            .metric-card {
                font-size: 2rem !important;
                padding: 20px 15px !important;
            }
            .gradient-bg h1 {
                font-size: 2rem !important;
            }
            .gradient-bg h2 {
                font-size: 1.1rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

DATE_TODAY = datetime.date.today()

# ---------- Embedded Data from Excel ----------
INITIAL_DATA = [
    # (Your existing INITIAL_DATA here, unchanged)
    # For brevity, omitted here but use your full INITIAL_DATA list as in your code
]

def load_data() -> pd.DataFrame:
    df = pd.DataFrame(INITIAL_DATA)
    if "Status" not in df.columns:
        df["Status"] = "Belum"
    if "Tanggal_Buyback" not in df.columns:
        df["Tanggal_Buyback"] = pd.NaT
    if "Catatan" not in df.columns:
        df["Catatan"] = ""
    if "Qty_Buyback" not in df.columns:
        df["Qty_Buyback"] = 0
    df["Tanggal_Buyback"] = pd.to_datetime(df["Tanggal_Buyback"], errors="coerce").dt.date
    df = df.reset_index(drop=True)
    df.insert(0, "_ROW_ID", range(1, len(df)+1))
    df["Sisa_Qty"] = df["QTY"] - df["Qty_Buyback"]
    df.loc[df["Sisa_Qty"] < 0, "Sisa_Qty"] = 0
    return df

def filtered_df(df: pd.DataFrame, status_opt: str, search: str) -> pd.DataFrame:
    out = df.copy()
    if status_opt in ("Belum", "Sudah"):
        out = out[out["Status"] == status_opt]
    if search:
        mask = pd.Series(False, index=out.index)
        for col in out.select_dtypes(include=["object"]).columns:
            mask = mask | out[col].fillna("").str.contains(search, case=False, na=False)
        out = out[mask]
    return out

def write_excel_to_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        export_df = df.drop(columns=["_ROW_ID"], errors="ignore")
        export_df.to_excel(writer, index=False, sheet_name="Sheet1")
    buf.seek(0)
    return buf.read()

# ---------- Load Data ----------
df = load_data()

# ---------- Header ----------
st.markdown(
    '<div class="gradient-bg">'
    '<h1>🔄 IDSMED - Mediva</h1>'
    '<h2>IDSMED–Mediva Spare Parts Buyback Tracking System</h2>'
    '<p>Lokasi: Logos - Managed by Akmaludin Agustian for Heru Utomo</p>'
    '</div>', unsafe_allow_html=True)

# ---------- Summary KPI ----------
total_qty = int(df["QTY"].sum())  # total unit awal, integer
total_qty_buyback = int(df["Qty_Buyback"].sum())
total_sisa_qty = total_qty - total_qty_buyback  # hitung sisa qty total secara logika
total_item = len(df)  # jumlah baris item
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card metric-red"><h3>{total_item}</h3><p>Total Item</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card metric-blue"><h3>{total_qty}</h3><p>Total Qty</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card metric-green"><h3>{total_qty_buyback}</h3><p>Buyback Qty</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card metric-purple"><h3>{total_sisa_qty}</h3><p>Sisa Qty</p></div>', unsafe_allow_html=True)

st.divider()

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.markdown('<div class="sidebar-content"><h3>Filter & Aksi</h3>', unsafe_allow_html=True)
    status_opt = st.selectbox("Status", ["Semua", "Belum", "Sudah"], index=0)
    search = st.text_input("Cari (bebas: nama/serial/kode)", "")
    st.caption("Pencarian diterapkan ke semua kolom teks.")
    st.markdown("---")
    st.write("**Kolom yang bisa diedit:** Status, Tanggal Buyback, Catatan, Qty Buyback")
    st.write("**Kolom otomatis:** Sisa Qty (QTY - Qty Buyback)")
    st.markdown("---")
    st.caption("Tip: Klik header kolom untuk sort / filter tambahan.")
    st.markdown('</div>', unsafe_allow_html=True)
    show_complete = st.checkbox("Tampilkan hanya yang belum selesai (Qty > 0)", value=False)
    show_zero_sisa = st.checkbox("Tampilkan hanya yang sudah habis (Qty = 0)", value=False)

# ---------- Apply Filters ----------
view = filtered_df(df, status_opt, search)
if show_complete:
    view = view[view["Sisa_Qty"] > 0]
elif show_zero_sisa:
    view = view[view["Sisa_Qty"] == 0]

# ---------- Editable Columns ----------
editable_cols = [c for c in ["Status", "Tanggal_Buyback", "Catatan", "Qty_Buyback"] if c in view.columns]
disabled_cols = [c for c in view.columns if c not in editable_cols]

cfg = {}
if "Status" in view.columns:
    cfg["Status"] = st.column_config.SelectboxColumn("Status", options=["Belum", "Sudah"], default="Belum")
if "Tanggal_Buyback" in view.columns:
    cfg["Tanggal_Buyback"] = st.column_config.DateColumn("Tanggal Buyback", format="YYYY-MM-DD", default=None)
if "Catatan" in view.columns:
    cfg["Catatan"] = st.column_config.TextColumn("Catatan")
if "Qty_Buyback" in view.columns:
    cfg["Qty_Buyback"] = st.column_config.NumberColumn("Qty Buyback", min_value=0, step=1, help="Jumlah unit yang sudah dibuyback, maksimal sama dengan QTY")
if "Sisa_Qty" in view.columns:
    cfg["Sisa_Qty"] = st.column_config.NumberColumn("Sisa Qty", disabled=True, help="Sisa unit yang belum dibuyback (otomatis)")

# ---------- Table (Editable) ----------
st.markdown("### 📊 Data Buyback")

# Simpan _ROW_ID terpisah untuk update nanti
row_ids = view["_ROW_ID"]

# Drop kolom _ROW_ID agar tidak tampil di tabel
view_display = view.drop(columns=["_ROW_ID"], errors="ignore")

# Tentukan kolom yang bisa diedit dan yang disabled
editable_cols = [c for c in ["Status", "Tanggal_Buyback", "Catatan", "Qty_Buyback"] if c in view_display.columns]
disabled_cols = [c for c in view_display.columns if c not in editable_cols]

# Konfigurasi kolom
cfg = {}
if "Status" in view_display.columns:
    cfg["Status"] = st.column_config.SelectboxColumn("Status", options=["Belum", "Sudah"], default="Belum")
if "Tanggal_Buyback" in view_display.columns:
    cfg["Tanggal_Buyback"] = st.column_config.DateColumn("Tanggal Buyback", format="YYYY-MM-DD", default=None)
if "Catatan" in view_display.columns:
    cfg["Catatan"] = st.column_config.TextColumn("Catatan")
if "Qty_Buyback" in view_display.columns:
    cfg["Qty_Buyback"] = st.column_config.NumberColumn("Qty Buyback", min_value=0, step=1, help="Jumlah unit yang sudah dibuyback, maksimal sama dengan QTY")
if "Sisa_Qty" in view_display.columns:
    cfg["Sisa_Qty"] = st.column_config.NumberColumn("Sisa Qty", disabled=True, help="Sisa unit yang belum dibuyback (otomatis)")

# Tampilkan data editor tanpa kolom _ROW_ID
edited = st.data_editor(view_display, use_container_width=True, hide_index=True, disabled=disabled_cols, column_config=cfg, num_rows="fixed", key="editor")

# Tambahkan kembali _ROW_ID ke edited dataframe untuk update
edited["_ROW_ID"] = row_ids.values

# ---------- Validation ----------
validation_passed = True
invalid_rows = edited[edited["Qty_Buyback"] > edited["QTY"]]
if not invalid_rows.empty:
    validation_passed = False
    st.markdown('<div class="error-msg">⚠️ Qty Buyback tidak boleh lebih besar dari Qty total!</div>', unsafe_allow_html=True)

# ---------- Apply Changes ----------
if validation_passed:
    edited["Sisa_Qty"] = edited["QTY"] - edited["Qty_Buyback"]
    edited.loc[edited["Sisa_Qty"] < 0, "Sisa_Qty"] = 0
    if not edited.equals(view):
        base = df.set_index("_ROW_ID")
        upd = edited.set_index("_ROW_ID")
        base.update(upd[editable_cols])
        df = base.reset_index()
        df["Sisa_Qty"] = df["QTY"] - df["Qty_Buyback"]
        df.loc[df["Sisa_Qty"] < 0, "Sisa_Qty"] = 0
        st.markdown('<div class="success-msg">✅ Data berhasil diperbarui!</div>', unsafe_allow_html=True)

# ---------- Download ----------
st.markdown("### 💾 Download Data")
bytes_xlsx = write_excel_to_bytes(df)
st.download_button("⬇️ Download Excel yang sudah diupdate", data=bytes_xlsx,
                   file_name=f"Data Buyback Mediva - updated {DATE_TODAY}.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                   use_container_width=True)
st.caption("Gunakan tombol download untuk menyimpan perubahan permanen.")

# ---------- Footer ----------
st.markdown("<hr><footer><p>© 2025 IDSMED - Mediva Buyback Tracking System</
