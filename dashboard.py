# dashboard.py

from fasthtml.common import *
from supabase import Client

def render_dashboard(user):
    """Render the user dashboard after login."""
    return Titled(
        "Dashboard",
        Div(f"Welcome, {user['email']}!", style="font-size: 24px;"),  # Access email as a dictionary key
        Div("This is your dashboard. You can manage your account here.", style="margin-top: 20px;"),
        Button("Logout", type="button", hx_post="/logout", hx_target="#logout_result"),
        Div(id="logout_result")
    )

def define_routes(rt):
    """Define routes for the dashboard."""
    
    @rt("/dashboard")
    def get_dashboard():
        """Render the dashboard page."""
        # Simulate getting the logged-in user (replace with actual logic)
        # Example: Replace this with actual Supabase authentication logic
        user = {"email": "test@example.com"}  # Simulated user dictionary
        
        if not user:
            return Div("You need to log in first.", style="color: red;")
        
        return render_dashboard(user)
