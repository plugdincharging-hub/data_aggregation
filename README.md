# Machine Revenue Dashboard

A Streamlit dashboard that retrieves Stripe Payment Intent data for the past 30 days and displays gross sales, Stripe processing fees, net revenue, and transaction counts by machine.

## Features

- Retrieves Stripe Payment Intents from the last 30 days
- Handles Stripe cursor pagination
- Retrieves Stripe processing fees per successful payment
- Groups revenue by machine `station_id`
- Displays gross sales, Stripe fees, net revenue, and transaction count
- Provides a downloadable CSV report

## Requirements

- Python 3.10 or newer
- A Stripe restricted API key with read access to:
  - Payment Intents
  - Charges
  - Balance Transactions

## Installation

Clone the repository, then move into this project folder:

```powershell
cd data_aggregation
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Configure Stripe

Set your Stripe API key as an environment variable for the current PowerShell session:

```powershell
$env:STRIPE_API_KEY = "your_restricted_stripe_key"
```

Do not put Stripe keys directly in source code or commit them to Git.

## Run the dashboard

```powershell
python -m streamlit run dashboard.py
```

Streamlit will open the dashboard locally, normally at:

```text
http://localhost:8501
```

## Revenue calculation

All Stripe amounts are returned in pence.

```text
Net revenue = amount received - Stripe processing fee
```

The dashboard converts values to GBP for display.

## Project structure

```text
data_aggregation/
├── api_queries.py       # Stripe API requests and pagination
├── transformation.py    # Revenue and fee calculations
├── dashboard.py         # Streamlit dashboard
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Important notes

- This dashboard currently reports the previous 30 days of Stripe activity.
- Stripe balance totals can differ from dashboard totals because of pending funds, refunds, disputes, payouts, adjustments, or timing differences.
- This project is intended as a reporting dashboard and is not accounting software.