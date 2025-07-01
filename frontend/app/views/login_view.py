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
    # 1. Create Widgets with improved styling
    title = pn.pane.Markdown(
        "# 📈 Customer Spending Analytics", 
        styles={
            'text-align': 'center',
            'color': '#2F4F4F',
            'font-weight': 'bold',
            'margin-bottom': '20px'
        }
    )
    username_input = pnw.TextInput(
        name="Username", 
        placeholder="Enter your username...", 
        sizing_mode="stretch_width",
        height=45
    )
    password_input = pnw.PasswordInput(
        name="Password", 
        placeholder="Enter your password...", 
        sizing_mode="stretch_width",
        height=45
    )
    login_button = pnw.Button(
        name="Login", 
        button_type="primary", 
        sizing_mode="stretch_width",
        height=45,
        styles={'font-size': '16px', 'font-weight': 'bold'}
    )
    
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

    # 4. Create a centered login card with better styling
    login_card = pn.Column(
        title,
        pn.layout.Divider(),
        username_input,
        password_input,
        login_button,
        alert_pane,
        width=400,  # Fixed width for consistent appearance
        margin=(40, 20, 40, 20),  # Add padding around the form
        styles={
            'background': 'white',
            'border-radius': '10px',
            'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'padding': '30px'
        }
    )
    
    # 5. Create the complete centered layout
    login_layout = pn.Row(
        pn.layout.HSpacer(),  # Left spacer
        login_card,           # The login form card
        pn.layout.HSpacer(),  # Right spacer
        sizing_mode="stretch_width",
        height=600,  # Give it enough height
        align='center'
    )
    
    return login_layout 