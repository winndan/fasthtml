from fasthtml.common import *
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from register import render_registration_form, handle_registration, User
import dashboard  # Import dashboard without calling its routes yet
import login  # Import the new login module

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app, rt = fast_app(debug=True)

@rt("/")
def get_registration():
    """Render user registration form"""
    return Titled(
        "User Registration",
        render_registration_form(),
        Div(
            Button("Go to Login Page", onclick="window.location='/login'", style="margin-top: 20px;")  # Redirect button
        )
    )

@rt("/register")
def post_registration(user: User):
    """Handle user registration with Supabase."""
    print("Received registration request for user:", user.email)  # Debugging
    return handle_registration(supabase, user)

@rt("/logout")
def post_logout():
    """Handle user logout."""
    try:
        supabase.auth.sign_out()
        return Redirect("/")  # Redirect to the registration/login page after logout
    except Exception as e:
        return Div(f"Error during logout: {str(e)}", style="color: red;")

# Pass 'rt' and 'supabase' to the dashboard and login modules to define their routes
dashboard.define_routes(rt, supabase)
login.define_routes(rt, supabase)

serve()