import streamlit as st
import pandas as pd

def find_avg_column(columns):
    # Look for a column that contains 'average', 'left', and 'right' (case-insensitive)
    for c in columns:
        c_lower = c.lower().replace('/', '\\').replace(' ', '')
        if 'average' in c_lower and 'left' in c_lower and 'right' in c_lower:
            return c
    return None

def process_iri(df):
    col = find_avg_column(df.columns)
    if not col:
        st.warning("Could not find 'Average Left\\Right' column. Found columns: " + str(list(df.columns)))
        return None
    return {
        'Average': df[col].mean(),
        'Median': df[col].median(),
        'Highest': df[col].max(),
        'Lowest': df[col].min()
    }

def process_bbi(df):
    # Try to find Left and Right columns (case-insensitive)
    left_col = right_col = None
    for c in df.columns:
        if c.strip().lower() == 'left':
            left_col = c
        if c.strip().lower() == 'right':
            right_col = c
    if not left_col or not right_col:
        st.warning("Could not find 'Left' and 'Right' columns. Found columns: " + str(list(df.columns)))
        return None
    df['Average Left\\Right'] = (df[left_col] + df[right_col]) / 2
    col = 'Average Left\\Right'
    return {
        'Average': df[col].mean(),
        'Median': df[col].median(),
        'Highest': df[col].max(),
        'Lowest': df[col].min()
    }

def process_file(file):
    results = []
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        # Try to read with skiprows=4, if error, try without skipping
        try:
            df = pd.read_excel(xls, sheet, skiprows=4)
        except Exception:
            df = pd.read_excel(xls, sheet)
        # Decide if IRI or BBI based on sheet name or columns
        if 'iri' in sheet.lower():
            stats = process_iri(df)
        elif 'bbi' in sheet.lower():
            stats = process_bbi(df)
        else:
            # Try to detect by columns
            if find_avg_column(df.columns):
                stats = process_iri(df)
            elif 'Left' in df.columns and 'Right' in df.columns:
                stats = process_bbi(df)
            else:
                continue
        if stats:
            stats['Sheet'] = sheet
            results.append(stats)
    return results

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
