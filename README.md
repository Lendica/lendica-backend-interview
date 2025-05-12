# lendica-backend
## Instructions for Candidate

### Background

Lendica is a financial platform that offers various lending products to businesses. One critical function is processing scheduled loan repayments through an external ACH (Automated Clearing House) payment provider.

You'll be working on two key functions:

1. A function to submit payments to the ACH provider
2. A function to reconcile payment statuses from the provider back to our internal system

The main challenge is maintaining accurate records across two systems, properly tracking payment statuses, and handling the various edge cases that can occur with financial transactions.

### Your Task

You need to implement two functions:

1. `submit_payment_to_ach_provider`: Sends a payment request to the external provider based on our internal payment schedule
2. `reconcile_ach_payment_statuses`: Fetches current statuses from the provider and updates our internal records

You'll work with a simplified version of our database models and a mock ACH provider client that simulates the behavior of the external API.

### Provided Resources

1. Database models (Company, Loan, PaymentSchedule, Payment)
2. Mock ACH provider documentation
3. Mock ACH provider client with simulated responses
4. Function signatures to implement


## Considerations

Consider the following as you implement the functions:

1. **Error Handling**: Financial transactions require robust error handling. How will you handle API failures, validation errors, or inconsistent data?
2. **Idempotence**: How will you ensure that payments aren't submitted multiple times?
3. **Status Mapping**: How will you map between the ACH provider's status values and your internal status values?
4. **Reconciliation Logic**: What's the most efficient way to identify and update payments that need status updates?
5. **Edge Cases**:
    - What if a payment amount is zero or negative?
    - How do you handle payments for canceled loans?
    - What if the ACH provider returns an unexpected status?
    - How should you handle returned payments (e.g., insufficient funds)?