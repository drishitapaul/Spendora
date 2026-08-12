# Spendora QA Test Cases

## Authentication

| ID | Test Scenario | Expected Result | Type |
|---|---|---|---|
| TC01 | Login with valid credentials | User reaches dashboard | Functional |
| TC02 | Login with invalid credentials | Error message is displayed | Negative |
| TC03 | Submit empty login fields | Validation message is displayed | Negative |

## Transactions

| ID | Test Scenario | Expected Result | Type |
|---|---|---|---|
| TC04 | Add valid income | Income is saved successfully | Functional |
| TC05 | Add valid expense | Expense appears in transaction list | Functional |
| TC06 | Submit incomplete transaction | Validation prevents submission | Negative |
| TC07 | Delete an existing transaction | Transaction is removed | Functional |

## Dashboard

| ID | Test Scenario | Expected Result | Type |
|---|---|---|---|
| TC08 | Open dashboard | Dashboard loads correctly | Functional |
| TC09 | View transaction summary | Correct totals are displayed | Functional |
| TC10 | Refresh dashboard | Data remains consistent | Regression |

## UI & Navigation

| ID | Test Scenario | Expected Result | Type |
|---|---|---|---|
| TC11 | Navigate between sections | Correct section loads | UI |
| TC12 | Enter invalid input | Appropriate validation appears | Negative |
