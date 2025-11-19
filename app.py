import numpy as np
import io
import datetime
import pandas as pd
import streamlit as st

# ================== Page Config ==================
st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔄", layout="wide")
DATE_TODAY = datetime.date.today()

# ================== Global Styles (IDsMED Blue) ==================
st.markdown("""
<style>
/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background: #f5f8ff; /* very light blue */
    font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* Header (IDsMED blue gradient) */
.hero {
    background: linear-gradient(135deg, #005AA9 0%, #1E88E5 100%);
    color: white;
    padding: 26px 28px;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    margin-bottom: 18px;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.06);
    border: 1px solid #e7f0ff; /* blue-ish border */
}
.metric-title { color: #5b6b7f; font-size: 13px; margin: 0 0 6px 0; }
.metric-value { color: #0f172a; font-weight: 700; font-size: 24px; margin: 0; }

/* Progress bar - blue */
.progress {
    width: 100%;
    height: 12px;
    background: #eaf2ff;
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid #d8e7ff;
}
.progress > span {
    display: block;
    height: 100%;
    background: linear-gradient(90deg, #38BDF8, #1E40AF);
}

/* Chips */
.chips { display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
    display: inline-block;
    padding: 4px 10px;
    font-size: 12px;
    border-radius: 999px;
    border: 1px solid transparent;
}
.chip-gray  { background: #f3f4f6; color: #374151; border-color: #e5e7eb; }           /* Belum */
.chip-cyan  { background: #ecfeff; color: #0e7490; border-color: #a5f3fc; }           /* Sudah sebagian */
.chip-blue  { background: #e6f2ff; color: #0b5cab; border-color: #b5daff; }           /* Sudah */

/* Sidebar */
.sidebar-box {
    background: linear-gradient(180deg, #f7fbff 0%, #eef6ff 100%);
    border: 1px solid #e0eeff;
    border-radius: 14px;
    padding: 14px;
}

/* Buttons (primary) */
.stButton > button, .stDownloadButton > button {
    background-color: #1E88E5 !important;
    color: #ffffff !important;
    border: 1px solid #1E88E5 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #1565C0 !important;
    border-color: #1565C0 !important;
}

/* Inputs focus */
input:focus, textarea:focus, select:focus {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(30,136,229,0.25) !important;
}

/* Detail card */
.detail-card {
    background: #ffffff;
    border: 1px solid #e7f0ff;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
.detail-title { font-weight: 700; color: #0b5cab; margin-bottom: 4px; }
.detail-sub { color: #5b6b7f; font-size: 12px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ================== Embedded Data ==================
INITIAL_DATA = [
    {"NO": 1, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7026-865", "DESCRIPTION": "ASSY, WEARABLES KIT, SCULP, SUBMENTAL, STD", "QTY": 2},
    {"NO": 2, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "S805-0035-005", "DESCRIPTION": "WINDOW, 625DIA, 585, 755, 1064, SAPHIRE", "QTY": 38},
    {"NO": 3, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "ASY-13442", "DESCRIPTION": "10 PAC KEY SCULPSURE SUBMNTL 1PK SEC", "QTY": 8},
    {"NO": 4, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "700-4001-200", "DESCRIPTION": "HVPS, 1200V, 4KJ/SEC, CYNERGY", "QTY": 1},
    {"NO": 5, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "700-4001-200", "DESCRIPTION": "HVPS, 1200V, 4KJ/SEC, CYNERGY", "QTY": 1},
    {"NO": 6, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7026-100", "DESCRIPTION": "SCULPSURE APPLCATR W/ BOX & OVERPACK", "QTY": 1},
    {"NO": 7, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7026-100", "DESCRIPTION": "SCULPSURE APPLCATR W/ BOX & OVERPACK", "QTY": 1},
    {"NO": 8, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "S100-7002-030", "DESCRIPTION": "CAPACITOR BANK, CYNERGY", "QTY": 1},
    {"NO": 9, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "S100-7002-030", "DESCRIPTION": "CAPACITOR BANK, CYNERGY", "QTY": 1},
    {"NO": 10, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "S100-7002-030", "DESCRIPTION": "CAPACITOR BANK, CYNERGY", "QTY": 1},
    {"NO": 11, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "710-0138-110", "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE", "QTY": 1},
    {"NO": 12, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "710-0138-110", "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE", "QTY": 1},
    {"NO": 13, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "710-0138-110", "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE", "QTY": 1},
    {"NO": 14, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "710-0138-110", "DESCRIPTION": "ASSY PCB, ETX COMPUTER INTERFACE", "QTY": 1},
    {"NO": 15, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "105-9050", "DESCRIPTION": "MIRROR 1\" TRIPLE PEAK, ROHS", "QTY": 14},
    {"NO": 16, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "S100-7009-090", "DESCRIPTION": "CAPASITOR BANK, ELITE", "QTY": 1},
    {
        "NO": 17, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7017-016",
        "DESCRIPTION": "ASSY, SHG, REVLITE/MEDLITE", "QTY": 1,
        "Qty_Buyback": 1, "Status": "Sudah",
        "Tanggal_Buyback": datetime.date(2025, 9, 4),
        "Catatan": "Untuk Bamed Clinic Menteng"
    },
    {"NO": 18, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7017-016", "DESCRIPTION": "ASSY, SHG, REVLITE/MEDLITE", "QTY": 1},
    {"NO": 19, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7017-016", "DESCRIPTION": "ASSY, SHG, REVLITE/MEDLITE", "QTY": 1},
    {"NO": 20, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-052", "DESCRIPTION": "HANDPIECE 10 MM", "QTY": 2},
    {"NO": 21, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "809-5000-033", "DESCRIPTION": "EYEWEAR, ALEX 755NM, ND:YAG (1064NM, RB) (OPERATOR)", "QTY": 4},
    {"NO": 22, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "312-9005", "DESCRIPTION": "EYEWEAR 532/1064NM OD7+ CEW NO LATEXROHS (MEDLITE/REVLITE)", "QTY": 4},
    {"NO": 23, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-064", "DESCRIPTION": "SPACER ZOOM HANDPIECE", "QTY": 7},
    {"NO": 24, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "710-0172-200", "DESCRIPTION": "ASSY PCB,  CAP BANK", "QTY": 1},
    {"NO": 25, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-053", "DESCRIPTION": "HANDPIECE 8 MM", "QTY": 1},
    {"NO": 26, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "805-1854-005", "DESCRIPTION": "LENS, PL/CX, 18X45FL, 585, 755, 1064, ROHS", "QTY": 10},
    {"NO": 27, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "805-1575-005", "DESCRIPTION": "LENS, PL/CX, 15X75FL, 585, 755, 1064, ROHS", "QTY": 10},
    {"NO": 28, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7002-390", "DESCRIPTION": "BEAM COMBINER BEAM BLOCK", "QTY": 4},
    {
        "NO": 29, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "809-5000-000",
        "DESCRIPTION": "PATIENT EYESHIELD, RB", "QTY": 5,
        "Qty_Buyback": 3,  # total sudah dibuyback 3 pcs
        "Status": "Sudah sebagian",
        "Tanggal_Buyback": DATE_TODAY,  # transaksi terakhir (Arayu) = hari ini
        "Catatan": "Riwayat: 1 pc Erha (2025-03-06), 1 pc Arayu (hari ini), 1 pc (detail menyusul)",
        # Riwayat per transaksi untuk tampilan detail & ekspor History
        "Buyback_History": [
            {"Tanggal": datetime.date(2025, 3, 6), "Qty": 1, "Ke": "Erha Clinic Samarinda", "Catatan": ""},
            {"Tanggal": DATE_TODAY, "Qty": 1, "Ke": "Arayu Clinic Makassar", "Catatan": ""},
            # 1 pc tambahan sudah tercatat di Qty_Buyback namun detail menyusul
        ]
    },
    {
        "NO": 30, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7017-069",
        "DESCRIPTION": "HDT PROTECTIVE WNDW ADJ HNDPC 7.5\"",
        "QTY": 4, "Qty_Buyback": 2, "Status": "Sudah",
        "Tanggal_Buyback": datetime.date(2025, 3, 6), "Catatan": "Untuk team PM"
    },
    {"NO": 31, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "805-1836-005", "DESCRIPTION": "LENS, PL/CX, 18X36FL, 585, 755, 1064, ROHS", "QTY": 9},
    {"NO": 32, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "102-0189", "DESCRIPTION": "LENS,  +60MM X 20MM DIA, ROHS 2 (HF I)", "QTY": 5},
    {"NO": 33, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "656-0305", "DESCRIPTION": "WASH BOTTLE 1L", "QTY": 3},
    {"NO": 34, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "805-1224-005", "DESCRIPTION": "LENS, PL/CX, 12X24FL, 585, 755, 1064, ROHS", "QTY": 8},
    {"NO": 35, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "805-1248-005", "DESCRIPTION": "LENS, PL/CX, 12X48FL, 585, 755, 1064, ROHS", "QTY": 8},
    {"NO": 36, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "312-9100", "DESCRIPTION": "FILTER, WATER, ROHS", "QTY": 7},
    {"NO": 37, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "805-1530-005", "DESCRIPTION": "LENS, PL/CX, 15X30FL, 585, 755, 1064, ROHS", "QTY": 9},
    {"NO": 38, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-056", "DESCRIPTION": "SPACER FIXED HANDPIECE", "QTY": 2},
    {"NO": 39, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "990-8006-200", "DESCRIPTION": "FLASHLAMP, LIN, 6\"ARC, 7X9MM, 200T (PDL)", "QTY": 1},
    {"NO": 40, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "990-8006-200", "DESCRIPTION": "FLASHLAMP, LIN, 6\"ARC, 7X9MM, 200T (PDL)", "QTY": 1},
    {"NO": 41, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "429-0207-9", "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS", "QTY": 1},
    {"NO": 42, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "429-0207-9", "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS", "QTY": 1},
    {"NO": 43, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "429-0207-9", "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS", "QTY": 1},
    {"NO": 44, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "429-0207-9", "DESCRIPTION": "ASSY LASER FOOTSWITCH ROHS", "QTY": 1},
    {"NO": 45, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "313-0099", "DESCRIPTION": "DI FILTER, ARROWHD #CAPSULE, ROHS", "QTY": 13},
    {"NO": 46, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "130-7002-089", "DESCRIPTION": "SHUTTER MOUNT, BEAM BLOCK, CYNERGY", "QTY": 5},
    {"NO": 47, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7026-061", "DESCRIPTION": "ASSY, LUX LOTION KIT, SINGLE", "QTY": 3},
    {"NO": 48, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "130-7002-093", "DESCRIPTION": "SHUTTER, BEAM BLOCK, CYNERGY, ROHS", "QTY": 5},
    {"NO": 49, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-1754-150", "DESCRIPTION": "HANDPIECE 15MM", "QTY": 7},
    {"NO": 50, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-1757-070", "DESCRIPTION": "HANDPIECE 7MM", "QTY": 1},
    {"NO": 51, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-040", "DESCRIPTION": "ASSY, OPTICAL MOUNT, PICOSURE, HMR", "QTY": 3},
    {"NO": 52, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-105", "DESCRIPTION": "ASSY, OPTICAL MOUNT, PICOSURE, PCMR", "QTY": 3},
    {"NO": 53, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-532", "DESCRIPTION": "PICOSURE 532DS", "QTY": 1},
    {"NO": 54, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7012-532", "DESCRIPTION": "PICOSURE 532DS", "QTY": 1},
    {"NO": 55, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "130-7051-190", "DESCRIPTION": "TRAY, REMOVABLE, TOP CVR, PICO300", "QTY": 7},
    {"NO": 56, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "656-1000", "DESCRIPTION": "HANDPIECE RL SI", "QTY": 1},
    {"NO": 57, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "661-0069", "DESCRIPTION": "HANDPIECE ADAPTER RL SI", "QTY": 1},
    {"NO": 58, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1},
    {"NO": 59, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1},
    {"NO": 60, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1},
    {"NO": 61, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1},
    {"NO": 62, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1},
    {"NO": 63, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1},
]

# ================== Helpers ==================
def ensure_history_list(x):
    # pastikan Buyback_History adalah list of dict
    if isinstance(x, list):
        return x
    return []

def update_status(df: pd.DataFrame) -> pd.DataFrame:
    df["Qty_Buyback"] = df.get("Qty_Buyback", 0).fillna(0).astype(int)
    # Ambil tanggal terakhir dari history kalau ada
    if "Buyback_History" in df.columns:
        last_dates = []
        for _, r in df.iterrows():
            hist = ensure_history_list(r.get("Buyback_History"))
            dates = [h.get("Tanggal") for h in hist if h.get("Tanggal") is not None]
            last_dates.append(max(dates) if dates else r.get("Tanggal_Buyback"))
        df["Tanggal_Buyback"] = last_dates
    df["Tanggal_Buyback"] = pd.to_datetime(df["Tanggal_Buyback"], errors="coerce").dt.date
    df["Sisa_Qty"] = (df["QTY"] - df["Qty_Buyback"]).clip(lower=0).astype(int)
    conditions = [
        (df["Qty_Buyback"] == 0),
        (df["Qty_Buyback"] > 0) & (df["Sisa_Qty"] > 0),
        (df["Sisa_Qty"] == 0),
    ]
    choices = ["Belum", "Sudah sebagian", "Sudah"]
    df["Status"] = pd.Categorical(np.select(conditions, choices, default="Belum"),
                                  categories=choices, ordered=True)
    return df

def load_data() -> pd.DataFrame:
    df = pd.DataFrame(INITIAL_DATA)
    for col, default in [("Status", "Belum"), ("Tanggal_Buyback", pd.NaT), ("Catatan", ""), ("Qty_Buyback", 0), ("Buyback_History", None)]:
        if col not in df.columns: df[col] = default
    df["Tanggal_Buyback"] = pd.to_datetime(df["Tanggal_Buyback"], errors="coerce").dt.date
    df = df.reset_index(drop=True)
    df.insert(0, "_ROW_ID", range(1, len(df)+1))
    df = update_status(df)
    return df

def build_progress_html(pct: float) -> str:
    pct = max(0.0, min(pct, 1.0))
    pct_txt = f"{int(pct*100)}%"
    return f'''
    <div class="progress"><span style="width:{pct*100:.2f}%"></span></div>
    <div style="font-size:12px;color:#5b6b7f;margin-top:6px;">Progress Buyback: <b>{pct_txt}</b></div>
    '''

def flatten_history(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        hist = ensure_history_list(r.get("Buyback_History"))
        known_sum = 0
        for h in hist:
            rows.append({
                "NO": r["NO"],
                "PRINCIPAL": r["PRINCIPAL"],
                "PART NUMBER": r["PART NUMBER"],
                "DESCRIPTION": r["DESCRIPTION"],
                "Tanggal": h.get("Tanggal"),
                "Qty": h.get("Qty", 0),
                "Ke": h.get("Ke", ""),
                "Catatan": h.get("Catatan", ""),
            })
            known_sum += h.get("Qty", 0) or 0
        # Jika Qty_Buyback > total dari history, tampilkan baris placeholder agar konsisten dibaca
        diff = int(r.get("Qty_Buyback", 0)) - known_sum
        if diff > 0:
            rows.append({
                "NO": r["NO"],
                "PRINCIPAL": r["PRINCIPAL"],
                "PART NUMBER": r["PART NUMBER"],
                "DESCRIPTION": r["DESCRIPTION"],
                "Tanggal": r.get("Tanggal_Buyback"),
                "Qty": diff,
                "Ke": "Belum ditentukan (detail menyusul)",
                "Catatan": "",
            })
    out = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["NO","PRINCIPAL","PART NUMBER","DESCRIPTION","Tanggal","Qty","Ke","Catatan"])
    if not out.empty:
        out["Tanggal"] = pd.to_datetime(out["Tanggal"], errors="coerce").dt.date
        out = out.sort_values(["NO", "Tanggal"], ascending=[True, True], na_position="last")
    return out

def write_excel_to_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    hist = flatten_history(df)
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        export_df = df.drop(columns=["_ROW_ID"], errors="ignore").copy()
        export_df.to_excel(writer, index=False, sheet_name="Data")
        if not hist.empty:
            hist.to_excel(writer, index=False, sheet_name="History")
    buf.seek(0)
    return buf.read()

# ================== Data ==================
df = load_data()

# ================== Header ==================
st.markdown(f"""
<div class="hero">
  <h1 style="margin:0 0 6px 0;">🔄 IDSMED - Mediva</h1>
  <div style="opacity:.95;">IDSMED–Mediva Spare Parts Buyback Tracking System · Location: Logos · Managed by Akmaludin Agustian for Heru Utomo</div>
</div>
""", unsafe_allow_html=True)

# ================== KPI & Progress ==================
total_item = len(df)
total_qty = int(df["QTY"].sum())
total_qty_buyback = int(df["Qty_Buyback"].sum())
total_sisa_qty = int(df["Sisa_Qty"].sum())
progress = (total_qty_buyback / total_qty) if total_qty else 0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><div class="metric-title">Total Line</div><div class="metric-value">'
                f'{total_item}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><div class="metric-title">Total Qty</div><div class="metric-value">'
                f'{total_qty}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><div class="metric-title">Buyback Qty</div><div class="metric-value">'
                f'{total_qty_buyback}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><div class="metric-title">Sisa Qty</div><div class="metric-value">'
                f'{total_sisa_qty}</div></div>', unsafe_allow_html=True)

st.markdown(build_progress_html(progress), unsafe_allow_html=True)

# Legend chips (biru)
st.markdown("""
<div class="chips" style="margin: 6px 0 2px 0;">
  <span class="chip chip-gray">Belum</span>
  <span class="chip chip-cyan">Sudah sebagian</span>
  <span class="chip chip-blue">Sudah</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ================== Sidebar Filters ==================
with st.sidebar:
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.subheader("Filter")
    q = st.text_input("Cari (bebas: nama/serial/kode)", "", key="q",
                      placeholder="Contoh: eyeshield / 809-5000 / Medlite")
    status_options = ["Belum", "Sudah sebagian", "Sudah"]
    status_filter = st.multiselect("Status", options=status_options, default=[], key="status_filter")
    only_outstanding = st.toggle("Outstanding saja (Sisa > 0)", value=False, key="only_outstanding")
    sort_by = st.selectbox(
        "Urutkan",
        ["Default (NO)", "Sisa Qty ↓", "Buyback Qty ↓", "Tanggal Buyback ↓", "Principal + Part Number"],
        index=0, key="sort_by"
    )

    colr1, colr2 = st.columns(2)
    with colr1:
        reset = st.button("Reset filter")
    with colr2:
        st.markdown("")  # spacer
    if reset:
        st.session_state.q = ""
        st.session_state.status_filter = []
        st.session_state.only_outstanding = False
        st.session_state.sort_by = "Default (NO)"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================== Apply Filters ==================
view = df.copy()

# Status filter
if status_filter:
    view = view[view["Status"].astype(str).isin(status_filter)]

# Search filter (di semua kolom object/string)
if q:
    mask = pd.Series(False, index=view.index)
    for col in view.columns:
        if view[col].dtype == "O":
            mask = mask | view[col].fillna("").astype(str).str.contains(q, case=False, na=False)
    view = view[mask]

# Outstanding filter
if only_outstanding:
    view = view[view["Sisa_Qty"] > 0]

# Sorting
if sort_by == "Sisa Qty ↓":
    view = view.sort_values(["Sisa_Qty", "QTY"], ascending=[False, False])
elif sort_by == "Buyback Qty ↓":
    view = view.sort_values(["Qty_Buyback", "QTY"], ascending=[False, False])
elif sort_by == "Tanggal Buyback ↓":
    view = view.sort_values("Tanggal_Buyback", ascending=False, na_position="last")
elif sort_by == "Principal + Part Number":
    view = view.sort_values(["PRINCIPAL", "PART NUMBER"], ascending=[True, True])
else:
    view = view.sort_values("NO", ascending=True)

# ================== Tabs ==================
tab1, tab2 = st.tabs(["📋 List Data", "📈 Ringkasan"])

with tab1:
    st.subheader("Data Buyback")

    left, right = st.columns([0.68, 0.32], gap="large")

    with left:
        # Simpan _ROW_ID untuk sinkron update
        row_ids = view["_ROW_ID"].copy()

        # Tampilkan tanpa kolom _ROW_ID & Buyback_History
        view_display = view.drop(columns=["_ROW_ID", "Buyback_History"], errors="ignore").copy()

        # Kolom editable (kita biarkan Qty_Buyback editable, Tanggal & Catatan juga)
        editable_cols = ["Qty_Buyback", "Tanggal_Buyback", "Catatan"]

        # Konfigurasi kolom
        cfg = {}
        for col in view_display.columns:
            disabled = col not in editable_cols
            if col in ["QTY", "Qty_Buyback", "Sisa_Qty", "NO"]:
                cfg[col] = st.column_config.NumberColumn(
                    col if col != "Sisa_Qty" else "Sisa Qty",
                    disabled=disabled,
                    min_value=0,
                    step=1,
                    help=("Jumlah unit tersedia" if col == "QTY" else
                          "Jumlah sudah dibuyback (bisa disesuaikan cepat)" if col == "Qty_Buyback" else
                          "Sisa unit yang belum dibuyback (otomatis)" if col == "Sisa_Qty" else "")
                )
            elif col == "Tanggal_Buyback":
                cfg[col] = st.column_config.DateColumn("Tanggal Buyback", format="YYYY-MM-DD", disabled=disabled)
            else:
                label = col
                if col == "PART NUMBER": label = "Part Number"
                if col == "DESCRIPTION": label = "Description"
                if col == "PRINCIPAL": label = "Principal"
                cfg[col] = st.column_config.TextColumn(label, disabled=disabled)

        # Render editor
        edited = st.data_editor(
            view_display,
            use_container_width=True,
            hide_index=True,
            column_config=cfg,
            num_rows="fixed",
            key="editor"
        )

        # Tambahkan kembali _ROW_ID untuk update
        edited["_ROW_ID"] = row_ids.values

        # Validasi
        invalid_rows = edited[edited["Qty_Buyback"] > edited["QTY"]]
        if not invalid_rows.empty:
            st.warning("⚠️ Ada baris dengan Qty Buyback melebihi QTY. Mohon koreksi nilainya.", icon="⚠️")

        # Apply Changes (hanya jika valid)
        if invalid_rows.empty:
            edited["Qty_Buyback"] = edited["Qty_Buyback"].fillna(0).astype(int)
            edited["Sisa_Qty"] = (edited["QTY"] - edited["Qty_Buyback"]).clip(lower=0).astype(int)
            base = df.set_index("_ROW_ID")
            upd = edited.set_index("_ROW_ID")
            for c in ["Qty_Buyback", "Tanggal_Buyback", "Catatan"]:
                if c in upd.columns:
                    base.loc[upd.index, c] = upd[c]
            df = base.reset_index()
            df = update_status(df)

    with right:
        st.markdown('<div class="detail-card">', unsafe_allow_html=True)
        st.markdown('<div class="detail-title">Detail & Riwayat</div>', unsafe_allow_html=True)
        st.markdown('<div class="detail-sub">Pilih item untuk melihat riwayat buyback, tambah transaksi, dan catatan.</div>', unsafe_allow_html=True)

        # Pilihan item untuk detail (default diarahkan ke 809-5000-000 jika ada)
        view_for_select = df.copy()
        view_for_select["Select_Label"] = view_for_select.apply(
            lambda r: f'{r["NO"]}. {r["PART NUMBER"]} — {r["DESCRIPTION"][:38]} (Sisa: {r["Sisa_Qty"]})', axis=1
        )
        default_index = 0
        candidates = view_for_select[view_for_select["PART NUMBER"] == "809-5000-000"]
        if not candidates.empty:
            default_index = candidates.index[0]
        selected_label = st.selectbox(
            "Pilih item",
            options=view_for_select["Select_Label"].tolist(),
            index=default_index if default_index < len(view_for_select) else 0
        )
        sel_row = view_for_select[view_for_select["Select_Label"] == selected_label].iloc[0]

        # Ringkas info
        st.markdown(
            f"- Part Number: {sel_row['PART NUMBER']}\n"
            f"- Description: {sel_row['DESCRIPTION']}\n"
            f"- Qty: {sel_row['QTY']} | Buyback: {sel_row['Qty_Buyback']} | Sisa: {sel_row['Sisa_Qty']}\n"
            f"- Status: {'✅ Sudah' if str(sel_row['Status'])=='Sudah' else '🟡 Sudah sebagian' if str(sel_row['Status'])=='Sudah sebagian' else '⬜ Belum'}\n"
            f"- Tgl terakhir: {sel_row['Tanggal_Buyback'] if pd.notna(pd.to_datetime(sel_row['Tanggal_Buyback'], errors='coerce')) else '-'}",
        )

        # Tampilkan riwayat
        hist_df_all = flatten_history(df)
        hist_sel = hist_df_all[hist_df_all["NO"] == sel_row["NO"]]
        st.markdown(" ")
        st.markdown("Riwayat Buyback")
        if hist_sel.empty:
            st.info("Belum ada riwayat.", icon="ℹ️")
        else:
            st.dataframe(hist_sel[["Tanggal","Qty","Ke","Catatan"]], use_container_width=True, hide_index=True)

        # Form tambah transaksi
        st.markdown("---")
        st.markdown("Tambah Transaksi Buyback")
        with st.form(key="add_tx_form", clear_on_submit=True):
            tgl = st.date_input("Tanggal", value=DATE_TODAY)
            qty = st.number_input("Qty", min_value=1, step=1, value=1)
            tujuan = st.text_input("Ke (nama klinik/customer)", value="")
            cat = st.text_input("Catatan", value="")
            submit_tx = st.form_submit_button("Tambah")

        if submit_tx:
            idx = df[df["NO"] == sel_row["NO"]].index[0]
            hist = ensure_history_list(df.at[idx, "Buyback_History"])
            # Validasi kapasitas sisa
            sisa_sekarang = int(df.at[idx, "Sisa_Qty"])
            if qty > sisa_sekarang:
                st.warning(f"Qty melebihi sisa stok (Sisa saat ini: {sisa_sekarang}).", icon="⚠️")
            else:
                hist.append({"Tanggal": tgl, "Qty": int(qty), "Ke": tujuan.strip(), "Catatan": cat.strip()})
                df.at[idx, "Buyback_History"] = hist
                df.at[idx, "Qty_Buyback"] = int(df.at[idx, "Qty_Buyback"]) + int(qty)
                # Update tanggal terakhir jika lebih baru
                last_dt = df.at[idx, "Tanggal_Buyback"]
                if (pd.isna(pd.to_datetime(last_dt, errors="coerce"))) or (tgl and tgl > last_dt):
                    df.at[idx, "Tanggal_Buyback"] = tgl
                df = update_status(df)
                st.success("Transaksi berhasil ditambahkan.", icon="✅")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Ringkasan")

    # Ringkasan per status
    statuses = ["Belum", "Sudah sebagian", "Sudah"]
    cols = st.columns(3)
    for i, stt in enumerate(statuses):
        subset = df[df["Status"].astype(str) == stt]
        cnt = len(subset)
        sisa = int(subset["Sisa_Qty"].sum()) if not subset.empty else 0
        chip_cls = "chip-gray" if stt == "Belum" else ("chip-cyan" if stt == "Sudah sebagian" else "chip-blue")
        with cols[i]:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-title">Status</div>'
                f'<div class="chips"><span class="chip {chip_cls}">{stt}</span></div>'
                f'<div style="height:10px"></div>'
                f'<div class="metric-title">Total Line</div><div class="metric-value">{cnt}</div>'
                f'<div class="metric-title" style="margin-top:8px;">Sisa Qty</div><div class="metric-value">{sisa}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(" ")
    # Tabel ringkasan agregat
    sum_df = (df.assign(Status=df["Status"].astype(str))
                .groupby("Status", as_index=False)
                .agg(Total_Line=("NO", "count"),
                     Total_Qty=("QTY", "sum"),
                     Buyback_Qty=("Qty_Buyback", "sum"),
                     Sisa_Qty=("Sisa_Qty", "sum"))
                .sort_values("Status"))
    st.dataframe(sum_df, use_container_width=True, hide_index=True)

# ================== Download ==================
st.markdown("### 💾 Download Data")
bytes_xlsx = write_excel_to_bytes(update_status(df.copy()))
st.download_button(
    "⬇️ Download Excel yang sudah diupdate",
    data=bytes_xlsx,
    file_name=f"Data Buyback Mediva - updated {DATE_TODAY}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.markdown("<hr><div style='text-align:center;color:#5b6b7f;'>© 2025 IDSMED - Mediva Buyback Tracking System</div>", unsafe_allow_html=True)
