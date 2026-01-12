CSS = """
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container - limit width */
    .main .block-container {
        max-width: 600px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title styling */
    h1 {
        font-weight: 600;
        font-size: 1.75rem;
        color: #111111;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle/description */
    .subtitle {
        font-size: 0.9rem;
        color: #666666;
        font-weight: 400;
        line-height: 1.5;
        margin-bottom: 2rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        padding: 0.75rem 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #fafafa;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #333333;
        box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.05);
        background-color: #ffffff;
    }
    
    .stTextInput > label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #333333;
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    /* Button styling (Default/Secondary) */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.65rem 1.5rem;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #ffffff;
        color: #333333;
        cursor: pointer;
        transition: all 0.2s ease;
        /* width: 100%; Removed to allow auto-sizing */
    }
    
    .stButton > button:hover {
        background-color: #f5f5f5;
        border-color: #cccccc;
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }

    /* Primary/Form Submit Button styling */
    [data-testid="stFormSubmitButton"] button {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: none !important;
        width: 100%;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #333333 !important;
    }
    
    /* Result card */
    .result-card {
        background-color: #fafafa;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        text-align: center;
    }
    
    .result-card img {
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* User info */
    .user-info {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #eeeeee;
    }
    
    .user-info .username {
        font-weight: 600;
        font-size: 1rem;
        color: #111111;
    }
    
    .user-info .user-id {
        font-size: 0.85rem;
        color: #888888;
        margin-top: 0.25rem;
    }
    
    /* Download button */
    .stDownloadButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        background-color: #ffffff;
        color: #333333;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 1rem;
    }
    
    .stDownloadButton > button:hover {
        background-color: #f5f5f5;
        border-color: #cccccc;
    }
    
    /* Error message */
    .stAlert {
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #eeeeee;
        margin: 1.5rem 0;
    }
    
    /* Info section */
    .info-section {
        font-size: 0.8rem;
        color: #999999;
        line-height: 1.6;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid #eeeeee;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #333333 transparent transparent transparent;
    }
    
    /* Form styling - align button with input */
    [data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] {
        margin-top: 0;
    }
    
    
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
        height: 42px;
        margin-top: 0;
    }
    
    /* Pill-style buttons for followers/following */
    .pill-container [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
        flex-wrap: wrap !important;
    }
    .pill-container button {
        background: #fff !important;
        border: 1px solid #ddd !important;
        padding: 4px 10px !important;
        border-radius: 16px !important;
        font-size: 0.8rem !important;
        color: #333 !important;
        cursor: pointer !important;
        transition: all 0.15s !important;
        min-height: auto !important;
        height: auto !important;
        line-height: 1.4 !important;
        font-weight: 400 !important;
    }
    .pill-container button:hover {
        background: #f5f5f5 !important;
        border-color: #ccc !important;
        color: #111 !important;
    }
    
    /* Hide 'Press Enter to apply' in text inputs */
    [data-testid="InputInstructions"] {
        display: none !important;
    }
    
    /* Make text inputs inside columns align better with buttons */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stTextInput"] {
        margin-bottom: 0px;
    }
</style>
"""

GEAR_ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 4px;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'''
