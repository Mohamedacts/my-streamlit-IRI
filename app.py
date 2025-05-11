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

        if 'iri' in sheet.lower():
            if 'Average Left\\Right' in df.columns:
                col = 'Average Left\\Right'
                # Convert to numeric, coerce errors to NaN
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
                # Convert to numeric, coerce errors to NaN
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
