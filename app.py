"""
GitHub Identicon Generator - Streamlit Interface
A minimal, clean interface for generating GitHub-style identicons.
"""

import streamlit as st
from src.styles import CSS, GEAR_ICON
from src.github_api import fetch_user_data
from src.identicon import generate_identicon_from_id
from src.ui.components import (
    render_token_settings,
    render_avatar_comparison,
    render_account_info,
    render_repos_list,
    render_hash_breakdown,
    render_how_it_works,
    render_follow_list
)

# Page configuration
st.set_page_config(
    page_title="GitHub Default Identicon Lookup",
    page_icon="assets/favicon.ico",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(CSS, unsafe_allow_html=True)


def generate_identicon_workflow(username: str, search_mode: str = 'auto') -> tuple:
    """
    Orchestrate the generation workflow: fetch data -> generate image.
    Uses session state for token if available.
    """
    token = st.session_state.get('github_token')
    
    # 1. Fetch data from GitHub API
    user_data, error = fetch_user_data(username, token, search_mode)
    
    if error:
        return None, None, error
        
    # 2. Generate identicon from User ID
    # Note: user_data['id'] is guaranteed to exist if no error
    img, metadata = generate_identicon_from_id(user_data['id'])
    
    # Merge metadata (hash, color, etc.) into user_data
    user_data.update(metadata)
    
    return img, user_data, None


# Main UI
st.title("GitHub Default Identicon")

st.markdown(
    '<p class="subtitle">Discover the original default identicon for any GitHub account. '
    'Even if a user has changed their profile picture, their default identicon remains tied to their account ID.</p>',
    unsafe_allow_html=True
)

with st.form(key="lookup_form"):
    # Search Mode Selection
    st.markdown('<p style="font-size: 0.8rem; font-weight: 500; color: #555; margin-bottom: 0px;">Search Mode</p>', unsafe_allow_html=True)
    search_option = st.radio(
        "Search Mode",
        options=["Username", "User ID"],
        horizontal=True,
        label_visibility="collapsed",
        key="search_mode_input"
    )

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True) # Spacer

    col1, col2 = st.columns([5, 1])
    with col1:
        username = st.text_input(
            "GitHub Username",
            placeholder="Enter a username (e.g., 'octocat') or ID (e.g., '1')",
            key="username_input",
            label_visibility="collapsed"
        )
    with col2:
        submit = st.form_submit_button("Look Up", type="primary", use_container_width=True)

# Map selection to API mode
mode_map = {
    "Username": "username",
    "User ID": "id"
}
selected_mode = mode_map[search_option]

# Helper for handling lookup
def handle_lookup(target_username, mode):
    if not target_username or not target_username.strip():
        st.warning("Please enter a GitHub username")
        return

    with st.spinner("Looking up..."):
        img, user_data, error = generate_identicon_workflow(target_username.strip(), mode)
        
        if error:
            st.error(error)
            # Check if rate limit error
            if "rate limit" in error.lower() or "Rate limit" in error:
                st.session_state['show_token_settings'] = True
        else:
            # Store in session state
            st.session_state['generated_image'] = img
            st.session_state['generated_username'] = target_username.strip()
            st.session_state['user_data'] = user_data
            st.session_state['show_token_settings'] = False

# Handle form submission
if submit:
    handle_lookup(username, selected_mode)

# Render Token Settings (only if rate limit hit)
render_token_settings()

# Display result
if 'generated_image' in st.session_state and 'user_data' in st.session_state:
    user_data = st.session_state['user_data']
    img = st.session_state['generated_image']
    gen_username = st.session_state['generated_username']
    
    # Section 1: Avatar Comparison
    render_avatar_comparison(user_data, img, gen_username)
    
    # Section 2: Account Info
    render_account_info(user_data)
    
    # Section 3: Repositories
    render_repos_list(user_data)
    
    # Section 4: Followers
    # Note: Currently these are static HTML pills as per request.
    # If we wanted them clickable, we'd need to refactor render_follow_list to use buttons 
    # and handle the click here loop.
    # Section 4: Followers
    # Note: Currently these are static HTML pills as per request.
    # If we wanted them clickable, we'd need to refactor render_follow_list to use buttons 
    # and handle the click here loop.
    render_follow_list("Followers", user_data.get('followers_list', []), user_data.get('followers', 0), "fl")
    
    # Section 5: Following
    render_follow_list("Following", user_data.get('following_list', []), user_data.get('following', 0), "fw")
    
    # Section 6: Hash Breakdown
    render_hash_breakdown(user_data)

# Info Section
render_how_it_works()
