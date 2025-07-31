import panel as pn
from app.services.api_client import api_client
from app.views.login_view import create_login_view
from app.views.dashboard_components import create_metric_cards, create_charts_view, create_filter_widgets

# Configure the page
pn.extension(sizing_mode="stretch_width", notifications=True)

class AppController:
    """Manages the application state and view by controlling a single root template."""

    def __init__(self):
        self.template = pn.template.MaterialTemplate(
            title="Spend Tracker",
            header_background="#2F4F4F",
        )
        if 'auth_token' in pn.state.cache:
            self.build_dashboard_view(pn.state.cache['auth_token'])
        else:
            self.build_login_view()

    def build_login_view(self, event=None):
        """Clears the template and populates it with the login interface."""
        if 'auth_token' in pn.state.cache:
            del pn.state.cache['auth_token']
        
        self.template.sidebar.clear()
        self.template.sidebar_width = 0
        self.template.main.clear()

        login_form = create_login_view(on_login_success=self.on_login_success)
        # Create a fully centered layout with better vertical and horizontal centering
        centered_login = pn.Column(
            pn.layout.VSpacer(),  # Top spacer
            login_form,           # The login form (already horizontally centered)
            pn.layout.VSpacer(),  # Bottom spacer
            sizing_mode="stretch_both",
            styles={'background': '#f5f5f5'}  # Light background for better contrast
        )
        self.template.main.append(centered_login)

    def on_login_success(self, token: str):
        """Stores the auth token and forces a page reload to show the dashboard."""
        pn.state.cache['auth_token'] = token
        pn.state.location.reload = True

    def on_logout(self, event=None):
        """Clears the auth token and forces a page reload to show the login screen."""
        if 'auth_token' in pn.state.cache:
            del pn.state.cache['auth_token']
        pn.state.location.reload = True

    def build_dashboard_view(self, token: str):
        """Clears the template and populates it with the dashboard interface."""
        # --- Fetch User Information ---
        user_info = api_client.get_user_info(token)
        
        # Extract first name from full name (fallback to username if no full name)
        full_name = user_info.get('full_name', '')
        username = user_info.get('username', 'User')
        
        if full_name:
            # Get first part of the full name (before first space)
            first_name = full_name.split()[0] if full_name.split() else username
        else:
            first_name = username

        # --- Configure Template ---
        self.template.main.clear()
        self.template.sidebar.clear()
        self.template.sidebar_width = 300

        # --- Fetch Data ---
        transactions_df = api_client.get_transactions(token)

        # --- Build Sidebar ---
        logout_button = pn.widgets.Button(name="Logout", icon="logout", button_type="primary", sizing_mode="stretch_width")
        logout_button.on_click(self.on_logout)

        sidebar_content = pn.Column(
            pn.pane.Markdown(
                f"### Welcome,\n# {first_name}", 
                styles={
                    'font-size': '18px',
                    'font-weight': 'bold',
                    'color': '#2F4F4F'
                }
            ),
            pn.layout.Divider(),
            "**Filters**"
        )
        self.template.sidebar.append(sidebar_content)

        if transactions_df.empty:
            self.template.main.append(pn.pane.Alert("Could not load transaction data.", alert_type="warning"))
            sidebar_content.append(pn.layout.VSpacer())
            sidebar_content.append(logout_button)
            return

        # --- Create and Add Filters to Sidebar ---
        filter_widgets = create_filter_widgets(transactions_df)
        date_filter = filter_widgets['date_range']
        category_filter = filter_widgets['categories']
        sidebar_content.append(date_filter)
        sidebar_content.append(category_filter)
        sidebar_content.append(pn.layout.VSpacer())
        sidebar_content.append(logout_button)

        # --- Create Reactive Data Pipeline ---
        # NOTE: Caching can be re-enabled for performance in production
        # @pn.cache
        def get_filtered_data(start_date, end_date, categories):
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'), 
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            
            # Format categories as comma-separated string (only if categories are selected)
            if categories and len(categories) > 0:
                params['categories'] = ','.join(categories)
            
            # Debug: Print filter parameters
            print(f"DEBUG - Filter params: {params}")
            print(f"DEBUG - Selected categories: {categories}")
            
            # Fetch both transactions and metrics reactively
            transactions = api_client.get_transactions(token, params=params)
            metrics = api_client.get_metrics(token, params=params)
            
            return transactions, metrics

        bound_data = pn.bind(get_filtered_data, start_date=date_filter.param.value_start, end_date=date_filter.param.value_end, categories=category_filter.param.value)

        def get_metrics_view(data):
            transactions, metrics = data
            return create_metric_cards(metrics)

        def get_charts_view(data):
            transactions, _ = data
            return create_charts_view(transactions)

        # --- Populate Main Area with Reactive Components ---
        self.template.main.append(
            pn.Column(
                pn.bind(get_metrics_view, data=bound_data),
                pn.bind(get_charts_view, data=bound_data)
            )
        )

    def get_view(self):
        """Returns the main servable template."""
        return self.template

# Create an instance of the controller and make it servable
app = AppController()
app.get_view().servable(title="Analytics Dashboard") 