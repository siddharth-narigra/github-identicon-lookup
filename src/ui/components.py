import streamlit as st
import requests
from ..styles import GEAR_ICON
from ..utils import format_number, format_account_age, image_to_bytes

def render_token_settings():
    """Render the token settings panel if visible."""
    if st.session_state.get('show_token_settings', False):
        st.markdown('''
        <div style="background: #fffbeb; border: 1px solid #fbbf24; border-radius: 8px; padding: 1.25rem; margin: 0.5rem 0 1rem 0;">
            <p style="margin: 0 0 0.25rem 0; font-weight: 600; font-size: 0.95rem; color: #92400e;">Increase Your Rate Limit</p>
            <p style="margin: 0 0 1rem 0; font-size: 0.85rem; color: #78716c;">Add a free GitHub token to get <strong>5,000 requests/hour</strong> instead of 60.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            token = st.text_input(
                "Token",
                type="password",
                placeholder="Paste your token here (ghp_xxxx...)",
                key="token_input",
                label_visibility="collapsed"
            )
        with col2:
            if st.button("Save", type="primary", use_container_width=True):
                if token:
                    st.session_state['github_token'] = token
                    st.session_state['show_token_settings'] = False
                    st.rerun()
        
        st.markdown('''
        <p style="font-size: 0.75rem; color: #6b7280; margin: 0.5rem 0 0 0; line-height: 1.6;">
            <strong>Get a token:</strong> 
            <a href="https://github.com/settings/tokens" target="_blank" style="color: #2563eb;">github.com/settings/tokens</a> 
            → Generate new token (classic) → No permissions needed → Copy here
        </p>
        ''', unsafe_allow_html=True)

def render_avatar_comparison(user_data, generated_image, generated_username):
    """Render the avatar comparison section."""
    st.markdown("---")
    st.markdown('<p style="font-weight: 600; font-size: 0.9rem; color: #333333; margin-bottom: 0.75rem;">Avatar Comparison</p>', unsafe_allow_html=True)
    
    # Determine correct username for filenames
    display_username = user_data.get('login', generated_username)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p style="font-size: 0.75rem; color: #888888; text-align: center; margin-bottom: 0.5rem;">Default Identicon</p>', unsafe_allow_html=True)
        st.image(generated_image, use_container_width=True)
        
        img_bytes = image_to_bytes(generated_image)
        st.download_button(
            label="Download Default",
            data=img_bytes,
            file_name=f"identicon_{display_username}.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col2:
        st.markdown('<p style="font-size: 0.75rem; color: #888888; text-align: center; margin-bottom: 0.5rem;">Current Avatar</p>', unsafe_allow_html=True)
        avatar_url = user_data.get('avatar_url')
        if avatar_url:
            st.image(avatar_url, use_container_width=True)
            # Try to fetch avatar bytes
            try:
                # We need a small timeout so we don't hang the UI
                response = requests.get(avatar_url, timeout=5)
                if response.status_code == 200:
                    st.download_button(
                        label="Download Current",
                        data=response.content,
                        file_name=f"avatar_{display_username}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.button("Current N/A", disabled=True, use_container_width=True, key="dl_disabled_1")
            except:
                st.button("Current N/A", disabled=True, use_container_width=True, key="dl_disabled_2")
        else:
            st.markdown('<p style="text-align: center; color: #cccccc; padding: 2rem 0;">Not available</p>', unsafe_allow_html=True)
            st.button("Current N/A", disabled=True, use_container_width=True, key="dl_disabled_3")
            
    # Username and ID
    st.markdown(
        f'<p style="text-align: center; margin-top: 1.5rem;">'
        f'<span style="font-weight: 600; font-size: 1.1rem; color: #111111;">{display_username}</span><br>'
        f'<span style="font-size: 0.85rem; color: #888888;">ID: {user_data["id"]}</span>'
        f'</p>',
        unsafe_allow_html=True
    )

def render_account_info(user_data):
    """Render the account information statistics."""
    st.markdown("---")
    st.markdown('<p style="font-weight: 600; font-size: 0.9rem; color: #333333; margin-bottom: 0.75rem;">Account Information</p>', unsafe_allow_html=True)
    
    # Account creation order
    user_id_int = int(user_data['id'])
    order_text = format_number(user_id_int)
    
    # Determine if early adopter
    early_badge = ""
    if user_id_int <= 1000:
        early_badge = '<span style="background: #111111; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; margin-left: 8px;">PIONEER</span>'
    elif user_id_int <= 100000:
        early_badge = '<span style="background: #444444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; margin-left: 8px;">EARLY ADOPTER</span>'
    elif user_id_int <= 1000000:
        early_badge = '<span style="background: #888888; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; margin-left: 8px;">FIRST MILLION</span>'
    
    st.markdown(
        f'<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">'
        f'<p style="margin: 0; font-size: 0.8rem; color: #888888;">Account Creation Order</p>'
        f'<p style="margin: 0.25rem 0 0 0; font-size: 1rem; color: #111111; font-weight: 500;">#{order_text}{early_badge}</p>'
        f'<p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: #aaaaaa;">Approximately the {order_text}th GitHub account created</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Account age
    if user_data.get('created_at'):
        age_str, date_str = format_account_age(user_data['created_at'])
        st.markdown(
            f'<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">'
            f'<p style="margin: 0; font-size: 0.8rem; color: #888888;">Account Age</p>'
            f'<p style="margin: 0.25rem 0 0 0; font-size: 1rem; color: #111111; font-weight: 500;">{age_str}</p>'
            f'<p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: #aaaaaa;">Joined {date_str}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Profile stats
    st.markdown(
        f'<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">'
        f'<p style="margin: 0; font-size: 0.8rem; color: #888888;">Profile Stats</p>'
        f'<div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">'
        f'<div style="text-align: center; flex: 1;">'
        f'<p style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #111111;">{user_data.get("public_repos", 0)}</p>'
        f'<p style="margin: 0; font-size: 0.7rem; color: #888888;">Repositories</p>'
        f'</div>'
        f'<div style="text-align: center; flex: 1; border-left: 1px solid #eeeeee; border-right: 1px solid #eeeeee;">'
        f'<p style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #111111;">{format_number(user_data.get("followers", 0))}</p>'
        f'<p style="margin: 0; font-size: 0.7rem; color: #888888;">Followers</p>'
        f'</div>'
        f'<div style="text-align: center; flex: 1;">'
        f'<p style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #111111;">{format_number(user_data.get("following", 0))}</p>'
        f'<p style="margin: 0; font-size: 0.7rem; color: #888888;">Following</p>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")

def render_repos_list(user_data):
    """Render the list of public repositories."""
    repos_list = user_data.get('repos_list', [])
    repos_count = user_data.get('public_repos', 0)
    
    st.markdown(f'<p style="font-weight: 600; font-size: 0.9rem; color: #333333; margin-bottom: 0.75rem;">Public Repositories ({repos_count})</p>', unsafe_allow_html=True)
    
    if repos_list:
        lang_colors = {
            'Python': '#3572A5', 'JavaScript': '#f1e05a', 'TypeScript': '#2b7489',
            'Java': '#b07219', 'C++': '#f34b7d', 'C': '#555555', 'C#': '#178600',
            'Go': '#00ADD8', 'Rust': '#dea584', 'Ruby': '#701516', 'PHP': '#4F5D95',
            'Swift': '#ffac45', 'Kotlin': '#F18E33', 'HTML': '#e34c26', 'CSS': '#563d7c',
            'Shell': '#89e051', 'Jupyter Notebook': '#DA5B0B', 'Vue': '#2c3e50',
            'Dart': '#00B4AB', 'R': '#198CE7', 'Scala': '#c22d40', 'Lua': '#000080',
        }
        
        repos_cards = []
        for repo in repos_list:
            repo_name = repo.get('name', '')
            repo_lang = repo.get('language', '') or ''
            repo_stars = repo.get('stars', 0)
            repo_desc = (repo.get('description', '') or '')[:80]
            if len(repo.get('description', '') or '') > 80:
                repo_desc += "..."
            
            lang_color = lang_colors.get(repo_lang, '#888888')
            lang_html = f'<span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 10px; height: 10px; border-radius: 50%; background: {lang_color};"></span><span style="font-size: 0.75rem; color: #666;">{repo_lang}</span></span>' if repo_lang else ''
            stars_html = f'<span style="font-size: 0.75rem; color: #666;">* {repo_stars}</span>' if repo_stars > 0 else ''
            desc_html = f'<p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #666; line-height: 1.4;">{repo_desc}</p>' if repo_desc else ''
            
            meta_items = [x for x in [lang_html, stars_html] if x]
            meta_html = f'<div style="display: flex; gap: 1rem; margin-top: 0.5rem;">{" ".join(meta_items)}</div>' if meta_items else ''
            
            card = f'<div style="background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 0.875rem; margin-bottom: 0.5rem; transition: all 0.2s;"><p style="margin: 0; font-weight: 600; font-size: 0.9rem; color: #111;">{repo_name}</p>{desc_html}{meta_html}</div>'
            repos_cards.append(card)
        
        repos_container = f'<div style="max-height: 320px; overflow-y: auto; padding-right: 4px;">{"".join(repos_cards)}</div>'
        st.markdown(repos_container, unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; color: #888; font-size: 0.85rem;">No public repositories</div>', unsafe_allow_html=True)

def render_follow_list(title, items, total_count, key_prefix):
    """Render a list of followers or following as clickable pills."""
    # Use the total count passed from API data
    display_count = total_count if total_count is not None else len(items)
    
    st.markdown(f'<p style="font-weight: 600; font-size: 0.9rem; color: #333333; margin-bottom: 0.75rem; margin-top: 1.5rem;">{title} ({format_number(display_count)})</p>', unsafe_allow_html=True)
    
    if items:
        # Display the pills (limited to first 100 or so from API)
        # Increased max-height to 350px to show more items
        html_content = '<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.5rem; max-height: 350px; overflow-y: auto;">'
        for item in items:
            html_content += f'<span style="background: #fff; border: 1px solid #ddd; padding: 4px 10px; border-radius: 16px; font-size: 0.8rem; color: #333; cursor: pointer;">{item}</span>'
        
        # If the list is truncated (Api limit 100 vs Total > 100), we can show a small caption
        if display_count > len(items):
             html_content += f'<div style="width: 100%; text-align: center; color: #999; font-size: 0.75rem; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px dashed #eee;">Showing top {len(items)} of {format_number(display_count)}</div>'

        html_content += '</div>'
        st.markdown(html_content, unsafe_allow_html=True)
            
        return None
    else:
        st.markdown(f'<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; color: #888; font-size: 0.85rem;">No {title.lower()}</div>', unsafe_allow_html=True)
        return None

def render_hash_breakdown(user_data):
    """Render the hash breakdown educational section."""
    st.markdown("---")
    st.markdown('<p style="font-weight: 600; font-size: 0.9rem; color: #333333; margin-bottom: 0.75rem;">Hash Breakdown</p>', unsafe_allow_html=True)
    
    hex_hash = user_data.get('md5_hash', '')
    color_hex = user_data.get('color_hex', '#000')
    color_rgb = user_data.get('color_rgb', (0,0,0))
    
    if not hex_hash:
        return

    st.markdown(
        f'<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">'
        f'<p style="margin: 0; font-size: 0.8rem; color: #888888;">MD5 Hash of User ID</p>'
        f'<p style="margin: 0.5rem 0 0 0; font-family: monospace; font-size: 0.85rem; color: #111111; word-break: break-all;">'
        f'<span style="background: #e8f4e8; padding: 1px 3px; border-radius: 2px;" title="Pattern (first 15 nibbles)">{hex_hash[:15]}</span>'
        f'<span style="color: #cccccc;">{hex_hash[15:25]}</span>'
        f'<span style="background: #e8e8f4; padding: 1px 3px; border-radius: 2px;" title="Hue">{hex_hash[25:28]}</span>'
        f'<span style="background: #f4e8e8; padding: 1px 3px; border-radius: 2px;" title="Saturation">{hex_hash[28:30]}</span>'
        f'<span style="background: #f4f4e8; padding: 1px 3px; border-radius: 2px;" title="Lightness">{hex_hash[30:32]}</span>'
        f'</p>'
        f'<div style="display: flex; gap: 1rem; margin-top: 0.75rem; font-size: 0.7rem; color: #888888; flex-wrap: wrap;">'
        f'<span><span style="background: #e8f4e8; padding: 1px 4px; border-radius: 2px;">green</span> Pattern</span>'
        f'<span><span style="background: #e8e8f4; padding: 1px 4px; border-radius: 2px;">blue</span> Hue</span>'
        f'<span><span style="background: #f4e8e8; padding: 1px 4px; border-radius: 2px;">red</span> Saturation</span>'
        f'<span><span style="background: #f4f4e8; padding: 1px 4px; border-radius: 2px;">yellow</span> Lightness</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Derived color
    st.markdown(
        f'<div style="background: #fafafa; border: 1px solid #eeeeee; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">'
        f'<p style="margin: 0; font-size: 0.8rem; color: #888888;">Derived Color</p>'
        f'<div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.5rem;">'
        f'<div style="width: 48px; height: 48px; background: {color_hex}; border-radius: 8px; border: 1px solid #eeeeee;"></div>'
        f'<div>'
        f'<p style="margin: 0; font-family: monospace; font-size: 0.95rem; color: #111111; font-weight: 500;">{color_hex.upper()}</p>'
        f'<p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: #888888;">RGB({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})</p>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def render_how_it_works():
    """Render the detailed educational section."""
    st.markdown("---")
    st.markdown('<p style="font-weight: 600; font-size: 1rem; color: #111; margin-bottom: 1rem;">The Logic Behind Your Identicon</p>', unsafe_allow_html=True)

    st.markdown('''
    <p style="margin: 0 0 1.5rem 0; color: #555; font-size: 0.85rem; line-height: 1.6;">
    Every GitHub user has a unique <strong>fingerprint</strong> — not stored as an image, but as a mathematical formula 
    waiting to be rendered. This tool doesn't fetch your identicon; it <strong>reconstructs</strong> it using the same 
    algorithm GitHub uses internally.
    </p>
    ''', unsafe_allow_html=True)

    # 1. The Pipeline Visual
    st.markdown('''
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 10px;">
        <div style="background: #fafafa; padding: 8px 12px; border-radius: 6px; border: 1px solid #eee; font-size: 0.75rem; color: #333;">User ID</div>
        <div style="color: #ccc;">→</div>
        <div style="background: #fafafa; padding: 8px 12px; border-radius: 6px; border: 1px solid #eee; font-size: 0.75rem; color: #333;">MD5 Hash</div>
        <div style="color: #ccc;">→</div>
        <div style="background: #fafafa; padding: 8px 12px; border-radius: 6px; border: 1px solid #eee; font-size: 0.75rem; color: #333;">Last 7 Nibbles (Color)</div>
        <div style="color: #ccc;">+</div>
        <div style="background: #fafafa; padding: 8px 12px; border-radius: 6px; border: 1px solid #eee; font-size: 0.75rem; color: #333;">First 15 Nibbles (Grid)</div>
        <div style="color: #ccc;">→</div>
        <div style="background: #333; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">Identicon</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 2. Step 1: Hash
    st.markdown('<p style="font-weight: 600; font-size: 0.9rem; color: #333; margin-top: 1.5rem; margin-bottom: 0.5rem;">1. The Hash Function</p>', unsafe_allow_html=True)
    st.markdown(r'''
    <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
    Everything starts with your User ID. To ensure the image is uniform and unpredictable (but consistent), 
    we apply the <strong>MD5 hashing algorithm</strong>. This turns your simple numeric ID into a long string of 32 hexadecimal characters.
    </p>
    ''', unsafe_allow_html=True)
    
    # 3. Step 2: Color
    st.markdown('<p style="font-weight: 600; font-size: 0.9rem; color: #333; margin-top: 1.5rem; margin-bottom: 0.5rem;">2. Extracting the Color</p>', unsafe_allow_html=True)
    st.markdown(r'''
    <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
    GitHub's algorithm doesn't pick random colors. It strictly determines the color from the <strong>last 7 characters</strong> of your hash.
    It uses the HSL (Hue, Saturation, Lightness) color model because it produces more aesthetically pleasing results than RGB.
    </p>
    <ul style="margin: 0.5rem 0 0 1rem; color: #666; font-size: 0.85rem; line-height: 1.6;">
        <li><strong>Hue:</strong> Derived from the last 3 nibbles.</li>
        <li><strong>Saturation:</strong> Derived from the 2 nibbles before that. Limits: [45%, 65%] to ensure vibrancy.</li>
        <li><strong>Lightness:</strong> Derived from the 2 nibbles before that. Limits: [55%, 75%] to ensure visibility on white.</li>
    </ul>
    ''', unsafe_allow_html=True)

    # 4. Step 3: Pattern
    st.markdown('<p style="font-weight: 600; font-size: 0.9rem; color: #333; margin-top: 1.5rem; margin-bottom: 0.5rem;">3. Building the Pattern</p>', unsafe_allow_html=True)
    st.markdown('''
    <p style="color: #666; font-size: 0.85rem; line-height: 1.6;">
    The identicon is a <strong>5x5 pixel grid</strong>. The pattern is determined by the <strong>first 15 characters</strong> of your hash.
    Since 15 characters isn't enough to fill 25 cells, there's a trick: <strong>Mirror Symmetry</strong>.
    </p>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="background: #f8f9fa; border-left: 3px solid #333; padding: 12px 16px; margin: 1rem 0; border-radius: 0 4px 4px 0;">
        <p style="margin: 0; font-size: 0.85rem; color: #555; line-height: 1.6;">
        <strong>The Algorithm:</strong><br>
        1. Take the first 15 nibbles.<br>
        2. If a nibble is <strong>even</strong>, color the cell. If odd, leave it white.<br>
        3. Fill the first 3 columns of the 5x5 grid.<br>
        4. Mirror the first and second columns to create the 4th and 5th columns.<br>
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <p style="color: #666; font-size: 0.85rem; line-height: 1.6; margin-top: 1.5rem;">
    This vertical symmetry is why almost all GitHub identicons look like little faces or creatures!
    </p>
    ''', unsafe_allow_html=True)
