from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="Personal Expense Tracker | Full CRUD",
    description="Assignment 17: HTML, JavaScript, and FastAPI together with full CRUD",
    version="1.0.0",
)

html_file = Path(__file__).with_name("index.html")


class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    amount: float = Field(..., gt=0, le=10000000)
    category: str = Field(..., min_length=2, max_length=50)
    date: str = Field(..., min_length=8, max_length=12)
    payment_method: str = Field(..., min_length=2, max_length=50)
    notes: Optional[str] = Field("", max_length=250)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=120)
    amount: Optional[float] = Field(None, gt=0, le=10000000)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    date: Optional[str] = Field(None, min_length=8, max_length=12)
    payment_method: Optional[str] = Field(None, min_length=2, max_length=50)
    notes: Optional[str] = Field(None, max_length=250)


class Expense(ExpenseBase):
    id: int


# Initial Seed Expenses
EXPENSES_DB: List[Expense] = [
    Expense(id=1, title="Monthly Groceries & Vegetables", amount=3450.0, category="Food & Dining", date="2026-11-01", payment_method="UPI", notes="Supermarket monthly essentials"),
    Expense(id=2, title="Electricity & Internet Bill", amount=1850.0, category="Bills & Utilities", date="2026-11-02", payment_method="Net Banking", notes="Broadband + Power"),
    Expense(id=3, title="Python & Cloud Architecture Course", amount=2499.0, category="Education", date="2026-11-03", payment_method="Credit Card", notes="Skill development certification"),
    Expense(id=4, title="Metro Pass & Commute", amount=900.0, category="Transportation", date="2026-11-04", payment_method="UPI", notes="Monthly metro card recharge"),
    Expense(id=5, title="Weekend Dinner with Friends", amount=1280.0, category="Food & Dining", date="2026-11-05", payment_method="UPI", notes="Restaurant dinner"),
    Expense(id=6, title="Movie & Popcorn", amount=650.0, category="Entertainment", date="2026-11-06", payment_method="Debit Card", notes="Weekend cinema"),
]
next_expense_id = 7


@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse(html_file, media_type="text/html")


@app.get("/api/expenses", response_model=List[Expense])
def get_expenses(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("date", regex="^(date|amount)$"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
):
    results = EXPENSES_DB

    if category and category != "All":
        results = [e for e in results if e.category.lower() == category.lower()]

    if search:
        q = search.lower()
        results = [
            e for e in results
            if q in e.title.lower() or q in (e.notes or "").lower() or q in e.payment_method.lower()
        ]

    reverse_sort = order == "desc"
    results = sorted(results, key=lambda x: getattr(x, sort_by or "date"), reverse=reverse_sort)
    return results


@app.get("/api/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    for e in EXPENSES_DB:
        if e.id == expense_id:
            return e
    raise HTTPException(status_code=404, detail="Expense record not found")


@app.post("/api/expenses", response_model=Expense, status_code=201)
def add_expense(payload: ExpenseCreate):
    global next_expense_id
    new_expense = Expense(
        id=next_expense_id,
        title=payload.title.strip(),
        amount=round(payload.amount, 2),
        category=payload.category.strip(),
        date=payload.date.strip(),
        payment_method=payload.payment_method.strip(),
        notes=(payload.notes or "").strip(),
    )
    EXPENSES_DB.append(new_expense)
    next_expense_id += 1
    return new_expense


@app.put("/api/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, payload: ExpenseUpdate):
    for i, e in enumerate(EXPENSES_DB):
        if e.id == expense_id:
            data = e.model_dump()
            if payload.title is not None:
                data["title"] = payload.title.strip()
            if payload.amount is not None:
                data["amount"] = round(payload.amount, 2)
            if payload.category is not None:
                data["category"] = payload.category.strip()
            if payload.date is not None:
                data["date"] = payload.date.strip()
            if payload.payment_method is not None:
                data["payment_method"] = payload.payment_method.strip()
            if payload.notes is not None:
                data["notes"] = payload.notes.strip()

            updated = Expense(**data)
            EXPENSES_DB[i] = updated
            return updated

    raise HTTPException(status_code=404, detail="Expense record not found")


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for i, e in enumerate(EXPENSES_DB):
        if e.id == expense_id:
            deleted = EXPENSES_DB.pop(i)
            return {"message": f"Expense '{deleted.title}' deleted successfully", "id": expense_id}
    raise HTTPException(status_code=404, detail="Expense record not found")


@app.get("/api/summary")
def get_summary():
    if not EXPENSES_DB:
        return {
            "total_spent": 0.0,
            "total_transactions": 0,
            "highest_expense": 0.0,
            "average_expense": 0.0,
            "category_breakdown": [],
            "payment_methods": [],
        }

    total_spent = sum(e.amount for e in EXPENSES_DB)
    total_tx = len(EXPENSES_DB)
    max_expense = max(e.amount for e in EXPENSES_DB)
    avg_expense = total_spent / total_tx

    cat_map = {}
    pm_map = {}
    for e in EXPENSES_DB:
        cat_map[e.category] = cat_map.get(e.category, 0.0) + e.amount
        pm_map[e.payment_method] = pm_map.get(e.payment_method, 0.0) + e.amount

    category_breakdown = [
        {
            "category": cat,
            "total": round(amt, 2),
            "percentage": round((amt / total_spent) * 100, 1) if total_spent > 0 else 0,
        }
        for cat, amt in sorted(cat_map.items(), key=lambda x: x[1], reverse=True)
    ]

    payment_methods = [
        {"method": m, "total": round(amt, 2)}
        for m, amt in sorted(pm_map.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "total_spent": round(total_spent, 2),
        "total_transactions": total_tx,
        "highest_expense": round(max_expense, 2),
        "average_expense": round(avg_expense, 2),
        "category_breakdown": category_breakdown,
        "payment_methods": payment_methods,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
