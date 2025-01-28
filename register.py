# register.py

from fasthtml.common import *
from dataclasses import dataclass
from supabase import Client

@dataclass
class User:
    username: str
    email: str
    password: str
    display_name: str  # Added display name
    phone_number: str  # Added phone number

def validate_user(user: User):
    """Validate user registration details"""
    errors = []
    if len(user.username) < 3:
        errors.append("Username must be at least 3 characters long.")
    if '@' not in user.email:
        errors.append("Invalid email address.")
    if len(user.password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if len(user.display_name) < 1:
        errors.append("Display name cannot be empty.")
    if len(user.phone_number) < 10 or not user.phone_number.isdigit():
        errors.append("Phone number must be at least 10 digits long and contain only numbers.")
    return errors

def render_registration_form():
    """Render the user registration form."""
    return Form(
        Input(type="text", name="username", placeholder="Username", required=True), 
        Input(type="email", name="email", placeholder="Email", required=True), 
        Input(type="password", name="password", placeholder="Password", required=True), 
        Input(type="text", name="display_name", placeholder="Display Name", required=True),  # New field for display name
        Input(type="text", name="phone_number", placeholder="Phone Number", required=True),  # New field for phone number
        Button("Register", type="submit"), 
        hx_post="/register",
        hx_target="#result"
    )

def handle_registration(supabase: Client, user: User):
    """Handle user registration with Supabase."""
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
            # Store additional user info in a custom users table including display_name and phone_number
            data, count = supabase.table('users').insert({
                'username': user.username,
                'email': user.email,
                'user_id': response.user.id,
                'display_name': user.display_name,  # Store display name here
                'phone_number': user.phone_number     # Store phone number here
            }).execute()
            
            return Div(f"Registered: {user.username} ({user.email}) with display name '{user.display_name}' and phone number '{user.phone_number}'",
                       id="result",
                       style="color: green;")
        else:
            return Div("Registration failed.", id="result", style="color: red;")
    
    except Exception as e:
        # Handle any registration errors
        return Div(f"Error: {str(e)}", id="result", style="color: red;")
