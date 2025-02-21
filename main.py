import streamlit as st
import pandas as pd
import os
import plotly.express as px
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="🚀 Data Sweeper", layout='wide')

# Custom styling with dark mode
st.markdown("""
    <style>
        body { background-color: black; color: white; }
        .stTextInput, .stFileUploader, .stButton, .stSelectbox, .stMultiselect, .stRadio, .stCheckbox { color: black !important; }
        .stDataFrame { background-color: #222 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for user input and file upload
st.sidebar.title("⚙️ User Input")
user_name = st.sidebar.text_input("Enter Your Name")

uploaded_files = st.sidebar.file_uploader(
    "📤 Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if user_name:
    st.sidebar.success(f"Welcome, {user_name}!")

st.title("🚀 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

if uploaded_files:
    st.subheader(f"📂 Uploaded Files by {user_name}")
    
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Load Data
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Type: {file_ext}")
            continue  # Skip unsupported files

        st.write(f"📁 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # Show dataframe preview
        st.write("🔍 **Preview of the Data**")
        st.dataframe(df, height=300)

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("✅ *Duplicates Removed!*")

        with col2:
            if st.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ *Missing Values Filled!*")

        # Select columns
        st.subheader("📌 Select Columns")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📈 Data Visualization")
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            st.warning("⚠ No numeric columns found for visualization. Try selecting appropriate columns.")
        else:
            chart_type = st.radio("Select chart type:", ["Bar Chart", "Line Chart", "Histogram"], key=file.name)
            
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], color=numeric_cols[0])
            elif chart_type == "Line Chart":
                fig = px.line(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], color=numeric_cols[0])
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=numeric_cols[0], color=numeric_cols[0])
            
            st.plotly_chart(fig)

        # File Conversion
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"conv_{file.name}")

        if st.button(f"Convert {file.name} to {conversion_type}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")


