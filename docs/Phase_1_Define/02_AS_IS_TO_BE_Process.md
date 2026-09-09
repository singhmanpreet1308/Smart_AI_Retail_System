# Smart AI Retail System

## AS-IS vs TO-BE Business Process

**Project:** Smart AI Retail System
**Phase:** Phase 1 — Define
**Document Status:** In Progress

---

# 1. AS-IS Business Process

## 1.1 Purpose

The AS-IS process describes the current state of retail data availability
and decision support before implementation of the Smart AI Retail System.

The objective is to identify where data is fragmented, where manual
reconciliation is required, and where opportunities exist for governed
analytics and decision-support automation.

---

## 1.2 Current Data Sources

The current analytical environment contains three primary operational
data sources.

| Data Source               | Primary Information                                                    | Current Structure                                  |
| ------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------- |
| Master_Sales_data.xlsx    | Sales, units sold, cost, selling price, profit, margin and stock level | Master sheet plus monthly snapshot sheets          |
| Stock_on_Hand_Report.xlsx | Product inventory across store locations                               | Wide Excel structure with individual store columns |
| MasterSOA.xlsx            | Sell Out Allowance (SOA) and applicable Starts/Ends window             | Product-level promotional allowance records        |

These sources contain related product information but are maintained
independently and are not yet integrated into a governed analytical
data model.

---

# 2. Current Sales Analysis Process

Sales information is available from `Master_Sales_data.xlsx`.

The dataset contains information including:

- Category
- Stock Code
- Description
- Level
- Sold Period
- Unit Cost
- Unit Price
- Cost Sales
- Sales Value
- Profit
- Profit %

The workbook contains a cumulative/master sheet together with monthly
snapshot sheets.

### Current Limitation

Sales information exists as an operational Excel source rather than as
a governed analytical fact table.

Before reliable cross-period or cross-source analysis can be performed,
the relationship between the master sheet and monthly snapshot sheets
must be established and duplicate records must be controlled.

---

# 3. Current Inventory Process

Stock-on-hand information is maintained separately in
`Stock_on_Hand_Report.xlsx`.

Inventory is represented across seven store locations:

- Gorey
- Dundrum
- Cavan
- Navan
- Blanch
- Sandyford
- Belfast

Each store currently appears as a separate column, with an additional
Total column.

### Current Limitation

The wide structure is suitable for reading an operational report but is
not suitable for governed store-level analytical relationships.

It prevents straightforward use of a standard structure such as:

Store → Product → Quantity

The inventory data therefore needs to be reshaped before store-level
analysis, joins and dashboards can be built.

---

# 4. Current SOA Process

Sell Out Allowance information is maintained separately in
`MasterSOA.xlsx`.

Each record contains:

- Model
- Description
- Starts
- Ends
- SOA

SOA represents an additional discount/support value applicable to the
product during the specified Starts-to-Ends date window.

### Current Limitation

SOA information is not yet integrated with product sales, unit cost,
selling price, inventory or competitor pricing within a governed
decision-support workflow.

Therefore, the available SOA information cannot yet directly drive a
controlled pricing recommendation process within the proposed system.

---

# 5. Current Product Identification Process

Related product information exists across the three datasets, but the
identifier naming is not consistent.

Sales data uses:

`Stock Code`

Stock-on-hand and SOA data use:

`Model`

### Current Limitation

Although these fields appear to represent equivalent or closely related
product identifiers, they require controlled reconciliation before they
can be treated as a canonical product key.

Without this control, cross-source joins could associate incorrect
products or fail to associate valid products.

---

# 6. Current Reporting and Analysis State

The available business information is distributed across separate Excel
workbooks.

There is currently no governed analytical layer within the scope of this
project that combines:

Sales
+
Profitability
+
Inventory
+
SOA

into a single reconciled source of truth.

Consequently, integrated analysis requires preparation and
reconciliation of information from multiple sources before business
decisions can be supported consistently.

---

# 7. Current Inventory Decision-Support State

Sales performance and store-level inventory have not yet been combined
into governed analytical rules for identifying conditions such as:

- High demand / low stock
- Low demand / high stock
- Balanced inventory
- Slow-moving inventory
- Reorder candidates

These decision rules will therefore need to be developed from the
governed data layer rather than being assumed from isolated stock
quantities.

---

# 8. Current Pricing Intelligence State

The available data contains internal product pricing/cost information
and SOA information, but the Smart AI Retail System does not yet have an
integrated competitor-pricing decision workflow.

