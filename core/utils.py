"""
Utility functions for PlanMyValentine
"""
import hashlib
import random
import string


def generate_share_code(your_name, partner_name):
    """Generate a unique share code for the plan"""
    # Create a URL-friendly code from names
    base = f"{your_name}-{partner_name}".lower()
    base = ''.join(c if c.isalnum() or c == '-' else '-' for c in base)
    
    # Add random suffix for uniqueness
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base}-{suffix}"


def format_budget(amount):
    """Format budget in Indian currency format"""
    try:
        amount = int(amount)
        if amount >= 10000000:  # 1 crore
            return f"₹{amount/10000000:.1f}Cr"
        elif amount >= 100000:  # 1 lakh
            return f"₹{amount/100000:.1f}L"
        elif amount >= 1000:
            return f"₹{amount/1000:.1f}K"
        else:
            return f"₹{amount}"
    except:
        return f"₹{amount}"


def get_relationship_emoji(relationship_type):
    """Get emoji for relationship type"""
    emojis = {
        'girlfriend': '❤️',
        'boyfriend': '❤️',
        'crush': '😏',
        'best_friend': '🫂',
        'self_love': '😌',
    }
    return emojis.get(relationship_type, '💘')


def get_vibe_emoji(vibe):
    """Get emoji for vibe"""
    emojis = {
        'romantic': '💕',
        'funny': '😄',
        'crazy': '🤪',
        'spiritual': '🙏',
        'filmy': '🎬',
    }
    return emojis.get(vibe, '✨')
