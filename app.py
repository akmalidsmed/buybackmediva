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
        
        /* Metric Cards */
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
        
        /* Sidebar Styling */
        .sidebar-content {
            background: linear-gradient(180deg, #f8f9ff 0%, #e6f3ff 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
        }
        
        /* Table Styling */
        .table-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: bold !important;
        }
        
        /* Button Styling */
        .btn-gradient {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .btn-gradient:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #54a0ff, #2e86de);
        }
        
        /* Main Content */
        .main-content {
            background: linear-gradient(to right, rgba(255,255,255,0.9), rgba(248,250,251,0.9));
            border-radius: 20px;
            padding: 20px;
            margin: 10px;
        }
        
        /* Glow effect for metrics */
        .metric-card:nth-child(1) { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
        .metric-card:nth-child(2) { box-shadow: 0 0 20px rgba(78, 205, 196, 0.3); }
        .metric-card:nth-child(3) { box-shadow: 0 0 20px rgba(84, 160, 255, 0.3); }
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
        "QTY": 1
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
    "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "100-7026-061",
        "DESCRIPTION": "ASSY, LUX LOTION KIT, SINGLE",
        "QTY": 3
    },
    {
        "NO": 30,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "130-7002-093",
        "DESCRIPTION": "SHUTTER, BEAM BLOCK, CYNERGY, ROHS",
        "QTY": 5
    },
    {
        "NO": 31,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-1754-150",
        "DESCRIPTION": "HANDPIECE 15MM",
        "QTY": 7
    },
    {
        "NO": 32,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-1757-070",
        "DESCRIPTION": "HANDPIECE 7MM",
        "QTY": 1
    },
    {
        "NO": 33,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-040",
        "DESCRIPTION": "ASSY, OPTICAL MOUNT, PICOSURE, HMR",
        "QTY": 3
    },
    {
        "NO": 34,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-105",
        "DESCRIPTION": "ASSY, OPTICAL MOUNT, PICOSURE, PCMR",
        "QTY": 3
    },
    {
        "NO": 35,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-532",
        "DESCRIPTION": "PICOSURE 532DS",
        "QTY": 1
    },
    {
        "NO": 36,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "100-7012-532",
        "DESCRIPTION": "PICOSURE 532DS",
        "QTY": 1
    },
    {
        "NO": 37,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "130-7051-190",
        "DESCRIPTION": "TRAY, REMOVABLE, TOP CVR, PICO300",
        "QTY": 7
    },
    {
        "NO": 38,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "656-1000",
        "DESCRIPTION": "HANDPIECE RL SI",
        "QTY": 1
    },
    {
        "NO": 39,
        "PRINCIPAL": "CYNOSURE",
        "PART NUMBER": "661-0069",
        "DESCRIPTION": "HANDPIECE ADAPTER RL SI",
        "QTY": 1
    },
    {
        "NO": 40,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 41,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 42,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 43,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 44,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    },
    {
        "NO": 45,
        "PRINCIPAL": "NEWPONG",
        "PART NUMBER": "CAT NP100-0004",
        "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT",
        "QTY": 1
    }
]

def load_data() -> pd.DataFrame:
    df = pd.DataFrame(INITIAL_DATA)
    # Add buyback tracking columns if not exist
    if "Status" not in df.columns:
        df["Status"] = "Belum"
    if "Tanggal_Buyback" not in df.columns:
        df["Tanggal_Buyback"] = pd.NaT
    if "Catatan" not in df.columns:
        df["Catatan"] = ""
    df["Tanggal_Buyback"] = pd.to_datetime(df["Tanggal_Buyback"], errors="coerce").dt.date
    df = df.reset_index(drop=True)
    df.insert(0, "_ROW_ID", range(1, len(df)+1))
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
st.markdown('<div class="gradient-bg"><h1 style="font-size: 2.5em; margin-bottom: 10px;">🔄 IDSMED - Mediva</h1><h2>Buyback Sparepart Tracking System</h2><p style="margin-top: 10px;">Lokasi: Logos - Managed by Akmaludin Agustian for Heru Utomo</p></div>', unsafe_allow_html=True)

# ---------- Summary KPI ----------
total = len(df)
sudah = int((df["Status"] == "Sudah").sum())
belum = total - sudah

st.markdown('<div class="main-content">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card metric-red"><h3 style="font-size: 2em; margin-bottom: 5px;">{total}</h3><p>Total Item</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card metric-green"><h3 style="font-size: 2em; margin-bottom: 5px;">{sudah}</h3><p>Sudah Buyback</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card metric-blue"><h3 style="font-size: 2em; margin-bottom: 5px;">{belum}</h3><p>Belum Buyback</p></div>', unsafe_allow_html=True)

st.divider()

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.markdown('<div class="sidebar-content"><h3 style="color: #667eea;">Filter & Aksi</h3>', unsafe_allow_html=True)
    status_opt = st.selectbox("Status", ["Semua", "Belum", "Sudah"], index=0)
    search = st.text_input("Cari (bebas: nama/serial/kode)", "")
    st.caption("Pencarian diterapkan ke semua kolom teks.")
    st.markdown("---")
    st.write("Kolom yang bisa diedit: **Status**, **Tanggal_Buyback**, **Catatan**.")
    st.markdown("---")
    st.caption("Tip: Klik header kolom untuk sort / filter tambahan.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Table (Editable) ----------
view = filtered_df(df, status_opt, search)

editable_cols = [c for c in ["Status", "Tanggal_Buyback", "Catatan"] if c in view.columns]
disabled_cols = [c for c in view.columns if c not in editable_cols]

cfg = {}
if "Status" in view.columns:
    cfg["Status"] = st.column_config.SelectboxColumn(
        "Status", options=["Belum", "Sudah"], default="Belum"
    )
if "Tanggal_Buyback" in view.columns:
    cfg["Tanggal_Buyback"] = st.column_config.DateColumn(
        "Tanggal Buyback", format="YYYY-MM-DD", 
        default=None
    )
if "Catatan" in view.columns:
    cfg["Catatan"] = st.column_config.TextColumn("Catatan")

edited = st.data_editor(
    view,
    use_container_width=True,
    hide_index=True,
    disabled=disabled_cols,
    column_config=cfg,
    num_rows="fixed",
    key="editor",
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Apply edits ----------
if not edited.equals(view):
    base = df.set_index("_ROW_ID")
    upd = edited.set_index("_ROW_ID")
    base.update(upd[editable_cols])
    df = base.reset_index()

# ---------- Actions ----------
st.markdown("### Download Data")
bytes_xlsx = write_excel_to_bytes(df)
st.download_button(
    "⬇️ Download Excel yang sudah diupdate",
    data=bytes_xlsx,
    file_name=f"Data Buyback Mediva - updated {DATE_TODAY}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)
st.caption("Gunakan tombol download untuk menyimpan perubahan permanen.")

# ---------- Footer ----------
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <p style="color: #666;">© 2025 IDSMED - Mediva Buyback Tracking System</p>
        <p>Built with ❤️ & 🎨 for colorful tracking experience</p>
    </div>
""", unsafe_allow_html=True)
