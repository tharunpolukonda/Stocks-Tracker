import streamlit as st

def apply_styles():
    """Apply dark black background with dark blue buttons and dynamic size adjustment."""
    st.markdown("""
        <style>
        /* General App Styling */
        .main {
            background: #0a0a0a;
            color: #f0f4f8;
            font-family: 'Georgia', serif;
            perspective: 1000px;
        }

        /* Container for Main Content */
        .stApp > div {
            background: rgba(10, 10, 10, 0.95);
            border-radius: 18px;
            box-shadow: 0 12px 50px rgba(0, 0, 0, 0.9), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            padding: 30px;
            transform: translateZ(25px);
        }

        /* Hide default Streamlit title */
        div[data-testid="stAppViewContainer"] > div > div > h1:first-child {
            display: none;
        }

        /* Header Styling */
        .header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            padding: 20px 0;
        }
        .header-row .stImage {
            display: inline-block;
            vertical-align: middle;
            margin: 0 20px;
        }
        .header-row h1 {
            color: #1e90ff;
            text-shadow: 2px 2px 6px #000000;
            font-size: 48px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            line-height: 100px;
            background: linear-gradient(145deg, #1e2a44, #0a101f);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
            flex: 1;
            text-align: center;
            transform: translateZ(35px);
            transition: transform 0.3s ease;
        }
        .header-row h1:hover {
            transform: translateZ(45px);
        }

        /* Component Containers */
        .component-container {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(20px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .component-container:hover {
            transform: translateZ(25px);
            box-shadow: 0 12px 50px rgba(0, 0, 0, 0.9);
        }

        /* Button Styling */
        .stButton > button {
            position: relative;
            background: linear-gradient(45deg, #1e4060 0%, #0a2030 100%);
            color: #f0f4f8;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-family: 'Georgia', serif;
            font-weight: bold;
            box-shadow: 0 8px 25px rgba(30, 64, 96, 0.5), inset 0 2px 6px rgba(240, 244, 248, 0.1);
            transform: translateZ(20px);
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
            text-align: center;
            font-size: clamp(12px, 2vw + 2px, 18px); /* Dynamic size based on text and viewport */
            min-width: clamp(90px, 10ch, 180px); /* Adjusts based on text length */
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .stButton > button::after {
            content: attr(data-text);
            position: absolute;
            bottom: -22px;
            left: 50%;
            transform: translateX(-50%) translateZ(5px);
            color: transparent;
            font-size: clamp(10px, 1.5vw, 14px);
            font-weight: bold;
            text-shadow: 0 0 8px rgba(240, 244, 248, 0.5), 0 2px 6px rgba(0, 0, 0, 0.7);
            white-space: nowrap;
            transition: text-shadow 0.2s ease;
            pointer-events: none;
        }
        .stButton > button:hover {
            transform: translateZ(25px) translateY(-4px);
            box-shadow: 0 12px 35px rgba(30, 64, 96, 0.7), inset 0 2px 6px rgba(240, 244, 248, 0.2);
            background: linear-gradient(45deg, #0a2030 0%, #1e4060 100%);
        }
        .stButton > button:hover::after {
            text-shadow: 0 0 10px rgba(240, 244, 248, 0.6), 0 2px 6px rgba(0, 0, 0, 0.8);
        }
        .stButton > button:active {
            transform: translateZ(15px) translateY(0);
            box-shadow: 0 5px 20px rgba(30, 64, 96, 0.4);
        }

        /* Primary Button Styling */
        .stButton > button[kind="primary"] {
            background: linear-gradient(45deg, #0a2030 0%, #1e4060 100%);
            box-shadow: 0 10px 30px rgba(30, 64, 96, 0.6), inset 0 2px 6px rgba(240, 244, 248, 0.1);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(45deg, #1e4060 0%, #0a2030 100%);
            box-shadow: 0 14px 40px rgba(30, 64, 96, 0.8);
        }

        /* Table Styling */
        .table-container {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(20px);
            transition: transform 0.3s ease;
        }
        .table-container:hover {
            transform: translateZ(25px);
        }
        .table-row {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px 0;
            border-bottom: 1px solid rgba(30, 40, 60, 0.4);
            transition: background 0.2s ease;
        }
        .table-row:hover {
            background: rgba(30, 40, 60, 0.2);
        }
        .table-cell {
            flex: 1;
            padding: 10px 15px;
            color: #f0f4f8;
            text-align: center;
            vertical-align: middle;
            font-family: 'Georgia', serif;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        }

        /* Track IPO Table Styling */
        .track-ipo-table table {
            width: 100%;
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(20px);
        }
        .track-ipo-table th {
            background: linear-gradient(145deg, #0a2030, #1e4060);
            color: #f0f4f8;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            font-family: 'Georgia', serif;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
        }
        .track-ipo-table td {
            border-bottom: 1px solid rgba(30, 40, 60, 0.4);
            font-family: 'Georgia', serif;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
            color: #f0f4f8;
        }
        .track-ipo-table tr:hover {
            background: rgba(30, 40, 60, 0.2);
        }

        /* Company Details Container */
        .company-details-container {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 12px 50px rgba(0, 0, 0, 0.8), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(20px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .company-details-container:hover {
            transform: translateZ(25px);
            box-shadow: 0 15px 60px rgba(0, 0, 0, 0.9);
        }

        /* IPO Details Container */
        .ipo-details-container {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(15px);
        }

        /* Sector Metrics Container */
        .sector-metrics-container {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(20px);
            transition: transform 0.3s ease;
        }
        .sector-metrics-container:hover {
            transform: translateZ(25px);
        }

        /* Input Fields */
        .stTextInput > label, .stNumberInput > label, .stDateInput > label, .stSelectbox > label {
            color: #1e90ff;
            font-size: 16px;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            transform: translateZ(15px);
        }
        .stTextInput > div > input, .stNumberInput > div > input, .stDateInput > div > input, .stSelectbox > div > select {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            color: #f0f4f8;
            border: 2px solid rgba(30, 40, 60, 0.6);
            border-radius: 12px;
            box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5), 0 2px 6px rgba(30, 64, 96, 0.2);
            padding: 12px;
            transform: translateZ(15px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            font-family: 'Georgia', serif;
            font-size: 16px;
            font-weight: bold;
        }
        .stTextInput > div > input:focus, .stNumberInput > div > input:focus, .stDateInput > div > input:focus, .stSelectbox > div > select:focus {
            transform: translateZ(20px);
            box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5), 0 4px 10px rgba(30, 64, 96, 0.4);
            border-color: #1e90ff;
        }

        /* Metrics */
        .stMetric {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5), inset 0 2px 6px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(15px);
            transition: transform 0.3s ease;
        }
        .stMetric:hover {
            transform: translateZ(20px);
        }
        .stMetric > label {
            color: #1e90ff;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            font-family: 'Georgia', serif;
            font-size: 16px;
            font-weight: bold;
        }
        .stMetric > value {
            color: #f0f4f8;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            font-family: 'Georgia', serif;
            font-size: 20px;
            font-weight: bold;
        }
        .stMetric > delta {
            color: #1e90ff;
            font-family: 'Georgia', serif;
            font-size: 14px;
            font-weight: bold;
        }

        /* Plotly Chart Styling */
        .js-plotly-plot .plotly .modebar {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 10px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 2px solid rgba(30, 40, 60, 0.6);
        }
        .js-plotly-plot .plotly .modebar-btn {
            color: #f0f4f8;
            font-family: 'Georgia', serif;
            font-size: 14px;
            font-weight: bold;
        }
        .js-plotly-plot .plotly .modebar-btn:hover {
            color: #1e90ff;
        }
        .plotly .plot-container {
            background: rgba(10, 10, 10, 0.95);
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
            transform: translateZ(15px);
        }

        /* DataFrame Styling */
        .stDataFrame {
            background: linear-gradient(145deg, #0a0a0a, #1e2a44);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid rgba(30, 40, 60, 0.6);
            transform: translateZ(15px);
        }
        .stDataFrame table {
            color: #f0f4f8;
            width: 100%;
        }
        .stDataFrame th {
            background: linear-gradient(145deg, #0a2030, #1e4060);
            color: #f0f4f8;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            font-family: 'Georgia', serif;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
        }
        .stDataFrame td {
            border-bottom: 1px solid rgba(30, 40, 60, 0.4);
            font-family: 'Georgia', serif;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
        }
        .stDataFrame tr:hover {
            background: rgba(30, 40, 60, 0.2);
        }

        /* Markdown Text */
        .stMarkdown {
            color: #f0f4f8;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            font-family: 'Georgia', serif;
            font-size: 16px;
        }

        /* Horizontal Rule */
        hr {
            border: 0;
            height: 2px;
            background: linear-gradient(to right, rgba(30, 64, 96, 0), rgba(30, 64, 96, 0.6), rgba(30, 64, 96, 0));
            margin: 30px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # JavaScript to dynamically set data-text attribute for buttons
    st.markdown("""
        <script>
        document.querySelectorAll('.stButton > button').forEach(button => {
            button.setAttribute('data-text', button.innerText);
        });
        </script>
    """, unsafe_allow_html=True)