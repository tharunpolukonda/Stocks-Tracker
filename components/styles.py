import streamlit as st

def apply_styles():
    """Apply enhanced classic and clear styling with a blue, black, and white theme."""
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
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid #1e90ff;
            padding: 25px;
            transform: translateZ(20px);
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
            padding: 15px 0;
            margin-bottom: 20px;
        }
        .header-row .stImage {
            display: inline-block;
            vertical-align: middle;
            margin: 0 15px;
            transition: transform 0.3s ease;
        }
        .header-row .stImage:hover {
            transform: scale(1.05);
        }
        .header-row h1 {
            color: #1e90ff;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
            font-size: 44px;
            font-family: 'Georgia', serif;
            margin: 0;
            line-height: 90px;
            background: linear-gradient(145deg, #1c2526, #0a0a0a);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
            flex: 1;
            text-align: center;
            transform: translateZ(30px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .header-row h1:hover {
            transform: translateZ(35px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
        }

        /* Component Containers */
        .component-container {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .component-container:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        /* Button Styling */
        .stButton > button {
            position: relative;
            background: linear-gradient(45deg, #0a2030, #1e4060);
            color: #f0f4f8;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-family: 'Lato', sans-serif;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(30, 64, 96, 0.4), inset 0 1px 3px rgba(240, 244, 248, 0.1);
            transform: translateZ(15px);
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
            text-align: center;
            font-size: clamp(14px, 2vw, 16px);
            min-width: clamp(100px, 12ch, 160px);
            max-width: 180px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .stButton > button::after {
            content: attr(data-text);
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%) translateZ(5px);
            color: transparent;
            font-size: clamp(10px, 1.5vw, 12px);
            font-weight: 600;
            text-shadow: 0 0 6px rgba(240, 244, 248, 0.5), 0 2px 4px rgba(0, 0, 0, 0.6);
            white-space: nowrap;
            transition: text-shadow 0.2s ease;
            pointer-events: none;
        }
        .stButton > button:hover {
            background: linear-gradient(45deg, #1e4060, #0a2030);
            transform: translateZ(20px) translateY(-2px);
            box-shadow: 0 6px 20px rgba(30, 64, 96, 0.5);
        }
        .stButton > button:hover::after {
            text-shadow: 0 0 8px rgba(240, 244, 248, 0.6), 0 2px 5px rgba(0, 0, 0, 0.7);
        }
        .stButton > button:active {
            transform: translateZ(10px) translateY(0);
            box-shadow: 0 3px 10px rgba(30, 64, 96, 0.3);
        }

        /* Primary Button Styling */
        .stButton > button[kind="primary"] {
            background: linear-gradient(45deg, #0a2030, #1e90ff);
            color: #f0f4f8;
            box-shadow: 0 4px 15px rgba(30, 64, 96, 0.4);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(45deg, #1e90ff, #0a2030);
            box-shadow: 0 6px 20px rgba(30, 64, 96, 0.6);
        }

        /* Table Styling */
        .table-container {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .table-container:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }
        .table-row {
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(240, 244, 248, 0.2);
            transition: background 0.2s ease;
        }
        .table-row:nth-child(even) {
            background: rgba(28, 37, 38, 0.1);
        }
        .table-row:hover {
            background: rgba(30, 64, 96, 0.2);
        }
        .table-cell {
            flex: 1;
            padding: 10px 15px;
            color: #f0f4f8;
            text-align: center;
            vertical-align: middle;
            font-family: 'Lato', sans-serif;
            font-size: 15px;
            font-weight: 500;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
        }
        .table-cell b {
            font-weight: 700;
            color: #1e90ff;
        }

        /* Track IPO Table Styling */
        .track-ipo-table table {
            width: 100%;
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
        }
        .track-ipo-table th {
            background: linear-gradient(145deg, #0a2030, #1e4060);
            color: #1e90ff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            font-family: 'Lato', sans-serif;
            font-size: 16px;
            font-weight: 700;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
        }
        .track-ipo-table td {
            border-bottom: 1px solid rgba(240, 244, 248, 0.2);
            font-family: 'Lato', sans-serif;
            font-size: 15px;
            font-weight: 500;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
            color: #f0f4f8;
        }
        .track-ipo-table tr:nth-child(even) {
            background: rgba(28, 37, 38, 0.1);
        }
        .track-ipo-table tr:hover {
            background: rgba(30, 64, 96, 0.2);
        }

        /* Company Details Container */
        .company-details-container {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .company-details-container:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        /* IPO Details Container */
        .ipo-details-container {
            background: linear-gradient(145deg, #1c2526, #0a0a0a);
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(10px);
        }

        /* Sector Metrics Container */
        .sector-metrics-container {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .sector-metrics-container:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        /* Input Fields */
        .stTextInput > label, .stNumberInput > label, .stDateInput > label, .stSelectbox > label {
            color: #1e90ff;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
            font-weight: 600;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
        }
        .stTextInput > div > input, .stNumberInput > div > input, .stDateInput > div > input, .stSelectbox > div > select {
            background: linear-gradient(145deg, #1c2526, #0a0a0a);
            color: #f0f4f8;
            border: 1px solid #1e90ff;
            border-radius: 8px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.4), 0 2px 6px rgba(30, 64, 96, 0.2);
            padding: 12px;
            font-family: 'Lato', sans-serif;
            font-size: 15px;
            font-weight: 500;
            transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
        }
        .stTextInput > div > input:focus, .stNumberInput > div > input:focus, .stDateInput > div > input:focus, .stSelectbox > div > select:focus {
            border-color: #1e90ff;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.4), 0 4px 10px rgba(30, 64, 96, 0.3);
            transform: translateZ(5px);
        }

        /* Metrics */
        .stMetric {
            background: linear-gradient(145deg, #1c2526, #0a0a0a);
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stMetric:hover {
            transform: translateZ(15px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
        }
        .stMetric > label {
            color: #1e90ff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            font-family: 'Lato', sans-serif;
            font-size: 16px;
            font-weight: 600;
        }
        .stMetric > value {
            color: #f0f4f8;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            font-family: 'Lato', sans-serif;
            font-size: 20px;
            font-weight: 700;
        }
        .stMetric > delta {
            color: #1e90ff;
            font-family: 'Lato', sans-serif;
            font-size: 14px;
            font-weight: 600;
        }

        /* Plotly Chart Styling */
        .js-plotly-plot .plotly .modebar {
            background: linear-gradient(145deg, #1c2526, #0a0a0a);
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
        }
        .js-plotly-plot .plotly .modebar-btn {
            color: #f0f4f8;
            font-family: 'Lato', sans-serif;
            font-size: 14px;
            font-weight: 600;
        }
        .js-plotly-plot .plotly .modebar-btn:hover {
            color: #1e90ff;
        }
        .plotly .plot-container {
            background: rgba(10, 10, 10, 0.95);
            border-radius: 10px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            transform: translateZ(10px);
        }

        /* DataFrame Styling */
        .stDataFrame {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
        }
        .stDataFrame table {
            color: #f0f4f8;
            width: 100%;
        }
        .stDataFrame th {
            background: linear-gradient(145deg, #0a2030, #1e4060);
            color: #1e90ff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            font-family: 'Lato', sans-serif;
            font-size: 16px;
            font-weight: 700;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
        }
        .stDataFrame td {
            border-bottom: 1px solid rgba(240, 244, 248, 0.2);
            font-family: 'Lato', sans-serif;
            font-size: 15px;
            font-weight: 500;
            text-align: center;
            vertical-align: middle;
            padding: 12px;
            color: #f0f4f8;
        }
        .stDataFrame tr:nth-child(even) {
            background: rgba(28, 37, 38, 0.1);
        }
        .stDataFrame tr:hover {
            background: rgba(30, 64, 96, 0.2);
        }

        /* Markdown Text */
        .stMarkdown {
            color: #f0f4f8;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            font-family: 'Lato', sans-serif;
            font-size: 16px;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1e90ff;
            font-family: 'Georgia', serif;
        }

        /* Horizontal Rule */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, rgba(30, 64, 96, 0), rgba(30, 64, 96, 0.4), rgba(30, 64, 96, 0));
            margin: 25px 0;
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