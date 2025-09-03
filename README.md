# IDSMED - Mediva Buyback Tracker (Streamlit)

A Streamlit app to track buyback status for items sold to Mediva and being bought back by IDSMED. 
- Edit **Status** (Belum/Sudah), **Tanggal_Buyback**, and **Catatan** directly in the table.
- Save back to Excel locally (if allowed) or download the updated Excel.

## Project structure
```
.
├── app.py
├── index.html                 # Your provided landing design (embedded at the top)
├── data/
│   └── Data Buyback Mediva.xlsx
└── requirements.txt
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud
1. Push this folder to GitHub.
2. Create a new Streamlit app from the repo; set **Main file** to `app.py`.
3. After updates, click **Download Excel** to persist data, or use **Simpan** if running locally.
