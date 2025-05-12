import streamlit as st
import pandas as pd
from io import BytesIO

# --- Sidebar with your photo and credits ---
st.sidebar.image("mohamed_ali.jpg", width=180, caption="Mohamed Ali")
st.sidebar.markdown("""
### Mohamed Ali  
**Pavement Engineer**  
📧 mehap201@gmail.com  
📞 +0966581764292  
[LinkedIn](https://www.linkedin.com/in/mohameddalli)
---
""")

st.set_page_config(
    page_title="BBI - IRI Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("BBI - IRI Analysis")
st.markdown("""
Upload your Excel files containing IRI and BBI data.  
The app will process each file and sheet, and provide summary statistics.
""")

uploaded_files = st.file_uploader(
    "Upload Excel files (.xlsx)", 
    type="xlsx", 
    accept_multiple_files=True
)

def process_file(file):
    results = []
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet, header=3)
        except Exception as e:
            st.warning(f"Error reading sheet {sheet}: {e}")
            continue

        if 'iri' in sheet.lower():
            if 'Average Left\\Right' in df.columns:
                col = 'Average Left\\Right'
                df[col] = pd.to_numeric(df[col], errors='coerce')
                stats = {
                    'Average': df[col].mean(),
                    'Median': df[col].median(),
                    'Highest': df[col].max(),
                    'Lowest': df[col].min()
                }
            else:
                st.warning(f"'Average Left\\Right' column not found in sheet {sheet}")
                continue

        elif 'bbi' in sheet.lower():
            if 'Left' in df.columns and 'Right' in df.columns:
                df['Left'] = pd.to_numeric(df['Left'], errors='coerce')
                df['Right'] = pd.to_numeric(df['Right'], errors='coerce')
                df['Average Left\\Right'] = (df['Left'] + df['Right']) / 2
                col = 'Average Left\\Right'
                stats = {
                    'Average': df[col].mean(),
                    'Median': df[col].median(),
                    'Highest': df[col].max(),
                    'Lowest': df[col].min()
                }
            else:
                st.warning(f"'Left' and/or 'Right' columns not found in sheet {sheet}")
                continue
        else:
            continue

        stats['Sheet'] = sheet
        results.append(stats)
    return results

def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

if uploaded_files:
    all_results = []
    for file in uploaded_files:
        file_results = process_file(file)
        for res in file_results:
            res['Filename'] = file.name
            all_results.append(res)
    if all_results:
        df_results = pd.DataFrame(all_results)
        st.subheader("Summary Table")
        st.dataframe(df_results)
        excel_bytes = to_excel_bytes(df_results)
        st.download_button(
            label="📥 Download Results as Excel",
            data=excel_bytes,
            file_name="bbi_iri_analysis_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No valid data found in uploaded files.")
else:
    st.info("Please upload one or more Excel files to get started.")
