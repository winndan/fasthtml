from fasthtml.common import *
from dataclasses import dataclass
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app, rt = fast_app()

@dataclass
class User:
    username: str
    email: str
    password: str

def validate_user(user: User):
    """Validate user registration details"""
    errors = []
    if len(user.username) < 3:
        errors.append("Username must be at least 3 characters long")
    if '@' not in user.email:
        errors.append("Invalid email address")
    if len(user.password) < 8:
        errors.append("Password must be at least 8 characters long")
    return errors

@rt("/")
def get():
    """Render user registration form"""
    return Titled("User Registration", 
        Form(
            Input(type="text", name="username", placeholder="Username", required=True), 
            Input(type="email", name="email", placeholder="Email", required=True), 
            Input(type="password", name="password", placeholder="Password", required=True), 
            Button("Register", type="submit"), 
            hx_post="/register", 
            hx_target="#result"
        ), 
        Div(id="result")
    )

@rt("/register")
def post(user: User):
    """Handle user registration with Supabase"""
    # Validate user input
    errors = validate_user(user)
    if errors:
        return Div(Ul(*[Li(error) for error in errors]), id="result", style="color: red;")
    
    try:
        # Create user in Supabase Authentication
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        
        # Check if user creation was successful
        if response.user:
            # Optionally, store additional user info in a custom users table
            data, count = supabase.table('users').insert({
                'username': user.username,
                'email': user.email,
                'user_id': response.user.id
            }).execute()
            
            return Div(f"Registered: {user.username} ({user.email})", 
                       id="result", 
                       style="color: green;")
        else:
            return Div("Registration failed", id="result", style="color: red;")
    
    except Exception as e:
        # Handle any registration errors
        return Div(f"Error: {str(e)}", id="result", style="color: red;")

serve()