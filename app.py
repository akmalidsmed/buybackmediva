
import io
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔄", layout="wide")

# ---------- Custom CSS for Colorful Design ----------
st.markdown("""
    <style>
        /* Background Gradient */
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            font-family: 'Arial', sans-serif;
            margin-bottom: 20px;
        }
        .metric-card {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            margin: 10px;
            text-align: center;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .metric-red { background: linear-gradient(45deg, #ff6b6b, #ff9e7d); color: white; }
        .metric-green { background: linear-gradient(45deg, #4ecdc4, #44a08d); color: white; }
        .metric-blue { background: linear-gradient(45deg, #54a0ff, #2e86de); color: white; }
        .metric-purple { background: linear-gradient(45deg, #667eea, #764ba2); color: white; }
        .sidebar-content {
            background: linear-gradient(180deg, #f8f9ff 0%, #e6f3ff 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
        }
        .filters-section {
            background: linear-gradient(45deg, #f0f9ff, #e0f2fe);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
        }
        .error-msg {
            background: linear-gradient(45deg, #fee2e2, #fecaca);
            border: 1px solid #f87171;
            color: #b91c1c;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .success-msg {
            background: linear-gradient(45deg, #d1fae5, #a7f3d0);
            border: 1px solid #34d399;
            color: #047857;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

DATE_TODAY = datetime.date.today()

# ---------- Embedded Data from Excel ----------
INITIAL_DATA = [
    {
        "NO": 1,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7026-865",
        "DESCRIPTION": "ASSY, WEARABLES KIT, SCULP, SUBMENTAL, STD",
        "QTY": 2
    },
    {
        "NO": 2,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "S805-0035-005",
        "DESCRIPTION": "WINDOW, 625DIA, 585, 755, 1064, SAPHIRE",
        "QTY": 38
    },
    {
        "NO": 3,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "ASY-13442",
        "DESCRIPTION": "10 PAC KEY SCULPSURE SUBMNTL 1PK SEC",
        "QTY": 8
    },
    {
        "NO": 4,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "700-4001-200",
        "DESCRIPTION": "HVPS, 1200V, 4KJ/SEC, CYNERGY",
        "QTY": 1
    },
    {
        "NO": 5,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "700-4001-200",
        "DESCRIPTION": "HVPS, 1200V, 4KJ/SEC, CYNERGY",
        "QTY": 1
    },
    {
        "NO": 6,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7026-100",
        "DESCRIPTION": "SCULPSURE APPLCATR W/ BOX & OVERPACK",
        "QTY": 1
    },
    {
        "NO": 7,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7026-100",
        "DESCRIPTION": "SCULPSURE APPLCATR W/ BOX & OVERPACK",
        "QTY": 1
    },
    {
        "NO": 8,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "S100-7002-030",
        "DESCRIPTION": "CAPACITOR BANK, CYNERGY",
        "QTY": 1
    },
    {
        "NO": 9,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "S100-7002-030",
        "DESCRIPTION": "CAPACITOR BANK, CYNERGY",
        "QTY": 1
    },
    {
        "NO": 10,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "S100-7002-030",
        "DESCRIPTION": "CAPACITOR BANK, CYNERGY",
        "QTY": 1
    },
    {
        "NO": 11,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "710-0138-110",
        "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE",
        "QTY": 1
    },
    {
        "NO": 12,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "710-0138-110",
        "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE",
        "QTY": 1
    },
    {
        "NO": 13,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "710-0138-110",
        "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE",
        "QTY": 1
    },
    {
        "NO": 14,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "710-0138-110",
        "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE",
        "QTY": 1
    },
    {
        "NO": 15,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "105-9050",
        "DESCRIPTION": "MIRROR 1\" TRIPLE PEAK, ROHS",
        "QTY": 14
    },
    {
        "NO": 16,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "S100-7009-090",
        "DESCRIPTION": "CAPASITOR BANK, ELITE",
        "QTY": 1
    },
    {
    "NO": 17,
    "PRINCIPAL": "CYNOSURE",
    "PART NUMBER": "100-7017-016",
    "DESCRIPTION": "ASSY, SHG, REVLITE/MEDLITE",
    "QTY": 1,
    "Qty_Buyback": 1,
    "Status": "Sudah",
    "Tanggal_Buyback": datetime.date(2025, 9, 4),  # update ke tanggal hari ini
    "Catatan": "Untuk PO di Bamed Clinic Menteng"
    },
    {
        "NO": 18,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7017-016",
        "DESCRIPTION": "ASSY, SHG, REVLITE/MEDLITE",
        "QTY": 1
    },
    {
        "NO": 19,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7017-016",
        "DESCRIPTION": "ASSY, SHG, REVLITE/MEDLITE",
        "QTY": 1
    },
    {
        "NO": 20,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-052",
        "DESCRIPTION": "HANDPIECE 10 MM",
        "QTY": 2
    },
    {
        "NO": 21,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "809-5000-033",
        "DESCRIPTION": "EYEWEAR, ALEX 755NM, ND:YAG (1064NM, RB) (OPERATOR)",
        "QTY": 4
    },
    {
        "NO": 22,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "312-9005",
        "DESCRIPTION": "EYEWEAR 532/1064NM OD7+ CEW NO LATEXROHS (MEDLITE/REVLITE)",
        "QTY": 4
    },
    {
        "NO": 23,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-064",
        "DESCRIPTION": "SPACER ZOOM HANDPIECE",
        "QTY": 7
    },
    {
        "NO": 24,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "710-0172-200",
        "DESCRIPTION": "ASSY PCB,  CAP BANK",
        "QTY": 1
    },
    {
        "NO": 25,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-053",
        "DESCRIPTION": "HANDPIECE 8 MM",
        "QTY": 1
    },
    {
        "NO": 26,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "805-1854-005",
        "DESCRIPTION": "LENS, PL/CX, 18X45FL, 585, 755, 1064, ROHS",
        "QTY": 10
    },
    {
        "NO": 27,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "805-1575-005",
        "DESCRIPTION": "LENS, PL/CX, 15X75FL, 585, 755, 1064, ROHS",
        "QTY": 10
    },
    {
        "NO": 28,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7002-390",
        "DESCRIPTION": "BEAM COMBINER BEAM BLOCK",
        "QTY": 4
    },
    {
        "NO": 29,
    "PRINCIPAL": "CYNOSURE",
    "PART NUMBER": "809-5000-000",
    "DESCRIPTION": "PATIENT EYESHIELD, RB",
    "QTY": 5,
    "Qty_Buyback": 1,
    "Status": "Sudah",
    "Tanggal_Buyback": datetime.date(2025, 3, 6),
    "Catatan": "Untuk Erha Clinic Samarinda"
    },
    {
        "NO": 30,
    "PRINCIPAL": "CYNOSURE",
    "PART NUMBER": "100-7017-069",
    "DESCRIPTION": "HDT PROTECTIVE WNDW ADJ HNDPC 7.5\"",
    "QTY": 4,
    "Qty_Buyback": 2,
    "Status": "Sudah",
    "Tanggal_Buyback": datetime.date(2025, 3, 6),
    "Catatan": "Untuk team PM"
    },
    {
        "NO": 31,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "805-1836-005",
        "DESCRIPTION": "LENS, PL/CX, 18X36FL, 585, 755, 1064, ROHS",
        "QTY": 9
    },
    {
        "NO": 32,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "102-0189",
        "DESCRIPTION": "LENS,  +60MM X 20MM DIA, ROHS 2 (HF I)",
        "QTY": 5
    },
    {
        "NO": 33,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "656-0305",
        "DESCRIPTION": "WASH BOTTLE 1L",
        "QTY": 3
    },
    {
        "NO": 34,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "805-1224-005",
        "DESCRIPTION": "LENS, PL/CX, 12X24FL, 585, 755, 1064, ROHS",
        "QTY": 8
    },
    {
        "NO": 35,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "805-1248-005",
        "DESCRIPTION": "LENS, PL/CX, 12X48FL, 585, 755, 1064, ROHS",
        "QTY": 8
    },
    {
        "NO": 36,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "312-9100",
        "DESCRIPTION": "FILTER, WATER, ROHS",
        "QTY": 7
    },
    {
        "NO": 37,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "805-1530-005",
        "DESCRIPTION": "LENS, PL/CX, 15X30FL, 585, 755, 1064, ROHS",
        "QTY": 9
    },
    {
        "NO": 38,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-056",
        "DESCRIPTION": "SPACER FIXED HANDPIECE",
        "QTY": 2
    },
    {
        "NO": 39,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "990-8006-200",
        "DESCRIPTION": "FLASHLAMP, LIN, 6\"ARC, 7X9MM, 200T (PDL)",
        "QTY": 1
    },
    {
        "NO": 40,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "990-8006-200",
        "DESCRIPTION": "FLASHLAMP, LIN, 6\"ARC, 7X9MM, 200T (PDL)",
        "QTY": 1
    },
    {
        "NO": 41,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "429-0207-9",
        "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS",
        "QTY": 1
    },
    {
        "NO": 42,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "429-0207-9",
        "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS",
        "QTY": 1
    },
    {
        "NO": 43,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "429-0207-9",
        "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS",
        "QTY": 1
    },
    {
        "NO": 44,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "429-0207-9",
        "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS",
        "QTY": 1
    },
    {
        "NO": 45,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "313-0099",
        "DESCRIPTION": "DI FILTER, ARROWHD #CAPSULE, ROHS",
        "QTY": 13
    },
    {
        "NO": 46,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "130-7002-089",
        "DESCRIPTION": "SHUTTER MOUNT, BEAM BLOCK, CYNERGY",
        "QTY": 5
    },
    {
        "NO": 47,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7026-061",
        "DESCRIPTION": "ASSY, LUX LOTION KIT, SINGLE",
        "QTY": 3
    },
    {
        "NO": 48,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "130-7002-093",
        "DESCRIPTION": "SHUTTER, BEAM BLOCK, CYNERGY, ROHS",
        "QTY": 5
    },
    {
        "NO": 49,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-1754-150",
        "DESCRIPTION": "HANDPIECE 15MM",
        "QTY": 7
    },
    {
        "NO": 50,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-1757-070",
        "DESCRIPTION": "HANDPIECE 7MM",
        "QTY": 1
    },
    {
        "NO": 51,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-040",
        "DESCRIPTION": "ASSY, OPTICAL MOUNT, PICOSURE, HMR",
        "QTY": 3
    },
    {
        "NO": 52,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-105",
        "DESCRIPTION": "ASSY, OPTICAL MOUNT, PICOSURE, PCMR",
        "QTY": 3
    },
    {
        "NO": 53,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-532",
        "DESCRIPTION": "PICOSURE 532DS",
        "QTY": 1
    },
    {
        "NO": 54,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-532",
        "DESCRIPTION": "PICOSURE 532DS",
        "QTY": 1
    },
    {
        "NO": 55,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "130-7051-190",
        "DESCRIPTION": "TRAY, REMOVABLE, TOP CVR, PICO300",
        "QTY": 7
    },
    {
        "NO": 56,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "656-1000",
        "DESCRIPTION": "HANDPIECE RL SI",
        "QTY": 1
    },
    {
        "NO": 57,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "661-0069",
        "DESCRIPTION": "HANDPIECE ADAPTER RL SI",
        "QTY": 1
    },
    {
        "NO": 58,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 59,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 60,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 61,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 62,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 63,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    }
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
st.markdown('<div class="gradient-bg"><h1>🔄 IDSMED - Mediva</h1><h2>IDSMED–Mediva Spare Parts Buyback Tracking System</h2><p>Lokasi: Logos - Managed by Akmaludin Agustian for Heru Utomo</p></div>', unsafe_allow_html=True)

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
    st.markdown('<div class="sidebar-content"><h3 style="color: #667eea;">Filter & Aksi</h3>', unsafe_allow_html=True)
    status_opt = st.selectbox("Status", ["Semua", "Belum", "Sudah"], index=0)
    search = st.text_input("Cari (bebas: nama/serial/kode)", "")
    st.caption("Pencarian diterapkan ke semua kolom teks.")
    st.markdown("---")
    st.write("**Kolom yang bisa diedit:** Status, Tanggal Buyback, Catatan, Qty Buyback")
    st.write("**Kolom otomatis:** Sisa Qty (QTY - Qty Buyback)")
    st.markdown("---")
    st.caption("Tip: Klik header kolom untuk sort / filter tambahan.")
    st.markdown('</div>', unsafe_allow_html=True)
with st.sidebar:
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
st.markdown("<hr><div style='text-align:center;'><p>© 2025 IDSMED - Mediva Buyback Tracking System</p></div>", unsafe_allow_html=True)
