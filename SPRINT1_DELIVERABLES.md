# Sprint 1 Deliverables

## Files Delivered

- `api_documentation.yaml` — Swagger-compatible YAML for the Sprint 1 endpoints verified in testing.
- `test_sprint1_api.py` — Pytest suite covering core auth, commerce, and admin flows.
- `conftest.py` — Root-level pytest bootstrap for the backend app.
- `USER_FEEDBACK_AND_NEXT_SPRINT_PLAN.md` — User feedback summary and next-sprint implementation plan.

## Scope Covered

The current sprint package validates these implemented APIs:

- `GET /health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/commerce/products`
- `POST /api/commerce/cart`
- `POST /api/commerce/orders`
- `GET /api/admin/stats`

## Test Cases

The table below is filled using the observed results from the pytest run in this repository.

| Test Case | Input | Expected Output | Actual Output |
|---|---|---|---|
| Health check | `GET /health` | `200` with `{"status": "ok"}` | `200` with `{"status": "ok"}` |
| Buyer registration | Buyer payload with `email`, `password`, `role`, `firstName`, `lastName` | `201`, token returned, role `buyer` | `201`, token returned, role `buyer` |
| Legacy auth doc shape | Artist payload using old fields `full_name` and `brand_name` | Rejected because live API expects `firstName`, `lastName`, `brandName` | `400` with `{"error": "Missing required fields"}` |
| Product creation | Approved artist token plus product payload | `201`, created product returned | `201`, product returned with artist name and price |
| Add to cart | Buyer token plus `product_id` and `quantity=2` | `201`, cart item stored | `201`, cart item returned with quantity `2` |
| Place order | Buyer token plus shipping and payment JSON | `201`, one order, one confirmed tracking event, cart cleared | `201`, order created, tracking starts with `confirmed`, cart cleared |
| Admin stats | Admin token | `200`, artist and buyer counts shown | `200`, `registeredArtists=1`, `registeredBuyers=1`, `pendingVerifications=0` |

## Mismatch Found During Testing

One useful discrepancy showed up during Sprint 1 testing:

- The earlier API documentation shape for registration did not match the implemented Flask code.
- The live backend expects `firstName`, `lastName`, and `brandName`.
- A payload using `full_name` and `brand_name` fails with `400 Missing required fields`.
- `api_documentation.yaml` has been updated to match the real implementation for the documented endpoints.

## How To Run The Tests

From the repository root:

```bash
.venv/bin/python -m pytest test_sprint1_api.py
```

The tests use an in-memory SQLite database, so they do not require the team PostgreSQL instance.
