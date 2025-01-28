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
        hx_target="#result"  # Ensure this target exists in the DOM
    )

def handle_registration(supabase: Client, user: User):
    """Handle user registration with Supabase."""
    print("Handling registration for user:", user.email)  # Debugging
    
    # Validate user input
    errors = validate_user(user)
    if errors:
        print("Validation errors:", errors)  # Debugging
        return Div(Ul(*[Li(error) for error in errors]), id="result", style="color: red;")
    
    try:
        # Create user in Supabase Authentication
        print("Attempting to sign up user:", user.email)  # Debugging
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        print("Supabase sign-up response:", response)  # Debugging
        
        # Check if user creation was successful
        if response.user:
            print("User created successfully:", response.user.id)  # Debugging
            # Store additional user info in the `users` table (if needed)
            data, count = supabase.table('users').insert({
                'user_id': response.user.id,  # Use the UUID from Supabase Auth
                'username': user.username,
                'email': user.email,
                'display_name': user.display_name,  # Store display name
                'phone_number': user.phone_number     # Store phone number
            }).execute()
            print("User data inserted into 'users' table:", data)  # Debugging
            
            return Div(f"Registered: {user.username} ({user.email}) with display name '{user.display_name}' and phone number '{user.phone_number}'",
                       id="result",
                       style="color: green;")
        else:
            print("Registration failed: No user in response")  # Debugging
            return Div("Registration failed. Please check your email for a confirmation link.", id="result", style="color: red;")
    
    except Exception as e:
        print("Error during registration:", str(e))  # Debugging
        return Div(f"Error: {str(e)}", id="result", style="color: red;")