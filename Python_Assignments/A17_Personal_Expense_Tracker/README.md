# A17 - Personal Expense Tracker

A full-stack Personal Expense Tracker application bringing HTML, CSS, JavaScript, and FastAPI together with full CRUD operations, category analytics, and spending summaries.

## Features
- **Add Expense**: Record expenses with Title/Merchant, Amount (₹), Category, Date, Payment Method (UPI, Cards, Cash, Net Banking), and optional Notes.
- **View & Filter Expenses**: Search by merchant/title or notes, filter by category, and review clear timestamps.
- **Update Expense**: Edit logged expenses using a pre-filled modal.
- **Delete Expense**: Delete expense items with confirmation.
- **Financial Analytics & Summary**:
  - Total Spent (₹)
  - Total Transactions count
  - Class-leading Category spending breakdown with percentage progress bars
  - Highest single expense & average spend per transaction
- **FastAPI REST API**: Clean endpoints under `/api/expenses` and `/api/summary`.

## Run
Install requirements and launch the server:

```bash
pip install -r requirements.txt
python main.py
```

Then visit:
`http://127.0.0.1:8000`
