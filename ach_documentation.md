# ACHQ Provider API Documentation

ACHQ provides a simple API for submitting and tracking ACH payment transactions.

## Authentication
- All requests must include the API key in the header: X-ACHQ-API-Key: your_api_key
- All requests must be sent to https://api.achq.com/v1/

## Endpoints

### 1. Create Payment

POST /payments/create

Request Body:
{
    "amount": number (required, > 0),
    "account_type": string (required, "checking" or "savings"),
    "transaction_type": string (required, "debit" or "credit"),
    "bank_account": {
        "routing_number": string (required, 9 digits),
        "account_number": string (required, 4-17 digits),
        "account_holder_name": string (required)
    },
    "memo": string (optional, max 10 chars),
    "client_reference_id": string (optional, your internal reference)
}

Response:
{
    "success": boolean,
    "payment_id": string (ACHQ's unique payment identifier),
    "status": string ("pending"),
    "estimated_settlement_date": string (ISO date),
    "trace_number": string (ACH trace number, only available after processing)
}

### 2. Get Payment Status

GET /payments/{payment_id}

Response:
{
    "payment_id": string,
    "status": string (one of: "pending", "processing", "completed", "failed", "returned"),
    "status_code": string (optional, only for failed/returned payments),
    "trace_number": string (only available after processing starts),
    "settlement_date": string (ISO date, only available after completion),
    "client_reference_id": string (your internal reference if provided)
}

### 3. List Payments

GET /payments?start_date={date}&end_date={date}&status={status}

Parameters:
- start_date: ISO date (optional)
- end_date: ISO date (optional)
- status: string (optional, filter by status)

Response:
{
    "payments": [
        {
            "payment_id": string,
            "status": string,
            "status_code": string (optional),
            "amount": number,
            "transaction_type": string,
            "trace_number": string (if available),
            "settlement_date": string (if completed),
            "client_reference_id": string (if provided)
        },
        ...
    ],
    "page": number,
    "total_pages": number
}

## Status Codes

When a payment fails or is returned, the status_code field will contain one of:

- R01: Insufficient Funds
- R02: Account Closed
- R03: No Account/Unable to Locate Account
- R04: Invalid Account Number
- R05: Unauthorized Debit
- R07: Authorization Revoked by Customer
- R08: Payment Stopped
- R09: Uncollected Funds
- R10: Customer Advises Not Authorized
- R20: Non-Transaction Account

## Webhooks

ACHQ can send webhook notifications when payment status changes.
Configure your webhook URL in the ACHQ dashboard.

Webhook payload:
{
    "event_type": "payment.status_update",
    "payment_id": string,
    "status": string,
    "status_code": string (optional),
    "trace_number": string,
    "client_reference_id": string (if provided),
    "timestamp": string (ISO datetime)
}
