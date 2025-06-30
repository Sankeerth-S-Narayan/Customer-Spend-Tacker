import panel as pn
import panel.widgets as pnw
from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets

# Import the API client
from app.services.api_client import api_client

def create_login_view(on_login_success):
    """
    Creates the login view with all its components and logic.

    Args:
        on_login_success: A callback function to be executed upon successful login.
                          This function should accept the JWT token as an argument.

    Returns:
        A Panel Column containing the login UI.
    """
    # 1. Create Widgets
    title = pn.pane.Markdown("## 📈 Customer Spending Analytics", sizing_mode="stretch_width", styles={'text-align': 'center'})
    username_input = pnw.TextInput(name="Username", placeholder="Enter your username...")
    password_input = pnw.PasswordInput(name="Password", placeholder="Enter your password...")
    login_button = pnw.Button(name="Login", button_type="primary")
    
    # An alert pane to show login status
    alert_pane = pn.pane.Alert(alert_type="danger", visible=False)

    # 2. Define the Login Callback
    def login_callback(event):
        """Handle the login button click event."""
        alert_pane.visible = False  # Hide alert on new attempt
        
        # Get credentials
        username = username_input.value
        password = password_input.value
        
        if not username or not password:
            alert_pane.object = "Username and password are required."
            alert_pane.alert_type = "warning"
            alert_pane.visible = True
            return
            
        # Attempt to login via the API client
        token = api_client.login(username, password)
        
        if token:
            # On success, execute the provided callback
            on_login_success(token)
        else:
            # On failure, show an error message
            alert_pane.object = "Login failed. Please check your credentials."
            alert_pane.alert_type = "danger"
            alert_pane.visible = True

    # 3. Link the callback to the button
    login_button.on_click(login_callback)

    # 4. Arrange components in a layout
    login_layout = pn.Column(
        title,
        pn.layout.Divider(),
        username_input,
        password_input,
        login_button,
        alert_pane,
        sizing_mode="stretch_width",
        max_width=400,  # Constrain width for a cleaner look
        align='center',
    )
    
    return login_layout 