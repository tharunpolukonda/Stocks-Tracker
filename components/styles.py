import streamlit as st

def apply_styles():
    """Apply enhanced 3D styling with dark black, blue, and white theme, including metric boxes, colored strengths/weaknesses, and company details."""
    st.markdown("""
        <style>
        /* General App Styling */
        .main {
            background: #0a0a0a;
            color: #f0f4f8;
            font-family: 'Georgia', serif;
            perspective: 1200px;
        }

        /* Container for Main Content */
        .stApp > div {
            background: rgba(10, 10, 10, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), inset 0 1px 3px rgba(240, 244, 248, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 2px solid #1e90ff;
            padding: 30px;
            transform: translateZ(25px);
        }

        /* Hide default Streamlit title */
        div[data-testid="stAppViewContainer"] > div > div > h1:first-child {
            display: none;
        }

        /* Centered Header Styling */
        .centered-header {
            text-align: center;
            color: #1e90ff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
            font-family: 'Georgia', serif;
            background: linear-gradient(145deg, #0a2030, #1e4060);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
            border: 1px solid #1e90ff;
            transform: translateZ(30px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin: 20px 0;
        }
        .centered-header:hover {
            transform: translateZ(35px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        }
        .centered-header h2, .centered-header h3 {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
        }

        /* Component Containers */
        .component-container {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6), inset 0 1px 3px rgba(240, 244, 248, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 2px solid #1e90ff;
            transform: translateZ(20px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .component-container:hover {
            transform: translateZ(25px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        }

        /* Metric Box Styling */
        .metric-box {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            color: #f0f4f8;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
        }
        .metric-box:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        /* Detail Box Styling for Company Details */
        .detail-box {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(240, 244, 248, 0.05);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            color: #f0f4f8;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .detail-box:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        /* Strengths and Weaknesses Boxes */
        .strength-box {
            background: linear-gradient(145deg, rgba(0, 255, 0, 0.1), rgba(0, 100, 0, 0.2));
            color: #00FF00;
            border-radius: 10px;
            padding: 12px;
            margin: 8px 0;
            box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
            border: 1px solid #00FF00;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
        }
        .strength-box:hover {
            transform: translateZ(20px);
            box-shadow: 0 6px 20px rgba(0, 255, 0, 0.3);
        }
        .weakness-box {
            background: linear-gradient(145deg, rgba(255, 0, 0, 0.1), rgba(100, 0, 0, 0.2));
            color: #FF0000;
            border-radius: 10px;
            padding: 12px;
            margin: 8px 0;
            box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
            border: 1px solid #FF0000;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
        }
        .weakness-box:hover {
            transform: translateZ(20px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        /* Screener Link Styling */
        .screener-link {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            color: #00FF00;
            border-radius: 10px;
            padding: 12px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
            border: 1px solid #00FF00;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            font-family: 'Lato', sans-serif;
            font-size: 18px;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .screener-link:hover {
            transform: translateZ(20px);
            box-shadow: 0 6px 20px rgba(0, 255, 0, 0.3);
        }
        .screener-link a {
            color: #00FF00;
            text-decoration: none;
        }
        .screener-link a:hover {
            text-decoration: underline;
        }

        /* Sector Header Styling */
        .sector-header {
            text-align: center;
            background: linear-gradient(145deg, #0a2030, #1e4060);
            color: #1e90ff;
            border-radius: 10px;
            padding: 12px;
            margin: 15px 0;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            border: 1px solid #1e90ff;
            transform: translateZ(20px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            font-family: 'Georgia', serif;
            font-size: 20px;
            font-weight: 700;
        }
        .sector-header:hover {
            transform: translateZ(25px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }

        /* Button Styling */
        .stButton > button {
            background: linear-gradient(45deg, #0a2030, #1e4060);
            color: #f0f4f8;
            border: none;
            border-radius: 10px;
            padding: 14px 28px;
            font-family: 'Lato', sans-serif;
            font-weight: 600;
            box-shadow: 0 6px 20px rgba(30, 64, 96, 0.5);
            transform: translateZ(20px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            font-size: 16px;
        }
        .stButton > button:hover {
            background: linear-gradient(45deg, #1e4060, #0a2030);
            transform: translateZ(25px) translateY(-2px);
            box-shadow: 0 8px 25px rgba(30, 64, 96, 0.6);
        }
        .stButton > button:active {
            transform: translateZ(15px) translateY(0);
            box-shadow: 0 4px 15px rgba(30, 64, 96, 0.4);
        }

        /* Primary Button Styling */
        .stButton > button[kind="primary"] {
            background: linear-gradient(45deg, #0a2030, #1e90ff);
            box-shadow: 0 6px 20px rgba(30, 64, 96, 0.5);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(45deg, #1e90ff, #0a2030);
            box-shadow: 0 8px 25px rgba(30, 64, 96, 0.6);
        }

        /* Metric Styling */
        .stMetric {
            background: linear-gradient(145deg, #0a0a0a, #1c2526);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            border: 1px solid #1e90ff;
            transform: translateZ(15px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stMetric:hover {
            transform: translateZ(20px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        }
        .stMetric > label {
            color: #1e90ff;
            font-family: 'Lato', sans-serif;
            font-size: 18px;
            font-weight: 600;
        }
        .stMetric > value {
            color: #f0f4f8;
            font-family: 'Lato', sans-serif;
            font-size: 22px;
            font-weight: 700;
        }

        /* Markdown Text */
        .stMarkdown {
            color: #f0f4f8;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1e90ff;
            font-family: 'Georgia', serif;
            text-align: center;
        }

        /* Horizontal Rule */
        hr {
            border: 0;
            height: 2px;
            background: linear-gradient(to right, rgba(30, 64, 96, 0), rgba(30, 64, 96, 0.6), rgba(30, 64, 96, 0));
            margin: 15px 0;
        }

        /* Input Fields */
        .stTextInput > div > input, .stSelectbox > div > select {
            background: linear-gradient(145deg, #1c2526, #0a0a0a);
            color: #f0f4f8;
            border: 1px solid #1e90ff;
            border-radius: 8px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.4);
            padding: 12px;
            font-family: 'Lato', sans-serif;
            font-size: 16px;
        }
        .stTextInput > div > input:focus, .stSelectbox > div > select:focus {
            border-color: #1e90ff;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.4), 0 4px 10px rgba(30, 64, 96, 0.3);
            transform: translateZ(5px);
        }
        </style>
    """, unsafe_allow_html=True)

    # JavaScript for button data-text
    st.markdown("""
        <script>
        document.querySelectorAll('.stButton > button').forEach(button => {
            button.setAttribute('data-text', button.innerText);
        });
        </script>
    """, unsafe_allow_html=True)