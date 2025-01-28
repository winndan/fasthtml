from fasthtml.common import *
from supabase import Client

def render_login_form():
    """Render the login form."""
    return Form(
        Input(type="email", name="login_email", placeholder="Email", required=True),
        Input(type="password", name="login_password", placeholder="Password", required=True),
        Button("Login", type="submit"),
        hx_post="/login_post",
        hx_target="#login_result"
    )

def define_routes(rt: Router, supabase: Client):
    @rt("/login")
    def get_login():
        """Render login page."""
        return Titled(
            "User Login",
            render_login_form(),
            Div(id="login_result"),
            Div(
                Button("Back to Registration Page", onclick="window.location='/'", style="margin-top: 20px;")  # Redirect button
            )
        )

    @rt("/login_post")
    def post_login(login_email: str, login_password: str):
        """Handle user login with Supabase."""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": login_email,
                "password": login_password,
            })

            if response.user:
                return Redirect("/dashboard")  # Redirect to the dashboard on successful login
            else:
                return Div("Login failed. Please check your credentials.", id="login_result", style="color: red;")

        except Exception as e:
            return Div(f"Error: {str(e)}", id="login_result", style="color: red;")
