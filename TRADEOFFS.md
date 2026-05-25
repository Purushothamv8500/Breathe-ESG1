# Tradeoffs — What We Didn't Build

## Async / queue-based ingestion

- **Skipped:** Celery, S3 staging, batch jobs.
- **Why:** Single Django app meets requirements; synchronous ingest is sufficient for analyst-scale CSV uploads.

## Emission factor library

- **Skipped:** DEFRA/EPA factor database, regional grids, GWP versions.
- **Why:** Evaluation focuses on normalization and review workflow, not final CO2e reporting.

## Normalized record versioning

- **Skipped:** History table when analysts edit normalized values.
- **Why:** `edited_flag` field reserved; approve/reject is the primary workflow for v1.

## Full SAP OData integration

- **Skipped:** Live OData client, IDoc parsing, BW extracts.
- **Why:** Assumed flat CSV export; documented in SOURCES.md.

## Role-based access control

- **Skipped:** Analyst vs admin roles, per-tenant user accounts.
- **Why:** `reviewed_by` is a free-text field for demo.

## Bulk approve/reject

- **Skipped:** Multi-record actions, export to GHG Protocol workbooks.
- **Why:** UI focuses on record-by-record audit quality.

## Data validation UI for ingest

- **Skipped:** Upload UI in frontend; ingest via API/curl/seed only.
- **Why:** Analyst dashboard is review-centric per spec.

## PostgreSQL / production hardening

- **Skipped:** Postgres, HTTPS, secrets management, rate limits.
- **Why:** SQLite + DEBUG for local evaluation; easy to swap DB in settings.

## Duplicate detection

- **Skipped:** Hash-based dedup across uploads.
- **Why:** Each ingest is a new immutable raw batch; dedup is an enterprise add-on.
