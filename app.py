import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Flight Price Predictor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1a73e8 0%, #0066cc 50%, #004ec4 100%);
        border-radius: 20px;
        padding: 40px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(26, 115, 232, 0.4);
        text-align: center;
    }
    
    .hero-section h1 {
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    
    .hero-section p {
        font-size: 1.1em;
        opacity: 0.95;
        margin-bottom: 5px;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #1a73e8;
    }
    
    .card h2 {
        color: #1a73e8;
        margin-bottom: 20px;
        font-size: 1.5em;
    }
    
    /* Price display */
    .price-box {
        background: linear-gradient(135deg, #1a73e8 0%, #0066cc 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    
    .price-box .price-value {
        font-size: 3em;
        font-weight: 700;
        margin: 15px 0;
    }
    
    .price-box .price-label {
        font-size: 0.9em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Price range indicator */
    .price-range-low {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
        font-size: 0.95em;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    .price-range-medium {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
        font-size: 0.95em;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
    }
    
    .price-range-high {
        background: linear-gradient(135deg, #f44336 0%, #e53935 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
        font-size: 0.95em;
        box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
    }
    
    /* Input Section Styling */
    .input-section {
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #1a73e8;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #1a73e8 0%, #0066cc 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    
    .metric-box .metric-value {
        font-size: 2em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-box .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8 0%, #0066cc 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 40px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.6) !important;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #1a73e8 0%, #0066cc 100%);
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #1a73e8 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #666;
        margin-top: 40px;
        border-top: 2px solid rgba(26, 115, 232, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Load models and scalers
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "svr_model.pkl"
    if model_path.exists():
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None

@st.cache_resource
def load_scaler():
    scaler_path = Path(__file__).parent / "scaler.pkl"
    if scaler_path.exists():
        with open(scaler_path, "rb") as f:
            return pickle.load(f)
    return None

@st.cache_resource
def load_feature_columns():
    features_path = Path(__file__).parent / "feature_columns.pkl"
    if features_path.exists():
        with open(features_path, "rb") as f:
            return pickle.load(f)
    return None

# Main content
st.markdown("""
<div class="hero-section">
    <h1>✈️ Flight Price Predictor</h1>
    <p>Advanced Machine Learning Price Estimation</p>
    <p style="font-size: 0.9em; margin-top: 15px;">Find the best flight deals with AI-powered price predictions</p>
</div>
""", unsafe_allow_html=True)

model = load_model()
scaler = load_scaler()
features = load_feature_columns()

if model is None or scaler is None:
    st.error("❌ Model or scaler files not found! Please ensure 'svr_model.pkl' and 'scaler.pkl' exist.")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Control Panel")
    st.markdown("---")
    prediction_mode = st.radio(
        "Select Mode:",
        ["Single Flight", "Batch Flights"],
        help="Choose prediction mode"
    )
    st.markdown("---")
    st.markdown(
        "<small>🔧 Built with Streamlit & Scikit-Learn | Flight Price ML v1.0</small>",
        unsafe_allow_html=True
    )

# Main content area
if prediction_mode == "Single Flight":
    # Input section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 🛫 Flight Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        airline = st.selectbox("Airline", ["IndiGo", "Air India", "Jet Airways", "SpiceJet", "Air Asia", "Vistara"])
        source = st.selectbox("Departure City", ["Banglore", "New Delhi", "Mumbai", "Kolkata", "Hyderabad"])
        destination = st.selectbox("Arrival City", ["Banglore", "New Delhi", "Mumbai", "Kolkata", "Hyderabad"])
        total_stops = st.number_input("Number of Stops", min_value=0, max_value=4, value=0)
        month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=3)
    
    with col2:
        year = st.number_input("Year", min_value=2019, max_value=2025, value=2019)
        dep_hour = st.number_input("Departure Hour (0-23)", min_value=0, max_value=23, value=14)
        dep_minute = st.number_input("Departure Minute (0-59)", min_value=0, max_value=59, value=0)
        arrival_hour = st.number_input("Arrival Hour (0-23)", min_value=0, max_value=23, value=18)
        arrival_minute = st.number_input("Arrival Minute (0-59)", min_value=0, max_value=59, value=30)
    
    duration_hour = st.number_input("Flight Duration (hours)", min_value=0, max_value=24, value=4)
    duration_minute = st.number_input("Flight Duration (minutes)", min_value=0, max_value=59, value=30)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prediction button
    if st.button("💰 Predict Flight Price", key="predict_btn"):
        try:
            # Create input dataframe
            input_data = pd.DataFrame({
                "Airline": [airline],
                "Source": [source],
                "Destination": [destination],
                "Total_Stops": [total_stops],
                "Month": [month],
                "Year": [year],
                "Dep_Hour": [dep_hour],
                "Dep_Minute": [dep_minute],
                "Arrival_Hour": [arrival_hour],
                "Arrival_Minute": [arrival_minute],
                "Duration_Hour": [duration_hour],
                "Duration_Minute": [duration_minute]
            })
            
            # One-hot encode categorical variables
            input_encoded = pd.get_dummies(input_data, columns=['Airline', 'Source', 'Destination'], drop_first=False)
            
            # Ensure all feature columns exist
            for feature in features:
                if feature not in input_encoded.columns:
                    input_encoded[feature] = 0
            
            # Select only the features the model was trained on
            input_encoded = input_encoded[features]
            
            # Scale the features
            input_scaled = scaler.transform(input_encoded)
            
            # Make prediction
            predicted_price = model.predict(input_scaled)[0]
            
            # Display results
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 💎 Price Prediction")
            
            # Price display
            st.markdown(f"""
            <div class="price-box">
                <div class="price-label">Estimated Flight Price</div>
                <div class="price-value">₹ {predicted_price:,.0f}</div>
                <div class="price-label">Indian Rupees</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Price range indicator
            if predicted_price < 5000:
                st.markdown(
                    '<div class="price-range-low">💚 Budget Friendly - Great Deal!</div>',
                    unsafe_allow_html=True
                )
            elif predicted_price < 10000:
                st.markdown(
                    '<div class="price-range-medium">⚠️ Moderate Price - Average Rate</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="price-range-high">🔴 Premium Price - Expensive Route</div>',
                    unsafe_allow_html=True
                )
            
            # Flight summary
            st.markdown("#### ✈️ Flight Summary")
            summary_df = pd.DataFrame({
                "Detail": ["Airline", "Route", "Stops", "Departure", "Arrival", "Duration"],
                "Information": [
                    airline,
                    f"{source} → {destination}",
                    f"{total_stops}",
                    f"{dep_hour:02d}:{dep_minute:02d}",
                    f"{arrival_hour:02d}:{arrival_minute:02d}",
                    f"{duration_hour}h {duration_minute}m"
                ]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")

else:  # Batch mode
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Flight Data (CSV)")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.markdown(f"**Loaded {len(df)} flight records**")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("💰 Predict Prices for All Flights"):
                # Prepare data
                df_encoded = pd.get_dummies(df, columns=['Airline', 'Source', 'Destination'], drop_first=False)
                
                # Ensure all feature columns exist
                for feature in features:
                    if feature not in df_encoded.columns:
                        df_encoded[feature] = 0
                
                # Select only the features the model was trained on
                df_encoded = df_encoded[features]
                
                # Scale the features
                df_scaled = scaler.transform(df_encoded)
                
                # Make predictions
                predictions = model.predict(df_scaled)
                
                # Add predictions to dataframe
                df["Predicted_Price"] = predictions
                df["Price_Category"] = df["Predicted_Price"].apply(
                    lambda x: "Budget" if x < 5000 else ("Standard" if x < 10000 else "Premium")
                )
                
                # Display results
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📊 Batch Prediction Results")
                
                avg_price = predictions.mean()
                min_price = predictions.min()
                max_price = predictions.max()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-label">Average Price</div>
                        <div class="metric-value">₹ {avg_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-box" style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);">
                        <div class="metric-label">Cheapest Flight</div>
                        <div class="metric-value">₹ {min_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-box" style="background: linear-gradient(135deg, #f44336 0%, #e53935 100%);">
                        <div class="metric-label">Most Expensive</div>
                        <div class="metric-value">₹ {max_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("#### 🎯 Detailed Predictions")
                st.dataframe(
                    df[["Airline", "Source", "Destination", "Total_Stops", "Predicted_Price", "Price_Category"]].head(20),
                    use_container_width=True
                )
                
                # Download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Predictions (CSV)",
                    data=csv,
                    file_name="flight_price_predictions.csv",
                    mime="text/csv"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <p>🚀 Flight Price Predictor Dashboard | Powered by Support Vector Regression (SVR)</p>
    <p style="font-size: 0.85em; color: #999;">© 2024 | Smart Travel Intelligence</p>
</div>
""", unsafe_allow_html=True)
