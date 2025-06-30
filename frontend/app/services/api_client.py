import requests
import pandas as pd
from typing import Dict, Any, Optional, List

# The base URL for the backend API, accessible within the Docker network
API_BASE_URL = "http://backend:8000/api/v1"


class ApiClient:
    """
    A client to handle all interactions with the backend FastAPI application.
    """

    def __init__(self, base_url: str = API_BASE_URL):
        """
        Initializes the API client.
        Args:
            base_url: The base URL for the API endpoints.
        """
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username: str, password: str) -> str | None:
        """
        Authenticates the user and returns a JWT token.
        Args:
            username: The user's email/username.
            password: The user's password.
        Returns:
            The JWT access token if authentication is successful, otherwise None.
        """
        login_url = f"{self.base_url}/login"
        form_data = {"username": username, "password": password}
        try:
            response = self.session.post(login_url, data=form_data)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during login: {e}")
            return None

    def _get_auth_headers(self, token: str) -> dict:
        """Constructs authorization headers."""
        return {"Authorization": f"Bearer {token}"}

    def get_transactions(self, token: str, params: dict | None = None) -> pd.DataFrame:
        """
        Fetches transaction data from the API.
        Args:
            token: The JWT access token.
            params: A dictionary of query parameters for filtering.
        Returns:
            A pandas DataFrame with transaction data, or an empty DataFrame on error.
        """
        transactions_url = f"{self.base_url}/transactions"
        headers = self._get_auth_headers(token)
        try:
            response = self.session.get(transactions_url, headers=headers, params=params)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred fetching transactions: {e}")
            return pd.DataFrame()

    def get_metrics(self, token: str, params: dict | None = None) -> dict:
        """
        Fetches analytics metrics from the API.
        Args:
            token: The JWT access token.
            params: A dictionary of query parameters for filtering.
        Returns:
            A dictionary with metrics, or an empty dictionary on error.
        """
        metrics_url = f"{self.base_url}/transactions/metrics"
        headers = self._get_auth_headers(token)
        try:
            response = self.session.get(metrics_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred fetching metrics: {e}")
            return {}

# A global instance of the API client that can be imported elsewhere
api_client = ApiClient() 