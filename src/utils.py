from datetime import datetime
from PIL import Image
import io

def format_account_age(created_at_str: str) -> tuple:
    """Calculate and format account age from ISO date string."""
    if not created_at_str:
        return None, None
    
    # Handle 'Z' for UTC if present
    created = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
    now = datetime.now(created.tzinfo)
    delta = now - created
    
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = delta.days % 30
    
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    if days > 0 and years == 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    age_str = ", ".join(parts) if parts else "Less than a day"
    date_str = created.strftime("%B %d, %Y")
    
    return age_str, date_str


def format_number(n: int) -> str:
    """Format large numbers with commas."""
    return f"{n:,}"


def image_to_bytes(img: Image.Image) -> bytes:
    """Convert PIL Image to bytes for download."""
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()
