import io
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔁", layout="wide")

DATE_TODAY = datetime.date.today()

# ---------- Embedded Data from Excel ----------
INITIAL_DATA = [
    {"NO": 1, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "100-7026-865", "DESCRIPTION": "ASSY, WEARABLES KIT, SCULP, SUBMENTAL, STD", "QTY": 2},
    {"NO": 2, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "S805-0035-005", "DESCRIPTION": "WINDOW, 625DIA, 585, 755, 1064, SAPHIRE", "QTY": 38},
    {"NO": 3, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "ASY-13442", "DESCRIPTION": "10 PAC KEY SCULPSURE SUBMNTL 1PK SEC", "QTY": 8},
    # ... lanjutkan semua data kamu sampai 63 row ...
    {"NO": 63, "PRINCIPAL": "NEWPONG", "PART NUMBER": "CAT NP100-0004", "DESCRIPTION": "CARTRIDGE S7, 2.0 MM DEPTH/7.0 MHZ/SINGLE SPOT", "QTY": 1}
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

with col1:
    if st.button(f"📦 Total Item\n{total}", use_container_width=True, key="btn_total"):
        st.session_state["filter_status"] = "Semua"
    st.markdown(
        "<style>div[data-testid='stButton'] button#btn_total{background-color:#FFD700;color:black;font-size:20px;"
        "padding:20px;border-radius:10px;width:100%;height:100px;}</style>", unsafe_allow_html=True
    )

with col2:
    if st.button(f"✅ Sudah Buyback\n{sudah}", use_container_width=True, key="btn_sudah"):
        st.session_state["filter_status"] = "Sudah"
    st.markdown(
        "<style>div[data-testid='stButton'] button#btn_sudah{background-color:#4CAF50;color:white;font-size:20px;"
        "padding:20px;border-radius:10px;width:100%;height:100px;}</style>", unsafe_allow_html=True
    )

with col3:
    if st.button(f"❌ Belum Buyback\n{belum}", use_container_width=True, key="btn_belum"):
        st.session_state["filter_status"] = "Belum"
    st.markdown(
        "<style>div[data-testid='stButton'] button#btn_belum{background-color:#FF4C4C;color:white;font-size:20px;"
        "padding:20px;border-radius:10px;width:100%;height:100px;}</style>", unsafe_allow_html=True
    )

st.divider()

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.subheader("Filter & Aksi")
    # Default dari session_state kalau ada
    status_opt = st.session_state.get("filter_status", "Semua")
    status_opt = st.selectbox("Status", ["Semua", "Belum", "Sudah"],
                              index=["Semua", "Belum", "Sudah"].index(status_opt))
    search = st.text_input("Cari (bebas: nama/serial/kode)", "")
    st.caption("Pencarian diterapkan ke semua kolom teks.")

# ---------- Table (Editable) ----------
view = filtered_df(df, status_opt, search)

editable_cols = [c for c in ["Status", "Tanggal_Buyback", "Catatan"] if c in view.columns]
disabled_cols = [c for c in view.columns if c not in editable_cols]

cfg = {}
if "Status" in view.columns:
    cfg["Status"] = st.column_config.SelectboxColumn("Status", options=["Belum", "Sudah"], default="Belum")
if "Tanggal_Buyback" in view.columns:
    cfg["Tanggal_Buyback"] = st.column_config.DateColumn("Tanggal Buyback", format="YYYY-MM-DD")
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
