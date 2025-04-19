import streamlit as st

def apply_styles():
    """Apply 3D-patterned CSS styles with Dark Blue, Black, and minimal White shadow, with bold Times New Roman centered table text and centered subheaders."""
    st.markdown("""
        <style>
        /* General App Styling */
        .main {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #ffffff;
            font-family: 'Times New Roman', serif;
            perspective: 1000px; /* Adds 3D perspective */
        }

        /* Container for Main Content */
        .stApp > div {
            background: rgba(26, 26, 26, 0.9);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            padding: 20px;
            transform: translateZ(15px);
        }

        /* Title Styling */
        h1 {
            color: #3b82f6;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.2), 0 4px 8px rgba(0, 0, 0, 0.5);
            font-size: 2.8em;
            text-align: center;
            margin-bottom: 30px;
            transform: translateZ(25px);
            transition: transform 0.3s ease;
            margin-top: 20px; /* Reduced to account for removed header */
        }
        h1:hover {
            transform: translateZ(35px);
        }

        /* Header Styling */
        h2, h3 {
            color: #1e3a8a;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.15), 0 2px 4px rgba(0, 0, 0, 0.4);
            transform: translateZ(15px);
            transition: transform 0.3s ease;
            text-align: center; /* Center subheaders */
        }
        h2:hover, h3:hover {
            transform: translateZ(20px);
        }

        /* Button Styling */
        .stButton>button {
            position: relative;
            background: linear-gradient(45deg, #1e3a8a 0%, #3b82f6 100%);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            box-shadow: 0 6px 20px rgba(30, 58, 138, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            transform: translateZ(10px);
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
            overflow: visible;
            text-align: center;
        }
        .stButton>button::after {
            content: attr(data-text);
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%) translateZ(5px);
            color: transparent;
            font-size: 12px;
            font-weight: bold;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.3), 0 2px 4px rgba(0, 0, 0, 0.5);
            white-space: nowrap;
            transition: text-shadow 0.2s ease;
            pointer-events: none;
        }
        .stButton>button:hover {
            transform: translateZ(15px) translateY(-3px);
            box-shadow: 0 10px 30px rgba(30, 58, 138, 0.7), inset 0 1px 2px rgba(255, 255, 255, 0.15);
            background: linear-gradient(45deg, #3b82f6 0%, #1e3a8a 100%);
        }
        .stButton>button:hover::after {
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.4), 0 2px 4px rgba(0, 0, 0, 0.6);
        }
        .stButton>button:active {
            transform: translateZ(5px) translateY(0);
            box-shadow: 0 4px 15px rgba(30, 58, 138, 0.4);
        }

        /* Primary Button Styling */
        .stButton>button[kind="primary"] {
            background: linear-gradient(45deg, #1e3a8a 0%, #3b82f6 100%);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
        }
        .stButton>button[kind="primary"]:hover {
            background: linear-gradient(45deg, #3b82f6 0%, #1e3a8a 100%);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.7);
        }

        /* Table Styling */
        .table-container {
            background: rgba(26, 26, 26, 0.9);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            transform: translateZ(10px);
            transition: transform 0.3s ease;
        }
        .table-container:hover {
            transform: translateZ(15px);
        }
        .table-row {
            display: flex;
            align-items: center;
            justify-content: center; /* Center horizontally */
            padding: 12px 0;
            border-bottom: 1px solid rgba(30, 58, 138, 0.2);
            transition: background 0.2s ease;
        }
        .table-row:hover {
            background: rgba(30, 58, 138, 0.2);
        }
        .table-cell {
            flex: 1;
            padding: 8px 12px;
            color: #ffffff;
            text-align: center; /* Center horizontally */
            vertical-align: middle; /* Center vertically */
            font-family: 'Times New Roman', serif;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }

        /* Company Details Container */
        .company-details-container {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            border-radius: 12px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .company-details-container:hover {
            transform: translateZ(20px);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.7);
        }

        /* IPO Details Container */
        .ipo-details-container {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            transform: translateZ(10px);
        }

        /* Sector Metrics Container */
        .sector-metrics-container {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            transform: translateZ(15px);
            transition: transform 0.3s ease;
        }
        .sector-metrics-container:hover {
            transform: translateZ(20px);
        }

        /* Input Fields */
        .stTextInput>label, .stNumberInput>label, .stDateInput>label, .stSelectbox>label {
            color: #3b82f6;
            font-size: 14px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            transform: translateZ(10px);
        }
        .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input, .stSelectbox>div>select {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            color: #ffffff;
            border: 1px solid rgba(30, 58, 138, 0.3);
            border-radius: 8px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3), 0 2px 4px rgba(30, 58, 138, 0.2);
            padding: 8px;
            transform: translateZ(10px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            font-family: 'Times New Roman', serif;
            font-size: 16px;
            font-weight: bold;
        }
        .stTextInput>div>input:focus, .stNumberInput>div>input:focus, .stDateInput>div>input:focus, .stSelectbox>div>select:focus {
            transform: translateZ(15px);
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3), 0 4px 8px rgba(30, 58, 138, 0.4);
            border-color: #3b82f6;
        }

        /* Metrics */
        .stMetric {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            transform: translateZ(10px);
            transition: transform 0.3s ease;
        }
        .stMetric:hover {
            transform: translateZ(15px);
        }
        .stMetric>label {
            color: #3b82f6;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            font-family: 'Times New Roman', serif;
            font-size: 16px;
            font-weight: bold;
        }
        .stMetric>value {
            color: #ffffff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            font-family: 'Times New Roman', serif;
            font-size: 18px;
            font-weight: bold;
        }
        .stMetric>delta {
            color: #3b82f6;
            font-family: 'Times New Roman', serif;
            font-size: 14px;
            font-weight: bold;
        }

        /* Plotly Chart Styling */
        .js-plotly-plot .plotly .modebar {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(30, 58, 138, 0.3);
        }
        .js-plotly-plot .plotly .modebar-btn {
            color: #ffffff;
            font-family: 'Times New Roman', serif;
            font-size: 14px;
            font-weight: bold;
        }
        .js-plotly-plot .plotly .modebar-btn:hover {
            color: #3b82f6;
        }
        .plotly .plot-container {
            background: rgba(26, 26, 26, 0.9);
            border-radius: 10px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            transform: translateZ(10px);
        }

        /* DataFrame Styling */
        .stDataFrame {
            background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(30, 58, 138, 0.3);
            transform: translateZ(10px);
        }
        .stDataFrame table {
            color: #ffffff;
            width: 100%;
        }
        .stDataFrame th {
            background: linear-gradient(145deg, #1e3a8a, #3b82f6);
            color: #ffffff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            font-family: 'Times New Roman', serif;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            padding: 10px;
        }
        .stDataFrame td {
            border-bottom: 1px solid rgba(30, 58, 138, 0.2);
            font-family: 'Times New Roman', serif;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            padding: 10px;
        }
        .stDataFrame tr:hover {
            background: rgba(30, 58, 138, 0.2);
        }

        /* Markdown Text */
        .stMarkdown {
            color: #ffffff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            font-family: 'Times New Roman', serif;
            font-size: 16px;
        }

        /* Horizontal Rule */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, rgba(30, 58, 138, 0), rgba(30, 58, 138, 0.5), rgba(30, 58, 138, 0));
            margin: 20px 0;
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