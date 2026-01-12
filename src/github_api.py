import requests

def get_api_headers(token=None):
    """Get headers for GitHub API requests, including token if provided."""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f"token {token}"
    return headers

def fetch_user_data(username: str, token: str = None, search_mode: str = 'auto') -> tuple:
    """
    Fetch user profile, repositories, followers, and following from GitHub.
    
    Args:
        username: GitHub username or ID
        token: Optional Personal Access Token
        search_mode: 'auto', 'username', or 'id'
        
    Returns:
        tuple: (user_data dict or None, error message or None)
    """
    headers = get_api_headers(token)
    user_data = {}
    
    try:
        # Determine URL based on search mode
        is_numeric = str(username).isdigit()
        
        if search_mode == 'id':
            if not is_numeric:
                return None, "Search mode is 'ID' but input is not a number."
            url = f"https://api.github.com/user/{username}"
        elif search_mode == 'username':
            url = f"https://api.github.com/users/{username}"
        else: # auto
            if is_numeric:
                url = f"https://api.github.com/user/{username}"
            else:
                url = f"https://api.github.com/users/{username}"
            
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # If looked up by ID, we need to ensure we have the login name for other calls
            actual_username = data.get('login')
            user_data = {
                'id': str(data['id']),
                'login': actual_username,  # Store the actual username
                'created_at': data.get('created_at'),
                'avatar_url': data.get('avatar_url'),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'name': data.get('name'),
                'bio': data.get('bio'),
            }
        elif response.status_code == 404:
            return None, f"User '{username}' not found on GitHub. Please check the username and try again."
        elif response.status_code == 403:
            return None, "Rate limit exceeded. GitHub allows 60 requests per hour for unauthenticated users. Please wait a few minutes and try again."
        elif response.status_code == 401:
            return None, "Authentication required. The GitHub API request was not authorized."
        else:
            return None, f"Unable to fetch user data. GitHub responded with status code {response.status_code}."
            
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"

    # Fetch additional lists
    # Use the resolved username (login) just in case the input was an ID
    search_username = user_data.get('login', username)
    
    # Increase per_page to 100 to show more items
    user_data['repos_list'] = _fetch_list(f"https://api.github.com/users/{search_username}/repos?per_page=100&sort=updated", headers, transform_repo)
    user_data['followers_list'] = _fetch_list(f"https://api.github.com/users/{search_username}/followers?per_page=100", headers, lambda x: x['login'])
    user_data['following_list'] = _fetch_list(f"https://api.github.com/users/{search_username}/following?per_page=100", headers, lambda x: x['login'])
    
    return user_data, None

def _fetch_list(url, headers, transform_func):
    """Helper to fetch a list of items and transform them."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return [transform_func(item) for item in response.json()]
    except:
        pass
    return []

def transform_repo(repo):
    """Transform raw repo data into our simplified format."""
    return {
        'name': repo['name'], 
        'description': repo.get('description', ''), 
        'stars': repo.get('stargazers_count', 0), 
        'language': repo.get('language', '')
    }
