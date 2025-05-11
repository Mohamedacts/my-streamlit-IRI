import streamlit as st
import pandas as pd

def process_file(file):
    results = []
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet, header=3)
        except Exception as e:
            st.warning(f"Error reading sheet {sheet}: {e}")
            continue

        # IRI sheet: use existing 'Average Left\Right' column
        if 'iri' in sheet.lower():
            if 'Average Left\\Right' in df.columns:
                col = 'Average Left\\Right'
                stats = {
                    'Average': df[col].mean(),
                    'Median': df[col].median(),
                    'Highest': df[col].max(),
                    'Lowest': df[col].min()
                }
            else:
                st.warning(f"'Average Left\\Right' column not found in sheet {sheet}")
                continue

        # BBI sheet: calculate average of Left and Right columns
        elif 'bbi' in sheet.lower():
            if 'Left' in df.columns and 'Right' in df.columns:
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
            # Skip sheets that are not IRI or BBI
            continue

        stats['Sheet'] = sheet
        results.append(stats)
    return results

# ---- Streamlit app interface ----

st.title("Bulk Excel File Analyzer")

uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    all_results = []
    for file in uploaded_files:
        file_results = process_file(file)
        for res in file_results:
            res['Filename'] = file.name
            all_results.append(res)
    if all_results:
        df_results = pd.DataFrame(all_results)
        st.dataframe(df_results)
    else:
        st.info("No valid data found in uploaded files.")
else:
    st.info("Please upload one or more Excel files above.")
