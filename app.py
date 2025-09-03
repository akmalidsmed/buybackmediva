import io
import os
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔁", layout="wide")

DATA_PATH = os.path.join("data", "Data Buyback Mediva.xlsx")
DATE_TODAY = datetime.date.today()

# ---------- Helpers ----------
@st.cache_data(show_spinner=False)
def load_excel(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_excel(path, sheet_name=0, engine="openpyxl", dtype=dict())
    df = ensure_columns(df)
    # attach stable row id
    df = df.reset_index(drop=True)
    df.insert(0, "_ROW_ID", range(1, len(df)+1))
    return df

def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    must_cols = {
        "Status": "Belum",              # 'Belum' | 'Sudah'
        "Tanggal_Buyback": pd.NaT,      # date
        "Catatan": ""                   # free text
    }
    for col, default in must_cols.items():
        if col not in df.columns:
            df[col] = default
    # normalize values
    df["Status"] = df["Status"].fillna("Belum").astype(str)
    df.loc[~df["Status"].isin(["Belum", "Sudah"]), "Status"] = "Belum"
    if "Tanggal_Buyback" in df:
        # coerce to datetime.date
        df["Tanggal_Buyback"] = pd.to_datetime(df["Tanggal_Buyback"], errors="coerce").dt.date
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
        # Drop helper column when exporting
        export_df = df.drop(columns=["_ROW_ID"], errors="ignore")
        export_df.to_excel(writer, index=False, sheet_name="Sheet1")
    buf.seek(0)
    return buf.read()

def save_to_local_file(df: pd.DataFrame, path: str) -> tuple[bool, str]:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            out_df = df.drop(columns=["_ROW_ID"], errors="ignore")
            out_df.to_excel(writer, index=False, sheet_name="Sheet1")
        return True, f"Berhasil menyimpan ke {path}"
    except Exception as e:
        return False, f"Gagal menyimpan ke file: {e}"

# ---------- UI: Header from user's design (index.html) ----------
st.markdown(
    "<style>div.block-container{padding-top:1rem;padding-bottom:2rem;}</style>",
    unsafe_allow_html=True,
)
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_header = f.read()
    st.components.v1.html(html_header, height=250, scrolling=False)
except Exception:
    st.title("🔄 IDSMED - Mediva Buyback Tracker")
    st.caption("Desain HTML tidak ditemukan, menggunakan header default.")

# ---------- Load data ----------
df = load_excel(DATA_PATH)

if df.empty:
    st.warning("File Excel tidak ditemukan atau kosong. Pastikan file ada di `data/Data Buyback Mediva.xlsx`.")
    st.stop()

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
        "Status", options=["Belum", "Sudah"], default="Belum", help="Tandai sebagai 'Sudah' bila item sudah dibuyback."
    )
if "Tanggal_Buyback" in view.columns:
    cfg["Tanggal_Buyback"] = st.column_config.DateColumn(
        "Tanggal Buyback", format="YYYY-MM-DD", help="Tanggal buyback selesai (opsional)."
    )
if "Catatan" in view.columns:
    cfg["Catatan"] = st.column_config.TextColumn("Catatan", help="Catatan tambahan (opsional).")

edited = st.data_editor(
    view,
    use_container_width=True,
    hide_index=True,
    disabled=disabled_cols,
    column_config=cfg,
    num_rows="fixed",
    key="editor",
)

# ---------- Apply edits back to main df ----------
if not edited.equals(view):
    # merge back changes using _ROW_ID
    base = df.set_index("_ROW_ID")
    upd = edited.set_index("_ROW_ID")
    base.update(upd[editable_cols])
    df = base.reset_index()

# ---------- Actions ----------
st.markdown("### Simpan / Unduh")
c1, c2 = st.columns([1,1])

with c1:
    if st.button("💾 Simpan ke file Excel (lokal)", use_container_width=True):
        ok, msg = save_to_local_file(df, DATA_PATH)
        if ok:
            st.success(msg)
            st.toast("Perubahan disimpan ke Excel.", icon="✅")
            # refresh cache
            load_excel.clear()
        else:
            st.error(msg)
            st.info("Jika deploy di Streamlit Cloud, penyimpanan lokal bisa bersifat sementara. Gunakan tombol unduh di samping agar data tidak hilang.")

with c2:
    bytes_xlsx = write_excel_to_bytes(df)
    st.download_button(
        "⬇️ Download Excel yang sudah diupdate",
        data=bytes_xlsx,
        file_name=f"Data Buyback Mediva - updated {DATE_TODAY}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.caption("Pembaruan berlaku pada tabel di atas. Gunakan 'Simpan' untuk menulis ke file, atau 'Download' untuk menyimpan perubahan secara permanen.")
