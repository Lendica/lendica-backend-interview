import requests
import json
import datetime
import random
import time
from typing import Dict, Any, List, Optional

class ACHQProvider:
    """
    Mock client for the ACHQ payment provider API.
    In a real implementation, this would make HTTP calls to the actual API.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.achq.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-ACHQ-API-Key": api_key,
            "Content-Type": "application/json"
        }

# For mock implementation, we'll store payment data locally
        self.mock_payments = {}

    def create_payment(self,
                      amount: float,
                      account_type: str,
                      transaction_type: str,
                      routing_number: str,
                      account_number: str,
                      account_holder_name: str,
                      memo: Optional[str] = None,
                      client_reference_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new payment through the ACHQ API.

        In a real implementation, this would send an HTTP POST request.
        For this exercise, we mock the response.
        """
# Input validation (simplified)
        if not amount or amount <= 0:
            return {"success": False, "error": "Invalid amount"}

        if account_type not in ["checking", "savings"]:
            return {"success": False, "error": "Invalid account type"}

        if transaction_type not in ["debit", "credit"]:
            return {"success": False, "error": "Invalid transaction type"}

        if not routing_number or len(routing_number) != 9:
            return {"success": False, "error": "Invalid routing number"}

        if not account_number or len(account_number) < 4 or len(account_number) > 17:
            return {"success": False, "error": "Invalid account number"}

        if not account_holder_name:
            return {"success": False, "error": "Account holder name required"}

# In a real implementation, construct and send the API request# response = requests.post(f"{self.base_url}/payments/create",#                         headers=self.headers,#                         json=payload)# return response.json()

# For mock implementation, generate a response
        payment_id = f"ACHQ-{random.randint(1000000, 9999999)}"
        estimated_settlement_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

# Store payment data for later status checks
        self.mock_payments[payment_id] = {
            "payment_id": payment_id,
            "amount": amount,
            "status": "pending",
            "transaction_type": transaction_type,
            "estimated_settlement_date": estimated_settlement_date,
            "client_reference_id": client_reference_id,
            "created_at": datetime.datetime.now().isoformat()
        }

        return {
            "success": True,
            "payment_id": payment_id,
            "status": "pending",
            "estimated_settlement_date": estimated_settlement_date,
            "trace_number": None# Not available until processing
        }

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get the current status of a payment.

        In a real implementation, this would send an HTTP GET request.
        For this exercise, we mock the response.
        """
# In a real implementation, send the API request# response = requests.get(f"{self.base_url}/payments/{payment_id}", headers=self.headers)# return response.json()

# For mock implementation, look up stored payment
        if payment_id not in self.mock_payments:
            return {"success": False, "error": "Payment not found"}

        payment = self.mock_payments[payment_id]

# Mock status progression based on time elapsed
        created_time = datetime.datetime.fromisoformat(payment["created_at"])
        time_elapsed = (datetime.datetime.now() - created_time).total_seconds()

# Simulate status progression
        if time_elapsed < 60:# Within a minute of creation
            status = "pending"
            trace_number = None
        elif time_elapsed < 120:# 1-2 minutes
            status = "processing"
            trace_number = f"TRACE{random.randint(10000000, 99999999)}"
            payment["trace_number"] = trace_number
        else:# After 2 minutes# 90% chance of success, 10% chance of failure
            if random.random() < 0.9:
                status = "completed"
                settlement_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                payment["settlement_date"] = settlement_date
            else:
                status = "failed"
                status_code = random.choice(["R01", "R03", "R04"])
                payment["status_code"] = status_code

        payment["status"] = status

        response = {
            "payment_id": payment_id,
            "status": status,
            "client_reference_id": payment.get("client_reference_id")
        }

        if "trace_number" in payment:
            response["trace_number"] = payment["trace_number"]

        if "settlement_date" in payment:
            response["settlement_date"] = payment["settlement_date"]

        if "status_code" in payment:
            response["status_code"] = payment["status_code"]

        return response

    def list_payments(self, start_date=None, end_date=None, status=None) -> Dict[str, Any]:
        """
        List payments with optional filtering.

        In a real implementation, this would send an HTTP GET request.
        For this exercise, we mock the response.
        """
# In a real implementation, construct query params and send the API request# response = requests.get(f"{self.base_url}/payments", headers=self.headers, params=params)# return response.json()

# For mock implementation, filter stored payments
        filtered_payments = []

        for payment_id, payment in self.mock_payments.items():
            include = True

            if start_date:
                payment_date = datetime.datetime.fromisoformat(payment["created_at"]).date()
                if payment_date < datetime.datetime.strptime(start_date, "%Y-%m-%d").date():
                    include = False

            if end_date:
                payment_date = datetime.datetime.fromisoformat(payment["created_at"]).date()
                if payment_date > datetime.datetime.strptime(end_date, "%Y-%m-%d").date():
                    include = False

            if status and payment["status"] != status:
                include = False

            if include:
                payment_copy = payment.copy()
                payment_copy.pop("created_at", None)# Remove internal field
                filtered_payments.append(payment_copy)

        return {
            "payments": filtered_payments,
            "page": 1,
            "total_pages": 1
        }
