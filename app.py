def process_file(file):
    results = []
    xls = pd.ExcelFile(file)
    for sheet in xls.sheet_names:
        # Read using header=3 (4th row as header)
        try:
            df = pd.read_excel(xls, sheet, header=3)
        except Exception as e:
            st.warning(f"Could not read sheet {sheet}: {e}")
            continue

        # For IRI: look for 'Average Left\Right'
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
                st.warning(f"Could not find 'Average Left\\Right' in {sheet}. Columns: {df.columns.tolist()}")
                continue

        # For BBI: calculate average of Left and Right
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
                st.warning(f"Could not find 'Left' and 'Right' in {sheet}. Columns: {df.columns.tolist()}")
                continue
        else:
            continue

        stats['Sheet'] = sheet
        results.append(stats)
    return results
