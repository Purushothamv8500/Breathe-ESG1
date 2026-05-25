# Source Data Format Assumptions

## 1. SAP (fuel + procurement)

**Assumed format:** Flat CSV export from SAP S/4HANA or ECC (transaction list), not live OData.

Typical quirks we modeled:

| Quirk | Example in samples |
|-------|-------------------|
| Inconsistent column names | `Plant` vs `PLANT_CODE`, `FuelUnit` vs `fuel_unit` |
| Mixed date formats | `01/15/2024`, `2024-02-20`, `15-Mar-2024` |
| Plant codes needing lookup | `P001`, `PLNT-S2` → tenant `PlantCodeMapping` |
| Mixed units | liters, gallons, kg |
| Missing fuel quantity | procurement rows with `net_value` only |
| Outlier quantities | 999999 liters row |

**Columns expected (any alias):**

- Plant: `Plant`, `PLANT_CODE`, `plnt`, `werk`
- Date: `Posting Date`, `posting_date`, `budat`
- Quantity: `fuel_qty`, `quantity`, `menge`
- Unit: `FuelUnit`, `unit`, `uom`
- Material: `Material`, `matnr`
- Spend: `net_value`, `amount`, `spend`

## 2. Utility electricity

**Assumed format:** CSV download from utility customer portal (e.g. Duke, PG&E style).

| Quirk | Handling |
|-------|----------|
| Billing periods vs single date | Midpoint of start/end |
| kWh vs MWh | Normalize to kWh |
| Missing usage | `MISSING_FIELD` flag |
| Tariff column | Stored in description/payload |
| Missing meter on row | Flagged |

**Columns:**

- `Meter_ID`, `Billing_Start`, `Billing_End`, `Usage`, `Usage_UOM`, `Tariff`

## 3. Corporate travel (Concur / Navan style)

**Assumed format:** Expense export CSV with trip segments.

| Quirk | Handling |
|-------|----------|
| Airport codes, no distance | `AirportDistance` lookup |
| Missing destination | `MISSING_FIELD` |
| Hotel/ground without airports | Fixed km estimates by type |
| Categories for Scope 3 | All travel → SCOPE_3 |

**Columns:**

- `Employee`, `Type`, `From`, `To`, `Start_Date`, `Amount`, `Currency`

Amount/currency are retained in raw payload but not used for CO2e in v1.

## Sample files

Located in `samples/`:

- `sap_fuel_procurement.csv` — 7 rows including outliers and procurement
- `utility_electricity.csv` — 5 rows including MWh and missing usage
- `travel_expenses.csv` — 6 rows including incomplete flight
