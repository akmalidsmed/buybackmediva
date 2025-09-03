import io
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔁", layout="wide")

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
    "PRINCIPAL": "CYNOSURE",
    "PART NUMBER": "809-5000-000",
    "DESCRIPTION": "PATIENT EYESHIELD, RB",
    "QTY": 5
  },
  {
    "NO": 30,
    "PRINCIPAL": "CYNOSURE",
    "PART NUMBER": "100-7017-069",
    "DESCRIPTION": "HDT PROTECTIVE WNDW ADJ HNDPC 7.5\"",
    "QTY": 4
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

# ---------- Summary KPI ----------
total = len(df)
sudah = int((df["Status"] == "Sudah").sum())
belum = total - sudah
col1, col2, col3 = st.columns(3)
col1.metric("Total Item", f"{total}")
col2.metric("Sudah Buyback", f"{sudah}")
col3.metric("Belum Buyback", f"{belum}")

st.divider()

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.subheader("Filter & Aksi")
    status_opt = st.selectbox("Status", ["Semua", "Belum", "Sudah"], index=0)
    search = st.text_input("Cari (bebas: nama/serial/kode)", "")
    st.caption("Pencarian diterapkan ke semua kolom teks.")
    st.markdown("---")
    st.write("Kolom yang bisa diedit: **Status**, **Tanggal_Buyback**, **Catatan**.")
    st.markdown("---")
    st.caption("Tip: Klik header kolom untuk sort / filter tambahan.")

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
        "Tanggal Buyback", format="YYYY-MM-DD"
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