The following capabilities are therefore not part of the current
project state:

- Automated competitor price collection
- Product-match confidence scoring
- Competitor price variance calculation
- Margin-floor protection
- Price recommendation logic
- Manager approval queue
- Automated ESL update
- Pricing audit trail

These capabilities form part of the proposed future-state Pricing
Intelligence layer.

---

# 9. Current Product Knowledge State

The current project datasets primarily contain operational product
information such as model, description, price, sales and stock.

They do not constitute a governed product-specification knowledge base
containing detailed manufacturer specifications, dimensions, features
and structured product comparisons.

A separate Product Knowledge Layer is therefore required in the TO-BE
system.

---

# 10. AS-IS Process Summary

The current analytical flow can be represented as:

Sales Excel
        ↓
Independent sales information

Stock-on-Hand Excel
        ↓
Independent store inventory information

SOA Excel
        ↓
Independent promotional allowance information

        ↓

Manual / separate interpretation and reconciliation

        ↓

Business analysis and decision-making

# 11. AS-IS Gap Analysis

| Area                   | AS-IS State                                | Identified Gap                                             |
| ---------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| Data Integration       | Sales, stock and SOA maintained separately | No governed integrated data layer                          |
| Product Identification | Stock Code and Model used across sources   | Canonical product key not yet established                  |
| Inventory Structure    | Stores represented as separate columns     | Not analysis-ready for store-level modelling               |
| Sales Data             | Master and monthly sheets coexist          | Consolidation/de-duplication rule required                 |
| Financial KPIs         | Financial measures exist in source         | Governed reconciliation required                           |
| Inventory Intelligence | Stock and sales available separately       | No governed reorder/slow-mover logic                       |
| Reporting              | Operational Excel sources                  | No single governed management dashboard                    |
| Pricing Intelligence   | Internal pricing/SOA data available        | No controlled competitor-price recommendation workflow     |
| Product Knowledge      | Basic operational descriptions available   | No governed specification knowledge layer                  |
| AI Decision Support    | Not implemented                            | No grounded natural-language analytical interface          |
| Forecasting            | Limited historical snapshots available     | Feasibility not yet established                            |
| Governance             | Raw operational sources                    | Data-quality, lineage and reconciliation controls required |

# 12. TO-BE Business Process

## 12.1 Purpose

The TO-BE process defines the future operating model of the Smart AI
Retail System.

The future state transforms fragmented operational data into a governed,
reconciled and reusable retail data foundation that supports management
reporting, inventory intelligence, pricing intelligence and grounded
AI-assisted decision support.

The system follows the principle:

Raw Data
    ↓
Validation & Transformation
    ↓
Governed Data Layer
    ↓
Analytics & Decision Intelligence
    ↓
Controlled Business Actions

# 13. Governed Data Ingestion

The system will initially consume three primary operational sources:

1. Master_Sales_data.xlsx
2. Stock_on_Hand_Report.xlsx
3. MasterSOA.xlsx

These files remain source systems but will no longer be used directly
by downstream dashboards, recommendation engines or AI applications.

The ETL process will:

- Load source data
- Validate expected schemas
- Check nulls and duplicates
- Standardize data types
- Normalize product identifiers
- Reshape store inventory
- Apply documented data-quality rules
- Reconcile financial measures
- Load validated records into the governed data layer

# 14. Canonical Product Master

A governed Product Master will provide the common product identity used
across the Smart AI Retail System.

The Product Master will reconcile identifiers such as:

Sales:
Stock Code

Inventory:
Model

SOA:
Model

into a canonical product identifier.

Conceptually:

Stock Code ──┐
             ├──> Canonical Product Key
Model ───────┘

The Product Master will also retain relevant descriptive attributes,
such as product description and category.

All downstream sales, inventory, SOA, pricing and product-knowledge
relationships should reference this governed product identity.

# 15. Governed Data Layer

Validated and transformed information will be stored in a governed
relational data layer.

The planned core tables are:

dim_product
    Governed product identity and descriptive attributes.

dim_store
    Store/location reference information.

fact_sales
    Product sales, units, cost, revenue and profitability information.

fact_stock
    Store-level product inventory quantities.

fact_soa
    Product Sell Out Allowance values and applicable Starts/Ends
    windows.

This layer becomes the analytical Single Source of Truth for the Smart
AI Retail System.

Downstream applications should consume governed tables or approved
views rather than independently reading or recalculating information
from raw Excel files.

