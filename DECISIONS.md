# Design Decisions

## Multi-tenancy

- **Decision:** `X-Client-Id` header (fallback: query/body `client_id`).
- **Rationale:** Simple header-based isolation without JWT/OAuth for this assessment. Every queryset filters by resolved `Tenant`.

## Raw immutability

- **Decision:** `RawDataRecord` cannot be updated after insert.
- **Rationale:** Audit trail for regulatory review; corrections happen on normalized records via review workflow, not by rewriting source files.

## SAP column handling

- **Decision:** Case-insensitive alias map for plant, date, quantity, unit, material, spend columns.
- **Rationale:** Real SAP OData/flat exports use inconsistent headers (`PLANT_CODE`, `FuelUnit`, `Posting Date`).

## Procurement vs fuel (SAP)

- **Decision:** If `net_value`/`amount`/`spend` is present and fuel quantity is empty → Scope 3 procurement; else fuel → Scope 1.
- **Rationale:** Single export file often mixes fuel lines and PO spend.

## Utility billing date

- **Decision:** `activity_date` = midpoint between billing start and end.
- **Rationale:** Utility CSVs rarely provide a single consumption date; mid-period is a common reporting convention.

## Travel distance

- **Decision:** Flights use `AirportDistance` lookup; unknown pairs default to **800 km** with `MISSING_FIELD` flag.
- **Decision:** Hotels/ground use fixed estimates (50 km / 30 km / 100 km by type).
- **Rationale:** Concur exports often lack distance; airport codes are reliably present for flights.

## Quality flags

- **MISSING_FIELD:** Required plant, meter, airports, dates, or quantities absent.
- **INVALID_UNIT:** Unit string not in conversion table.
- **SUSPICIOUS_VALUE:** kWh > 1M, fuel > 50k L, distance > 20k km.

## Authentication

- **Decision:** No auth on API (`AllowAny`) for local demo.
- **Rationale:** Focus on data model; production would add token auth and tenant RBAC.

## CO2e calculation

- **Decision:** `emission_factor` and `co2e_kg` fields exist but are not populated.
- **Rationale:** Emission factors vary by region/fuel; out of scope for ingestion correctness demo.
