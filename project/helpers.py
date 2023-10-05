from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user

def custom_login_required(redirect_url, login_type):
    def decorator(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("You must be logged in to access this page.", "warning")
                return redirect(url_for(redirect_url, type=login_type, next=request.url))
            return view_func(*args, **kwargs)
        return decorated_view
    return decorator