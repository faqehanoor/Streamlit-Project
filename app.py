import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for styling the app with a black background and white text
st.markdown(
    """
    <style>
        body, .main, .block-container {
            background-color: black !important;
            color: white !important;
        }
        h1, h2, h3, h4, h5, h6, label, .stTextInput>div>div>input, .stRadio>label {
            color: white !important;
        }
        .stButton>button {
            border: none;
            border-radius: 8px;
            background-color: #0078D7;
            color: white;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 10px rgba(255, 255, 255, 0.2);
        }
        .stButton>button:hover {
            background-color: #005a9e;
            cursor: pointer;
        }
        .stDataFrame, .stTable {
            border-radius: 10px;
            overflow: hidden;
            background-color: #333;
            color: white;
        }
        .stDownloadButton>button {
            background-color: #28a745;
            color: white;
        }
        .stDownloadButton>button:hover {
            background-color: #218838;
        }
        .stFileUploader label {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the main app title and introductory text
st.title("Advanced Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File uploader widget
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")
        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())

        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled!")

        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    # Enhanced success message with great styling
    st.markdown(
        """
        <div style="
            background-color: #28a745;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.3);
        ">
            🎉 All files processed successfully!
        </div>
        """,
        unsafe_allow_html=True
    )
