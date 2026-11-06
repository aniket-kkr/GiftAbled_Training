# A16 - Fest Web Page with CRUD

A festive full CRUD event portal for campus fest activities with live attendee registration, category filtering, capacity counters, and a FastAPI backend.

## Features
- **Add Fest Event**: Create events with Title, Category (Technical, Cultural, Gaming, Workshop, Sports), Date, Time, Venue, Coordinator, and Capacity.
- **View Events**: Search events, filter by category, inspect date/time, venue, and registration status.
- **Update Event**: Modify event details with pre-populated form values.
- **Delete Event**: Cancel and delete events.
- **Attendee Registration Engine**:
  - Click "Register" to increment participant count.
  - Automatically flags events as full when max capacity is reached.
- **Event Metrics**: Real-time total events, registrations, overall campus venue capacity, and category count.

## Run
Install requirements and launch the server:

```bash
pip install -r requirements.txt
python main.py
```

Then open your browser at:
`http://127.0.0.1:8000`
