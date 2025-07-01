### ✅ Phase 5: Frontend (Panel) Setup

**Goal:** To build an interactive web dashboard using Panel that allows a logged-in user to visualize and filter their spending data from the backend API.

*   **Task 5.1: Initial Setup & Dependencies**
    *   [x] Update `frontend/requirements.txt` with necessary libraries: `panel==1.4.1`, `pandas`, `holoviews`, `bokeh`, `requests`.
    *   [x] Create a modular file structure inside `frontend/` for better organization (e.g., `app/`, `app/views/`, `app/services/`).

*   **Task 5.2: API Client Service**
    *   [x] Create an `api_client.py` service to handle all communication with the backend.
    *   [x] Implement a function to handle `/login` requests.
    *   [x] Implement functions to fetch data from `/transactions` and `/metrics`, including passing the auth token in headers.
    *   [x] Add error handling for API requests (e.g., 401 Unauthorized, connection errors).

*   **Task 5.3: Login View**
    *   [x] Create a `login_view.py` to define the login screen.
    *   [x] Add a title "Customer Spending Analytics".
    *   [x] Create username and password input widgets and a login button.
    *   [x] Implement the callback for the login button that uses the `api_client` to authenticate and stores the JWT token upon success.
    *   [x] Add a notification/alert for failed login attempts.

*   **Task 5.4: Dashboard View & Layout**
    *   [x] Create a `dashboard_view.py`.
    *   [x] Use `pn.template.MaterialTemplate` for the layout.
    *   [x] Define a sidebar for filters and a logout button.
    *   [x] Define a main area for metrics and charts.

*   **Task 5.5: Dashboard Components**
    *   [x] **Metric Cards:** Create a function to display the `/metrics` data using `pn.indicators.Number`.
    *   [x] **Charts:**
        *   [x] Create a function to generate a bar chart for spending by category using HoloViews.
        *   [x] Create a function to generate a line chart for spending over time using HoloViews.
        *   [x] Create a function to generate a pie chart for category proportions using HoloViews.
    *   [x] **Filters:**
        *   [x] Create a `pn.widgets.DateRangeSlider` for date filtering.
        *   [x] Create a `pn.widgets.MultiChoice` for category filtering. The options for this should be dynamically populated based on the user's data.

*   **Task 5.6: Integration & State Management**
    *   [ ] In `main.py`, create a main controller class or function to manage application state.
    *   [ ] Implement logic to show the `login_view` by default and switch to the `dashboard_view` upon successful login.
    *   [ ] Store the JWT token securely in `panel.state.cache` or a similar state management approach.
    *   [ ] Wire up the filter widgets to a callback function. This function will re-fetch data from the API using the new filter values and update all charts and metrics.
    *   [ ] Implement the logout button functionality, which should clear the token and return to the login screen.

*   **Task 5.7: Final Polish & Testing**
    *   [ ] Ensure the UI is responsive and handles empty states gracefully (e.g., when there is no data for a selected filter).
    *   [ ] Test the complete user flow: login -> view dashboard -> apply filters -> logout. 