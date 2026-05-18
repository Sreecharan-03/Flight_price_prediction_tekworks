import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="✈️ Skybound - Flight Price Predictor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling - Premium Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Playfair+Display:wght@700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 50%, #0d3b66 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 50%, #0d3b66 100%);
    }
    
    /* Premium Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1f7a8c 0%, #3aaed8 50%, #e28844 100%);
        border-radius: 30px;
        padding: 50px;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(31, 122, 140, 0.6), 0 0 80px rgba(226, 136, 68, 0.2);
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .hero-section h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 15px;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-section p {
        font-size: 1.2em;
        opacity: 0.95;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(20px); }
    }
    
    /* Premium Card styling */
    .premium-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(31, 122, 140, 0.2);
        border: 1px solid rgba(226, 136, 68, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(31, 122, 140, 0.3);
    }
    
    .premium-card h2 {
        color: #1f7a8c;
        margin-bottom: 25px;
        font-size: 1.8em;
        font-weight: 600;
    }
    
    /* Stunning Price Display */
    .price-display-box {
        background: linear-gradient(135deg, #1f7a8c 0%, #3aaed8 50%, #e28844 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 15px 50px rgba(31, 122, 140, 0.4);
        animation: scaleIn 0.5s ease-out;
    }
    
    .price-display-box .price-value {
        font-family: 'Playfair Display', serif;
        font-size: 4em;
        font-weight: 700;
        margin: 20px 0;
        animation: slideInUp 0.6s ease-out;
    }
    
    .price-display-box .price-label {
        font-size: 1em;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Price category badges */
    .price-badge-budget {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        padding: 18px 25px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        font-weight: 600;
        font-size: 1.05em;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.35);
        animation: slideInUp 0.6s ease-out 0.1s both;
    }
    
    .price-badge-standard {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        padding: 18px 25px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        font-weight: 600;
        font-size: 1.05em;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.35);
        animation: slideInUp 0.6s ease-out 0.2s both;
    }
    
    .price-badge-premium {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 18px 25px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        font-weight: 600;
        font-size: 1.05em;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.35);
        animation: slideInUp 0.6s ease-out 0.3s both;
    }
    
    /* Premium Metric Boxes */
    .metric-card {
        background: linear-gradient(135deg, rgba(31, 122, 140, 0.95), rgba(58, 174, 216, 0.95));
        color: white;
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 35px rgba(31, 122, 140, 0.4);
        border: 1px solid rgba(226, 136, 68, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(31, 122, 140, 0.5);
    }
    
    .metric-card .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.8em;
        font-weight: 700;
        margin: 12px 0;
    }
    
    .metric-card .metric-label {
        font-size: 0.95em;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
    
    /* Input Section */
    .input-section {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 20px;
        padding: 35px;
        margin: 25px 0;
        box-shadow: 0 10px 40px rgba(31, 122, 140, 0.2);
        border: 2px solid rgba(226, 136, 68, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .input-section > h3 {
        color: #1f7a8c;
        font-size: 1.6em;
        margin-bottom: 25px;
        font-weight: 600;
    }
    
    /* Premium Button */
    .stButton > button {
        background: linear-gradient(135deg, #1f7a8c 0%, #3aaed8 50%, #e28844 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px 45px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.15em !important;
        box-shadow: 0 8px 25px rgba(31, 122, 140, 0.4) !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(226, 136, 68, 0.6) !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, rgba(31, 122, 140, 0.95), rgba(13, 59, 102, 0.95)) !important;
    }
    
    .stSidebar > div > div:first-child {
        padding-top: 30px;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(31, 122, 140, 0.2);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3aaed8, #e28844) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #ccc;
        margin-top: 50px;
        border-top: 1px solid rgba(226, 136, 68, 0.3);
        font-size: 0.95em;
    }
    
    .footer p {
        margin: 8px 0;
    }
    
    /* Selectbox and inputs styling */
    .stSelectbox, .stNumberInput {
        margin-bottom: 15px;
    }
    
    /* Info badges */
    .info-badge {
        background: rgba(58, 174, 216, 0.2);
        border-left: 4px solid #3aaed8;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #1f7a8c;
        font-weight: 500;
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
    <h1>✈️ SKYBOUND</h1>
    <p>Premium Flight Price Intelligence</p>
    <p style="font-size: 0.95em; margin-top: 20px; opacity: 0.95;">Powered by Advanced SVR Machine Learning • Real-time Price Predictions</p>
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
    st.markdown("### 🎯 Skybound Control Panel")
    st.markdown("---")
    prediction_mode = st.radio(
        "Select Mode:",
        ["Single Flight", "Batch Flights"],
        help="Choose prediction mode"
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; color: #fff;">
        <small>🚀 **SKYBOUND v1.0**  
        Powered by Support Vector Regression (SVR)  
        Real-time ML Price Predictions  
        © 2024 Flight Intelligence</small>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main content area
if prediction_mode == "Single Flight":
    # Input section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### ✈️ Flight Details")
    st.markdown('<div class="info-badge">💡 Enter your flight details below for instant AI-powered price prediction</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📍 Route Information**")
        airline = st.selectbox("Airline", ["IndiGo", "Air India", "Jet Airways", "SpiceJet", "Air Asia", "Vistara"], key="airline")
        source = st.selectbox("Departure City", ["Banglore", "New Delhi", "Mumbai", "Kolkata", "Hyderabad"], key="source")
        destination = st.selectbox("Arrival City", ["Banglore", "New Delhi", "Mumbai", "Kolkata", "Hyderabad"], key="dest")
        total_stops = st.number_input("Number of Stops", min_value=0, max_value=4, value=0, key="stops")
        
        st.markdown("**📅 Date & Time**")
        month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=3, key="month")
        year = st.number_input("Year", min_value=2019, max_value=2025, value=2019, key="year")
    
    with col2:
        st.markdown("**🕐 Departure & Arrival**")
        dep_hour = st.number_input("Departure Hour (0-23)", min_value=0, max_value=23, value=14, key="dep_h")
        dep_minute = st.number_input("Departure Minute (0-59)", min_value=0, max_value=59, value=0, key="dep_m")
        arrival_hour = st.number_input("Arrival Hour (0-23)", min_value=0, max_value=23, value=18, key="arr_h")
        arrival_minute = st.number_input("Arrival Minute (0-59)", min_value=0, max_value=59, value=30, key="arr_m")
        
        st.markdown("**⏱️ Flight Duration**")
        duration_hour = st.number_input("Flight Duration (hours)", min_value=0, max_value=24, value=4, key="dur_h")
        duration_minute = st.number_input("Flight Duration (minutes)", min_value=0, max_value=59, value=30, key="dur_m")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prediction button with premium styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_btn = st.button("💰 Get Price Prediction", key="predict_btn", use_container_width=True)
    
    if predict_btn:
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
            
            # Display results with animations
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.markdown("### 💎 Price Prediction Results")
            
            # Price display with premium styling
            st.markdown(f"""
            <div class="price-display-box">
                <div class="price-label">✈️ Estimated Flight Price</div>
                <div class="price-value">₹ {predicted_price:,.0f}</div>
                <div class="price-label">Indian Rupees (INR)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Price category with animations
            if predicted_price < 5000:
                st.markdown(
                    '<div class="price-badge-budget">💚 Budget Friendly - Excellent Deal! Book Now!</div>',
                    unsafe_allow_html=True
                )
                deal_type = "Budget"
            elif predicted_price < 10000:
                st.markdown(
                    '<div class="price-badge-standard">🔵 Moderate Price - Standard Market Rate</div>',
                    unsafe_allow_html=True
                )
                deal_type = "Standard"
            else:
                st.markdown(
                    '<div class="price-badge-premium">🔴 Premium Pricing - High-Demand Route</div>',
                    unsafe_allow_html=True
                )
                deal_type = "Premium"
            
            # Flight details with icons
            st.markdown("---")
            st.markdown("### 📋 Flight Summary")
            
            col_summary1, col_summary2 = st.columns(2)
            
            with col_summary1:
                st.markdown(f"""
                **Airline:** {airline}  
                **Route:** {source} → {destination}  
                **Stops:** {total_stops}
                """)
            
            with col_summary2:
                st.markdown(f"""
                **Departure:** {dep_hour:02d}:{dep_minute:02d}  
                **Arrival:** {arrival_hour:02d}:{arrival_minute:02d}  
                **Duration:** {duration_hour}h {duration_minute}m
                """)
            
            # Additional insights
            st.markdown("---")
            st.markdown("### 📊 Price Insights")
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Deal Category</div>
                    <div class="metric-value">{deal_type}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with insight_col2:
                savings = max(0, 10000 - predicted_price)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Potential Savings*</div>
                    <div class="metric-value">₹ {savings:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with insight_col3:
                rating = min(5, max(1, (10000 - predicted_price) / 2000))
                stars = "⭐" * int(rating)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Value Rating</div>
                    <div class="metric-value">{stars}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.caption("*Savings estimated vs. average premium fare")
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")

else:  # Batch mode
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 📁 Batch Flight Analysis")
    st.markdown('<div class="info-badge">📊 Upload a CSV file to predict prices for multiple flights instantly</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.markdown(f"**✅ Loaded {len(df)} flight records**")
            
            with st.expander("👁️ Preview Data"):
                st.dataframe(df.head(), use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            col_batch1, col_batch2, col_batch3 = st.columns([1, 2, 1])
            with col_batch2:
                batch_btn = st.button("💰 Predict Prices for All Flights", key="batch_btn", use_container_width=True)
            
            if batch_btn:
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
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Batch Prediction Results")
                
                avg_price = predictions.mean()
                min_price = predictions.min()
                max_price = predictions.max()
                median_price = np.median(predictions)
                
                # Premium metrics display
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📊 Average</div>
                        <div class="metric-value">₹ {avg_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #4caf50, #45a049);">
                        <div class="metric-label">💰 Cheapest</div>
                        <div class="metric-value">₹ {min_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col3:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #ff6b6b, #ee5a6f);">
                        <div class="metric-label">🔥 Most Expensive</div>
                        <div class="metric-value">₹ {max_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col4:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #9c27b0, #7b1fa2);">
                        <div class="metric-label">📈 Median</div>
                        <div class="metric-value">₹ {median_price:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Price distribution visualization
                st.markdown("---")
                st.markdown("### 📈 Price Distribution Analysis")
                
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    # Histogram
                    fig_hist = go.Figure(data=[
                        go.Histogram(
                            x=predictions,
                            nbinsx=30,
                            marker_color='rgba(31, 122, 140, 0.7)',
                            showlegend=False
                        )
                    ])
                    fig_hist.update_layout(
                        title="Price Distribution",
                        xaxis_title="Price (₹)",
                        yaxis_title="Frequency",
                        template="plotly_white",
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col_viz2:
                    # Category pie chart
                    category_counts = df["Price_Category"].value_counts()
                    colors = {'Budget': '#4caf50', 'Standard': '#2196F3', 'Premium': '#ff6b6b'}
                    fig_pie = go.Figure(data=[
                        go.Pie(
                            labels=category_counts.index,
                            values=category_counts.values,
                            marker=dict(colors=[colors.get(cat, '#999') for cat in category_counts.index]),
                            textposition='auto'
                        )
                    ])
                    fig_pie.update_layout(
                        title="Price Category Breakdown",
                        height=400,
                        template="plotly_white"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Category distribution
                st.markdown("---")
                st.markdown("### 💡 Category Breakdown")
                cat_col1, cat_col2, cat_col3 = st.columns(3)
                
                budget_count = (df["Price_Category"] == "Budget").sum()
                standard_count = (df["Price_Category"] == "Standard").sum()
                premium_count = (df["Price_Category"] == "Premium").sum()
                
                with cat_col1:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #4caf50, #45a049);">
                        <div class="metric-label">Budget Flights</div>
                        <div class="metric-value">{budget_count}</div>
                        <div class="metric-label">{budget_count/len(df)*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cat_col2:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #2196F3, #1976D2);">
                        <div class="metric-label">Standard Flights</div>
                        <div class="metric-value">{standard_count}</div>
                        <div class="metric-label">{standard_count/len(df)*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cat_col3:
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #ff6b6b, #ee5a6f);">
                        <div class="metric-label">Premium Flights</div>
                        <div class="metric-value">{premium_count}</div>
                        <div class="metric-label">{premium_count/len(df)*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed predictions table
                st.markdown("---")
                st.markdown("### 🎯 Detailed Predictions")
                
                display_df = df[["Airline", "Source", "Destination", "Total_Stops", "Predicted_Price", "Price_Category"]].copy()
                display_df["Predicted_Price"] = display_df["Predicted_Price"].apply(lambda x: f"₹ {x:,.0f}")
                
                st.dataframe(display_df.head(20), use_container_width=True, hide_index=True)
                
                # Download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download All Predictions (CSV)",
                    data=csv,
                    file_name="flight_price_predictions.csv",
                    mime="text/csv",
                    key="download_btn"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1em; font-weight: 600;">✈️ SKYBOUND - Premium Flight Price Intelligence</p>
    <p>Powered by Advanced SVR Machine Learning • Real-time AI Predictions</p>
    <p style="font-size: 0.85em; color: #999; margin-top: 15px;">© 2024 Skybound Analytics | Data-Driven Travel Solutions</p>
</div>
""", unsafe_allow_html=True)
