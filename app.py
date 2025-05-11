import streamlit as st
import pandas as pd

def process_iri(df):
    col = 'Average Left\\Right'
    return {
        'Average': df[col].mean(),
        'Median': df[col].median(),
        'Highest': df[col].max(),
        'Lowest': df[col].min()
    }

def process_bbi(df):
    df['Average Left\\Right'] = (df['Left'] + df['Right']) / 2
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
        df = pd.read_excel(xls, sheet, skiprows=4)
        if 'IRI' in sheet:
            stats = process_iri(df)
        elif 'BBI' in sheet:
            stats = process_bbi(df)
        else:
            continue
        stats['Sheet'] = sheet
        return stats
    return results

st.title("Bulk Excel File Analyzer")
uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    all_results = []
    for file in uploaded_files:
        result = process_file(file)
        if result:
            result['Filename'] = file.name
            all_results.append(result)
    if all_results:
        st.write(pd.DataFrame(all_results))
    else:
        st.write("No valid data found in uploaded files.")
