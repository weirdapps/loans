"""Tests for the Flask loan calculator application."""


class TestAppCreation:
    """Tests for Flask app setup."""

    def test_app_creates_successfully(self, app):
        """Flask app instance is created and configured for testing."""
        assert app is not None
        assert app.config["TESTING"] is True

    def test_security_headers_present(self, client):
        """Security headers are set on every response."""
        response = client.get("/")
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
        assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"

    def test_index_returns_200(self, client):
        """GET / returns 200 and renders the index template."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Effective Rate Calculator" in response.data


class TestLoanCalculation:
    """Tests for the /calculate endpoint and loan math."""

    def test_standard_loan_calculation(self, client):
        """A typical loan returns the result page with an effective rate."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "10000",
                "duration": "12",
                "annual_interest_rate": "5",
                "partner_commission_rate": "1",
            },
        )
        assert response.status_code == 200
        assert b"Effective Rate" in response.data
        # Result page contains a percentage value
        assert b"%" in response.data

    def test_large_loan_amount(self, client):
        """Large loan amounts compute without error."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "1000000",
                "duration": "360",
                "annual_interest_rate": "3.5",
                "partner_commission_rate": "0.5",
            },
        )
        assert response.status_code == 200
        assert b"Effective Rate" in response.data

    def test_zero_commission_returns_result(self, client):
        """Zero partner commission still returns a valid result."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "50000",
                "duration": "60",
                "annual_interest_rate": "4",
                "partner_commission_rate": "0",
            },
        )
        assert response.status_code == 200
        assert b"Effective Rate" in response.data

    def test_short_duration_loan(self, client):
        """Single-month loan computes correctly."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "1000",
                "duration": "1",
                "annual_interest_rate": "10",
                "partner_commission_rate": "0",
            },
        )
        assert response.status_code == 200
        assert b"Effective Rate" in response.data

    def test_high_interest_rate(self, client):
        """High interest rate computes without error."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "5000",
                "duration": "24",
                "annual_interest_rate": "20",
                "partner_commission_rate": "2",
            },
        )
        assert response.status_code == 200
        assert b"Effective Rate" in response.data


class TestInputValidation:
    """Tests for invalid input handling.

    The app re-renders the index form on validation errors (status 200).
    The error message is passed as a template variable but the current
    index.html template does not display it, so we verify the form is
    re-rendered (contains the form elements) and does NOT show the
    result page.
    """

    def _assert_form_rerendered(self, response):
        """Helper: response re-renders the input form, not the result."""
        assert response.status_code == 200
        # The form page has the <form> tag; the result page does not
        assert b"<form" in response.data
        # The result page text should NOT appear
        assert b"after deducting partner" not in response.data

    def test_negative_loan_amount_rejected(self, client):
        """Negative loan amount re-renders the form."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "-1000",
                "duration": "12",
                "annual_interest_rate": "5",
                "partner_commission_rate": "1",
            },
        )
        self._assert_form_rerendered(response)

    def test_zero_duration_rejected(self, client):
        """Zero duration re-renders the form."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "10000",
                "duration": "0",
                "annual_interest_rate": "5",
                "partner_commission_rate": "1",
            },
        )
        self._assert_form_rerendered(response)

    def test_negative_interest_rate_rejected(self, client):
        """Negative interest rate re-renders the form."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "10000",
                "duration": "12",
                "annual_interest_rate": "-5",
                "partner_commission_rate": "1",
            },
        )
        self._assert_form_rerendered(response)

    def test_negative_commission_rejected(self, client):
        """Negative commission rate re-renders the form."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "10000",
                "duration": "12",
                "annual_interest_rate": "5",
                "partner_commission_rate": "-1",
            },
        )
        self._assert_form_rerendered(response)

    def test_non_numeric_input_rejected(self, client):
        """Non-numeric input re-renders the form."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "abc",
                "duration": "12",
                "annual_interest_rate": "5",
                "partner_commission_rate": "1",
            },
        )
        self._assert_form_rerendered(response)

    def test_missing_field_rejected(self, client):
        """Missing form field re-renders the form."""
        response = client.post(
            "/calculate",
            data={
                "loan_amount": "10000",
                "duration": "12",
                # missing annual_interest_rate and partner_commission_rate
            },
        )
        self._assert_form_rerendered(response)
