import streamlit as st
import pandas as pd
from io import BytesIO

# Sidebar with your credits - place this at the top level
st.sidebar.markdown("""
## About the Developer
**Mohamed Ali**  
Pavement Engineer  
📧 mehap201@gmail.com  
📞 +0966581764292  
[LinkedIn Profile](https://www.linkedin.com/in/mohameddalli)
---
""")

st.title("🚀 BBI - IRI Analysis ")

# File uploader widget
uploaded_files = st.file_uploader(
    "Upload Excel files (.xlsx)", 
    type="xlsx", 
    accept_multiple_files=True
)

def process_file(file):
    # Dummy processing: just return a DataFrame with filename and sheet names
    xls = pd.ExcelFile(file)
    data = []
    for sheet in xls.sheet_names:
        data.append({'Filename': file.name, 'Sheet': sheet})
    return pd.DataFrame(data)

if uploaded_files:
    all_results = pd.DataFrame()
    for file in uploaded_files:
        df = process_file(file)
        all_results = pd.concat([all_results, df], ignore_index=True)

    st.subheader("Processed Files Summary")
    st.dataframe(all_results)

    # Prepare Excel bytes for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        all_results.to_excel(writer, index=False)
    excel_data = output.getvalue()

    # Download button
    st.download_button(
        label="📥 Download Results as Excel",
        data=excel_data,
        file_name="bulk_analysis_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload one or more Excel files.")
