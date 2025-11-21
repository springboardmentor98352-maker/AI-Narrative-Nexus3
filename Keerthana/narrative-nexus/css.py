def load_css():
    return """
    <style>

    /*PAGE BACKGROUND*/
    .main {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .page-title {
        text-align:center;
        color:#ffffff;
        font-size:48px;
        margin-bottom:5px;
        font-weight:800;
    }

    .page-subtitle {
        text-align:center;
        color:#c0c0ff;
        font-size:22px;
        margin-bottom:35px;
    }

    /*CARD SECTIONS*/
    .card-section {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
        backdrop-filter: blur(6px);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    }

    .center { text-align:center; }

    .section-title {
        font-size: 22px;
        color: #ffd6ff;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /*TEXT BOXES*/
    .text-box {
        background: #12003b;
        color: #ffffff;
        padding: 15px;
        height: 250px;
        overflow-y: auto;
        border-radius: 12px;
        border: 1px solid #7b2cbf;
        font-size: 14px;
    }

    .text-box-title {
        font-size: 18px;
        margin-bottom: 8px;
        color: #ffd6ff;
        font-weight:600;
    }

    /*STAT CARDS*/
    .stat-card {
        padding: 18px;
        border-radius: 14px;
        text-align:center;
        color:white;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }

    .blue  { background: linear-gradient(135deg,#4facfe,#00f2fe); }
    .purple{ background: linear-gradient(135deg,#a18cd1,#fbc2eb); }

    .stat-number {
        font-size: 32px;
        font-weight: 700;
    }

    .stat-label {
        font-size: 14px;
        margin-top: 5px;
    }

    .reduce-card {
        background: #2d0052;
        padding: 15px;
        font-size:18px;
        text-align:center;
        border-radius: 12px;
        border:1px solid #bb86fc;
        color:#ffccff;
        font-weight:600;
    }

    /*FILE TITLE*/
    .file-title {
        background: rgba(255,255,255,0.15);
        padding: 15px;
        border-radius: 10px;
        font-size:20px;
        margin-top:25px;
        margin-bottom:10px;
        font-weight:600;
    }

    /*BUTTON STYLING*/
    .stButton>button {
        background: linear-gradient(90deg,#ff00cc,#3333ff);
        color:white;
        border:none;
        padding: 14px 25px;
        border-radius: 10px;
        font-size:18px;
        font-weight:700;
        width: 100%;
        cursor:pointer;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }

    /*INPUT FIELDS*/
    .stTextInput>div>div>input,
    .stTextArea textarea {
        background-color: rgba(255,255,255,0.15);
        color: white;
        border-radius: 8px;
        border:1px solid #d5baff;
        font-size: 14px;
    }

    </style>
    """