# 16. Sales and Profitability Intelligence

The governed sales layer will support consistent calculation and
analysis of retail performance measures including:

- Revenue
- Units Sold
- Gross Profit
- Gross Margin %
- Sales Velocity
- Product Contribution
- Category Contribution
- Period-on-Period Performance

Analysis will also support product and category segmentation such as
Pareto analysis and identification of high- and low-performing products.

Financial measures will be reconciled against source information before
being exposed to downstream reporting.

# 17. Inventory Intelligence

Store-level inventory will be transformed from the current wide report
into an analytical structure:

Store | Product | Quantity

Inventory information will then be combined with sales performance and
product classifications.

This will support identification of:

- High-demand / low-stock products
- Low-demand / high-stock products
- Balanced inventory
- Slow-moving products
- Potential reorder requirements

The Inventory Intelligence layer will produce governed recommendation
outputs such as:

Reorder
Review
No Action

and slow-mover flags.

The recommendation logic will be maintained centrally rather than
being independently recreated in dashboards or applications.

# 18. Power BI Decision Support

Power BI will connect to the governed data layer rather than directly
to raw operational Excel files.

The reporting layer will provide three principal management views:

### Executive Dashboard

- Revenue
- Gross Profit
- Margin %
- Performance trends
- Category contribution

### Sales Dashboard

- Product ranking
- Category performance
- Period-on-period changes
- Pareto analysis

### Inventory Dashboard

- Store-level stock
- ABC inventory classification
- Slow movers
- Reorder indicators

Power BI measures will be reconciled against the governed SQL/Python
reference calculations before publication.

# 19. Conditional Forecasting Process

Forecasting will only enter the operational TO-BE process if the
Phase 3 data-sufficiency assessment demonstrates that the available
historical information supports meaningful forecasting.

If approved, the process will begin with an appropriate baseline such
as a naive or moving-average forecast.

More complex forecasting approaches will only be considered where they
can be evaluated reliably against the baseline using time-based
out-of-sample validation.

If sufficient historical signal is not available, forecasting will be
formally excluded rather than introducing unreliable predictions into
business decisions.

# 20. Pricing Intelligence Process

SOA changes will provide an input into a controlled pricing-intelligence
workflow.

The intended future process is:

SOA Change
    ↓
Product Identified
    ↓
Competitor Price Lookup
    ↓
Product Match Confidence
    ↓
Price Comparison
    ↓
Margin-Floor Validation
    ↓
Recommendation
    ↓
Approval Gate
    ↓
Approved ESL Update
    ↓
Audit Log

## 20.1 Pricing Controls

Pricing recommendations will not be based solely on the lowest observed
competitor price.

The process will consider:

- Exact product/model matching
- Match confidence
- Current selling price
- Unit cost
- SOA
- Competitor price
- Price variance
- Margin floor
- Configured business rules

High-confidence, within-policy recommendations may become eligible for
automated approval.

Medium/low-confidence matches and recommendations outside configured
pricing boundaries will require management review.

Any recommendation that breaches the configured margin floor will be
blocked.

Every pricing decision will be recorded in an audit log.

# 21. Product Knowledge Process

Store staff will be able to retrieve verified product information using
a model number or, where supported, barcode/QR lookup.

The future process will be:

Model / Barcode Input
        ↓
Input Normalization
        ↓
Product Master Match
        ↓
Match Confidence
        ↓
Manufacturer Source Retrieval
        ↓
Specification Extraction
        ↓
Validation
        ↓
Governed Product Knowledge
        ↓
Staff-Facing Product Spec Card

The Product Knowledge Layer may provide:

- Product model
- Category
- Key specifications
- Dimensions
- Capacity
- Features
- Included accessories
- Warranty information
- Comparative pros/cons
- Source reference
- Data completeness
- Match confidence

Product information must be grounded in verified sources.

Where a product cannot be confidently matched, the system should return
a clear not-confidently-matched result rather than guessing product
specifications.

# 22. AI Retail Assistant

The AI Retail Assistant will provide a natural-language interface over
approved governed retail information.

The assistant may support questions relating to:

- Sales performance
- Profitability
- Product performance
- Category performance
- Inventory position
- Reorder recommendations
- Slow-moving products
- Approved pricing intelligence
- Product specifications

The assistant will use read-only governed data sources and approved
views.

Responses should expose relevant source and refresh-date information so
that users can assess the currency of the underlying data.

The assistant must not invent unavailable business values or product
specifications.
