import streamlit as st
import pandas as pd
import os
import plotly.express as px
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="🎩 Data Magician",
    layout="wide",
    page_icon="🎩"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
        /* General styling */
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #FF6B6B;
        }
      .stTextInput>div>div>input, .stSelectbox>div>div>select, .stMultiselect>div>div>div {
            background-color:rgb(255, 255, 255);
            color: black;
            border-radius: 5px;
        }
        .stDataFrame {
            background-color: #1E1E1E !important;
            color: white !important;
        }
        .stFileUploader>div>div>div>button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
        }
        .stFileUploader>div>div>div>button:hover {
            background-color: #FF6B6B;
        }
        /* Styled box for description */
        .description-box {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #FF4B4B;
            margin-bottom: 20px;
        }
       .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color:rgb(31, 32, 32); /* Match the app's dark theme */
    color: white;
    text-align: center;
    padding: 10px;
    border-top: 1px solid #FF4B4B; /* Accent color for the top border */
    z-index: 1000; /* Ensure footer stays on top of other elements */
}
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and user input
st.sidebar.title("🎩 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "📊 Visualization", "🛠️ Tools"])

st.sidebar.title("⚙️ User Input")
user_name = st.sidebar.text_input("👤 Enter Your Name")

uploaded_files = st.sidebar.file_uploader(
    "📤 Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if user_name:
    st.sidebar.success(f"👋 Welcome, {user_name}!")



# Main content
st.markdown("""
    <div style="
        background-color:rgb(31, 32, 32);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #FF4B4B;
        text-align: center;
        margin: 20px auto;
        max-width: 80%;
    ">
        <h1 style="color: #FF4B4B; margin: 0;">🎩 Data Transformation App</h1>
        <p style="font-size: 18px; color:rgb(241, 233, 233); margin: 10px 0 0;">
            Your one-stop solution for data cleaning, visualization, and transformation! ✨
        </p>
    </div>
""", unsafe_allow_html=True)

# Description box
st.markdown("""
    <div class="description-box" >
        <p style="font-size: 18px; color:rgb(241, 233, 233); margin: 10px 0 0;">✨ Transform your files between CSV and Excel formats with built-in data cleaning and visualization.</p>
        <p style="font-size: 18px; color:rgb(241, 233, 233); margin: 10px 0 0;">🧹 Clean your data, 📊 visualize it, and 🔄 convert it effortlessly!</p>
    </div>
""", unsafe_allow_html=True)

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
            st.error(f"❌ Unsupported File Type: {file_ext}")
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
            if st.button(f"🧼 Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")

        with col2:
            if st.button(f"🔧 Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values Filled!")

        # Select columns
        st.subheader("📌 Select Columns")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            st.warning("⚠ No numeric columns found for visualization. Try selecting appropriate columns.")
        else:
            chart_type = st.radio("Select chart type:", ["Bar Chart", "Line Chart", "Histogram", "Box Plot", "Area Chart"], key=file.name)
            
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], color=numeric_cols[0])
            elif chart_type == "Line Chart":
                fig = px.line(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], color=numeric_cols[0])
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=numeric_cols[0], color=numeric_cols[0])
            elif chart_type == "Box Plot":
                fig = px.box(df, y=numeric_cols[0])
            elif chart_type == "Area Chart":
                fig = px.area(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], color=numeric_cols[0])
            
            st.plotly_chart(fig, use_container_width=True)

        # File Conversion
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"conv_{file.name}")

        if st.button(f"🛠️ Convert {file.name} to {conversion_type}"):
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

# Text before footer
st.markdown("""
    <div style="text-align: center; margin-top: 20px; ">
        <h3 style='color: #FF4B4B'>💡 Tips for Using Data Magician</h3>
        <p>1. Upload your CSV or Excel files to get started.</p>
        <p>2. Use the data cleaning tools to remove duplicates or fill missing values.</p>
        <p>3. Visualize your data with interactive charts.</p>
        <p>4. Convert your files to the desired format and download them.</p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by <a href="https://github.com/yourusername" target="_blank" style="color: #FF4B4B; text-decoration: none;">Aamna Ashraf</a> | Powered by Streamlit 🚀
    </div>
""", unsafe_allow_html=True)


