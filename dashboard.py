from fasthtml.common import *
from supabase import Client

def render_dashboard(user):
    """Render the user dashboard after login."""
    return Titled(
        "Dashboard",
        Div(f"Welcome, {user['email']}!", style="font-size: 24px;"),  # Access email as a dictionary key
        Div(f"User ID: {user['id']}", style="margin-top: 20px;"),
        Div(f"Created At: {user['created_at']}", style="margin-top: 20px;"),
        Div("This is your dashboard. You can manage your account here.", style="margin-top: 20px;"),
        Button("Logout", type="button", hx_post="/logout", hx_target="#logout_result"),
        Div(id="logout_result")
    )

def define_routes(rt, supabase: Client):
    """Define routes for the dashboard."""
    
    @rt("/dashboard")
    def get_dashboard():
        """Render the dashboard page."""
        # Get the current session
        session = supabase.auth.get_session()
        
        if not session:
            return Div("You need to log in first.", style="color: red;")
        
        # Fetch user details from Supabase Auth
        try:
            user = supabase.auth.get_user().user
            if user:
                return render_dashboard({
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at
                })
            else:
                return Div("User details not found.", style="color: red;")
        except Exception as e:
            return Div(f"Error fetching user details: {str(e)}", style="color: red;")