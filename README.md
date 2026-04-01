# Spendora – Finance Tracker

## Overview
Spendora is a full-stack finance tracking application built using Flask (backend), React (frontend), and SQLite (relational database). It allows users to add transactions, view insights, and visualize expenses.

---

## Architecture
Frontend (React) → REST API (Flask) → SQLite Database

- React handles UI and state
- Flask exposes APIs for transactions and insights
- SQLite stores structured transaction data

---

## Key Technical Decisions
- Used Flask for simplicity and fast API development
- SQLite chosen for lightweight relational storage
- React used for component-based UI and state handling
- Recharts used for data visualization

---

## Validation & Safety
- Input validation ensures required fields (title, amount, type)
- Backend prevents invalid or incomplete data insertion
- Type conversion (amount → float) ensures consistency

---

## AI Usage
AI tools were used to:
- Accelerate development
- Assist in debugging and structuring code

All generated code was reviewed, tested, and modified where necessary.

---

## Limitations / Risks
- No authentication (single-user system)
- SQLite not suitable for large-scale production
- Basic validation only (can be extended)

---

## Future Improvements
- Add authentication and user accounts
- Add categories and filters
- Improve AI-based financial insights
- Add budget tracking

---

## Deployment
- Frontend: Vercel
- Backend: Render