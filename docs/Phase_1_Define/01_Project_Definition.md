# Smart AI Retail System

## Phase 1 — Project Definition

**Project:** Smart AI Retail System
**Phase:** Phase 1 — Define
**Methodology:** Lean Six Sigma (DMAIC) + Agile + SDLC + Data/AI Lifecycle
**Status:** In Progress

---

# 1. Business Problem Statement

## 1.1 Current Business Situation

The retail business generates operational data across multiple sources, including sales data, stock-on-hand data and SOA (Sell Out Allowance) data.

Sales data contains product and category performance information, including units sold, sales value, cost, profit and margin.

Stock-on-hand data contains inventory quantities distributed across multiple store locations.

SOA data contains Sell Out Allowance values applicable to products during defined Starts and Ends date windows.

These datasets currently exist as separate operational files with different structures and product identifiers. Sales data uses Stock Code, while inventory and SOA data use Model, requiring controlled product reconciliation before integrated analysis can be performed.

The current data structure therefore does not provide a single governed source from which sales, inventory, profitability and promotional allowance information can be analysed together.

---

## 1.2 Core Business Problem

Retail sales, inventory, product profitability and promotional allowance information are fragmented across separate operational data sources, limiting the ability of management and staff to obtain timely, consistent and actionable insights for sales, inventory, pricing and product decisions.

The absence of a governed integrated data layer means that important decisions can require manual data preparation, reconciliation and interpretation rather than being supported through a consistent decision-support system.

---

## 1.3 Business Impact

The current situation creates challenges across several areas:

### Inventory

There is limited integrated visibility between product demand and stock held across individual stores.

### Sales and Profitability

Product and category revenue, gross profit, margin and sales velocity need to be brought together consistently for performance analysis.

### Pricing

SOA information and product economics are not yet integrated into a controlled pricing-intelligence workflow.

### Reporting

Separate source files increase manual preparation and reconciliation requirements.

### Decision-Making

Management does not yet have a single governed analytical layer from which dashboards, inventory recommendations and AI-assisted queries can operate.

---

## 1.4 Desired Business Outcome

Develop a governed, data-driven retail decision-support system that integrates sales, inventory and SOA information into a trusted
analytical foundation and uses that foundation to improve visibility, inventory decisions, pricing decisions, reporting and staff access to retail intelligence.

---

## 1.5 Formal Problem Statement

The current retail reporting and decision-making process relies on fragmented sales, stock and promotional allowance data maintained across separate operational files.

Differences in data structure and product identifiers make integrated analysis and reconciliation difficult, while management lacks a
governed single source of truth for evaluating sales performance, profitability, inventory position and pricing opportunities.

The Smart AI Retail System will address this problem by integrating and governing these data sources and progressively delivering analytics, dashboards, inventory intelligence, pricing intelligence and grounded AI-assisted decision support.

---

# 2. Project Objectives

## 2.1 Primary Objective

To develop a governed, data-driven retail decision-support system thatintegrates sales, inventory and Sell Out Allowance (SOA) information into a trusted analytical foundation and supports better retail decision-making across sales performance, profitability, inventory, pricing and product knowledge.

---

## 2.2 Business Objectives

### Objective 1 — Establish a Governed Single Source of Truth

Integrate sales, stock-on-hand and SOA data into a governed data layer with standardized product identifiers, documented transformation rules and reconciled business measures.

This foundation will ensure that downstream dashboards, analytical outputs, recommendation logic and AI-assisted queries use consistent and traceable data.

### Objective 2 — Improve Sales and Profitability Visibility

Provide consistent visibility into retail performance using measures such as:

- Revenue
- Units sold
- Gross profit
- Gross margin %
- Sales velocity
- Product performance
- Category contribution
- Period-on-period performance

This will support identification of high-performing and underperforming products and categories.

### Objective 3 — Improve Inventory Decision Support

Combine product sales performance with store-level stock information to identify inventory conditions such as:

- High-demand / low-stock products
- Low-demand / high-stock products
- Balanced stock positions
- Slow-moving products
- Potential reorder requirements

The system should support purchasing and operations decisions rather than relying only on isolated stock quantities.

### Objective 4 — Deliver Management Decision Dashboards

Provide management with interactive reporting based on the governed data layer rather than directly on raw operational Excel files.

The reporting layer should provide executive, sales and inventory views with reconciled KPIs and drill-down capability across relevant products, categories, periods and stores.

### Objective 5 — Support Controlled Pricing Intelligence

Use product economics, SOA information and reliable competitor pricing information to support price recommendations.

Pricing recommendations must operate within defined business controls,
including:

- Product-match confidence
- Margin-floor protection
- Pricing variance rules
- Human approval for uncertain or out-of-band decisions
- Complete auditability of proposed and approved changes

Pricing automation must not silently push unverified or commercially unsafe price changes.

### Objective 6 — Provide Grounded AI-Assisted Retail Intelligence

Develop an AI Retail Assistant that allows approved users to query governed retail information using natural language.

Responses should be grounded in approved data sources and expose source and refresh information rather than generating unsupported business facts.

### Objective 7 — Improve Product Knowledge Accessibility

Provide store staff with a Product Knowledge Layer that enables product lookup using model numbers and, where supported, barcode or QR-based identification.

The system should provide verified product specifications, dimensions, features and grounded product comparisons while clearly identifying match confidence and data completeness.

### Objective 8 — Maintain Data Quality, Traceability and Control

Establish controls for:

- Data-quality validation
- Product-key consistency
- Financial reconciliation
- Refresh monitoring
- Recommendation traceability
- Pricing audit logs
- Source and refresh metadata
- Version-controlled analytical logic

This will allow the system's outputs to remain reproducible, explainable and maintainable.

---

## 2.3 Conditional Objective — Forecasting

Demand forecasting is a conditional project objective.

Forecasting will only proceed if the Phase 3 data-sufficiency assessment shows that the available historical data contains enough independent time periods and signal to support meaningful out-of-sample forecasting.

If the available history is insufficient, the forecasting phase will be formally descoped or restricted to an appropriate baseline rather than deploying an unreliable forecasting model.

---

## 2.4 Objective Success Principle

The success of the Smart AI Retail System will not be measured simply by whether individual technical components are built.

The project will be considered successful when its outputs are:

- Based on governed and reconciled data
- Relevant to defined business decisions
- Measurable against agreed acceptance criteria
- Traceable to their underlying data sources
- Protected by appropriate business controls
- Usable by the intended stakeholder groups

---

# 3. Stakeholders

The Smart AI Retail System supports multiple business functions involved in retail performance, inventory, pricing, reporting and customer-facing product decisions.

## 3.1 Stakeholder Register

| Stakeholder                       | Role in Business                                         | Primary Need from the System                                                                              | Influence | Interest |
| --------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------- | -------- |
| Store / Operations Management     | Oversees store performance and operational decisions     | Visibility into sales, stock position, slow movers, product performance and operational KPIs              | High      | High     |
| Purchasing / Inventory Management | Manages stock availability and replenishment decisions   | Sales velocity, stock levels, ABC classification, reorder recommendations and slow-moving inventory flags | High      | High     |
| Sales Management                  | Monitors sales and product/category performance          | Revenue, units sold, product ranking, category contribution and period-on-period performance              | High      | High     |
| Finance                           | Monitors profitability, costs and financial performance  | Sales value, unit cost, gross profit, margin %, reconciliation and pricing-margin controls                | High      | High     |
| Pricing / Commercial Management   | Reviews pricing and promotional decisions                | Product price, SOA, competitor prices, margin-floor checks and price recommendations                      | High      | High     |
| Store Sales Staff                 | Supports customers and sells products on the shop floor  | Fast access to accurate product specifications, dimensions, features and product comparisons              | Medium    | High     |
| Data / Business Analyst           | Maintains analysis, reporting and data-quality processes | Governed datasets, KPI definitions, SQL views, dashboards and traceable data sources                      | Medium    | High     |
| System / Data Administrator       | Supports technical operation of the solution             | Reliable ETL, database refresh, monitoring, access control and auditability                               | Medium    | Medium   |

---


## 3.2 Stakeholder Classification

### Primary Business Stakeholders

- Store / Operations Management
- Purchasing / Inventory Management
- Sales Management
- Finance
- Pricing / Commercial Management

These stakeholders are the primary decision-makers and consumers of business intelligence produced by the system.

### Operational Users

- Store Sales Staff

Store sales staff primarily interact with the Product Knowledge Layerto retrieve verified product specifications and comparative product information for customer-facing use.

### Technical / Analytical Stakeholders

- Data / Business Analyst
- System / Data Administrator

These stakeholders are responsible for maintaining the governed data layer, analytical logic, reporting outputs, data quality and system operation.


## 3.3 Stakeholder Requirements Summary

| Stakeholder                 | Key Information / Capability Required                                 |
| --------------------------- | --------------------------------------------------------------------- |
| Operations Management       | Executive KPIs, stock visibility, category/product performance        |
| Purchasing                  | Stock levels, sales velocity, ABC class, reorder and slow-mover flags |
| Sales Management            | Revenue, units sold, product ranking, category performance            |
| Finance                     | Cost, sales value, gross profit, margin and reconciliation            |
| Pricing / Commercial        | SOA, competitor comparison, margin floor and approval workflow        |
| Store Sales Staff           | Product specifications, dimensions, features and grounded comparisons |
| Data / Business Analyst     | Governed SQL data, KPI logic, data quality and reporting              |
| System / Data Administrator | ETL reliability, refresh monitoring, access and audit logs            |

# 4. AS-IS Business Process

> Detailed process maintained in `02_AS_IS_TO_BE_Process.md`.

---

# 5. TO-BE Business Process

> Detailed process maintained in `02_AS_IS_TO_BE_Process.md`.

---

# 6. Business Questions


The Smart AI Retail System is designed to answer a defined set of business questions across sales, profitability, inventory, pricing and
product intelligence.

These questions establish the analytical requirements of the project and will later be mapped to measurable KPIs and acceptance criteria.

---

## 6.1 Executive Performance Questions

BQ-01: What is the total sales revenue for the selected reporting period?

BQ-02: What is the total gross profit generated during the selected
reporting period?

BQ-03: What is the overall gross margin percentage?

BQ-04: Which product categories contribute the most to revenue and
gross profit?

BQ-05: Which individual products contribute the most to revenue and
gross profit?

BQ-06: How does sales performance change between the available
reporting periods?

BQ-07: What proportion of total revenue and profit is generated by the
highest-contributing products or categories?

---

## 6.2 Sales Performance Questions

BQ-08: Which products have the highest and lowest units sold?

BQ-09: Which products have the highest and lowest sales value?

BQ-10: Which products generate the highest and lowest gross profit?

BQ-11: Which products or categories have unusually high or low gross
margin percentages?

BQ-12: What is the sales velocity of each product?

BQ-13: Which products are high-performing, medium-performing or
low-performing based on agreed performance measures?

BQ-14: Which products or categories show meaningful period-on-period
changes in sales performance?

---

## 6.3 Inventory Questions

BQ-15: How much stock is currently available for each product?

BQ-16: How is stock distributed across individual store locations?

BQ-17: Which products have high demand but relatively low stock?

BQ-18: Which products have low demand but relatively high stock?

BQ-19: Which products currently have a balanced relationship between
sales velocity and available stock?

BQ-20: Which products should be classified as slow-moving inventory?

BQ-21: Which products should be considered for reorder, review or
no action based on the approved inventory rules?

BQ-22: Which products or categories account for the greatest inventory
value and therefore require tighter inventory control?

---

## 6.4 Product and Category Segmentation Questions

BQ-23: Which products account for the majority of revenue and profit using Pareto analysis?

BQ-24: How should products be classified using ABC inventory classification?

BQ-25: Which product/category combinations represent the strongest commercial performers?

BQ-26: Which product/category combinations require management attention because of weak sales, low margin or excess stock?

---

## 6.5 SOA Questions

BQ-27: Which products currently have an applicable Sell Out Allowance (SOA)?

BQ-28: What SOA value applies to each product during its defined Starts-to-Ends window?

BQ-29: Which SOA records are currently active, upcoming or expired relative to the relevant reporting date?

BQ-30: How can SOA information be associated with the correct governed product record for downstream pricing analysis?

---

## 6.6 Pricing Intelligence Questions

BQ-31: What is our current selling price for a product?

BQ-32: What verified competitor prices are available for the exact matching product?

BQ-33: How does our selling price compare with the verified competitor price?

BQ-34: What is the percentage price variance between our price and the competitor price?

BQ-35: Is the competitor product match sufficiently confident to support an automated pricing decision?

BQ-36: Would matching or undercutting the competitor price breach the configured margin floor?

BQ-37: What new price should be recommended after considering product cost, current price, SOA, competitor price and configured business rules?

BQ-38: Can the recommendation be automatically approved, or does it require management review?

BQ-39: Why was a pricing recommendation approved, rejected, blocked or routed for manual review?

---

## 6.7 Product Knowledge Questions

BQ-40: What exact product corresponds to the entered model number or scanned barcode/QR identifier?

BQ-41: How confident is the system that the correct product variant has been identified?

BQ-42: What verified specifications are available for the product?

BQ-43: What are the product's dimensions, capacity and key features where those attributes are applicable and available from the verified source?

BQ-44: What manufacturer source supports the displayed product information?

BQ-45: How complete and current is the available product information?

BQ-46: How does the product compare with relevant products in the same catalogue based on verified specifications?

BQ-47: What evidence supports each comparative product advantage or disadvantage presented to staff?

---

## 6.8 Forecasting Questions — Conditional

The following questions are conditional and will only become active if the Phase 3 forecasting feasibility assessment supports forecasting.

BQ-48: Does the available historical data contain sufficient independent time periods to support meaningful forecasting?

BQ-49: What baseline forecasting approach is appropriate for the available data?

BQ-50: Can a forecasting model outperform the selected naive baseline on time-based out-of-sample data?

BQ-51: If forecasting is feasible, what future demand is expected at the supported product or category level?

BQ-52: What level of forecast uncertainty should be communicated when the forecast contributes to downstream decisions?

---

## 6.9 Data Quality and Governance Questions

BQ-53: Can products be consistently matched across Stock Code and Model?

BQ-54: Are there unmatched or ambiguous products across the source datasets?

BQ-55: Do calculated revenue, profit and margin measures reconcile with the source data within the agreed tolerance?

BQ-56: Are duplicate, missing or invalid records present in the governed data?

BQ-57: Are negative Level values being handled according to the documented business rule?

BQ-58: When was the underlying data last refreshed?

BQ-59: Can each important analytical or recommendation output be traced back to its governed source and business rule?

---

## 6.10 AI Retail Assistant Questions

The AI Retail Assistant should provide a natural-language interface to approved business questions rather than acting as an unrestricted source of business information.

Initial approved question categories include:

- Sales performance
- Revenue and profitability
- Product/category contribution
- Inventory position
- Slow-moving inventory
- Reorder recommendations
- Approved pricing intelligence
- Product specifications and comparisons
- Data refresh and source information

The assistant must answer from governed data or verified product
knowledge sources and must not invent unavailable values or product
specifications.

---

# 7. Key Performance Indicators (KPIs)

## 7.1 Data Quality & Governance KPIs

| KPI ID | KPI                             | Definition                                                                  | Formula / Logic                                      |
| ------ | ------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------- |
| KPI-40 | Product Match Rate              | Percentage of source product records mapped to the canonical Product Master | Matched Products / Products Requiring Mapping × 100 |
| KPI-41 | Unmatched Product Count         | Number of product records that cannot be confidently mapped                 | COUNT(Unmatched Products)                            |
| KPI-42 | Duplicate Record Count          | Number of records violating the approved uniqueness rule                    | COUNT(Duplicate Records)                             |
| KPI-43 | Required-Field Null Count       | Missing values in fields defined as mandatory                               | COUNT(Required Null Values)                          |
| KPI-44 | Revenue Reconciliation Variance | Difference between governed revenue and source revenue                      | Governed Revenue - Source Revenue                    |
| KPI-45 | Profit Reconciliation Variance  | Difference between governed gross profit and source profit                  | Governed GP - Source Profit                          |
| KPI-46 | Data Refresh Date               | Most recent successful governed data refresh                                | MAX(Successful Refresh Timestamp)                    |

## 7.2 KPI Validation Principles

Before a KPI is approved for downstream use:

1. Its business definition must be documented.
2. Its calculation must have one governed implementation.
3. Required source fields must be identified.
4. Calculated financial KPIs must be reconciled against source values.
5. Any differences must be investigated rather than silently corrected.
6. KPI calculations must handle null, zero and invalid denominator cases
   explicitly.
7. Product-level KPIs must use the governed canonical product key.
8. Store-level inventory KPIs must use the reshaped governed stock data.
9. Time-dependent KPIs must use validated reporting periods rather than
   assumed dates or durations.
10. Recommendation KPIs must expose the business rule responsible for
    their classification.
11. Conditional KPIs must not be exposed as production measures until
    their prerequisite phase has passed its gate.

# 8. Project Scope

## 8.1 In Scope

The scope defines the business and technical boundaries of the Smart AI Retail System.

Capabilities are classified into three groups:

1. In Scope
2. Conditional Scope
3. Out of Scope

This distinction prevents experimental or externally dependent capabilities from being treated as guaranteed project deliverables.

## 8.2 Out of Scope / Conditional Scope


## A. Data Integration and Governance

The project will integrate the currently available retail data sources:

- Master_Sales_data.xlsx
- Stock_on_Hand_Report.xlsx
- MasterSOA.xlsx

The project will:

- Profile and validate source data
- Standardize data types and structures
- Investigate data-quality issues
- Reshape store-level inventory data
- Reconcile Stock Code and Model identifiers
- Establish a canonical Product Master
- Consolidate governed sales information
- Integrate stock information
- Integrate Sell Out Allowance (SOA) information
- Perform financial reconciliation
- Maintain documented transformation rules
- Produce data-quality outputs

---

## B. Governed Retail Data Layer

The project will create a governed analytical data model containing,
at minimum:

- dim_product
- dim_store
- fact_sales
- fact_stock
- fact_soa

This governed layer will act as the analytical Single Source of Truth.

Downstream analytical applications should consume governed tables or approved views rather than independently processing the raw Excel sources.

---

## C. Sales and Profitability Analytics

The project will support analysis of:

- Revenue
- Units sold
- Cost of sales
- Gross profit
- Gross margin %
- Sales velocity
- Product performance
- Category performance
- Revenue contribution
- Profit contribution
- Period-on-period performance

Financial measures will be reconciled against source information before
being approved for downstream use.

---

## D. Product and Category Analysis

The project will include analytical techniques such as:

- Product ranking
- Category ranking
- Pareto analysis
- ABC classification
- Margin outlier analysis
- Product/category performance segmentation

These outputs will support identification of commercially important products and products requiring management attention.

---

## E. Inventory Intelligence

The project will combine governed sales and stock information to support:

- Store-level stock visibility
- Total product stock
- Sales-to-stock analysis
- High-demand / low-stock identification
- Low-demand / high-stock identification
- Balanced inventory identification
- Slow-mover identification
- Reorder recommendations

The final operational recommendation states will include:

- Reorder
- Review
- No Action

Recommendation rules will be governed and reusable across downstream applications.

---

## F. Power BI Decision Support

The project will develop Power BI reporting based on the governed data layer.

The planned reporting scope includes:

### Executive Dashboard

- Revenue
- Gross profit
- Margin
- Performance trends
- Category contribution

### Sales Dashboard

- Product performance
- Product ranking
- Category performance
- Period-on-period analysis
- Pareto analysis

### Inventory Dashboard

- Store-level stock
- ABC classification
- Slow movers
- Reorder indicators

Dashboard measures must reconcile against the governed reference calculations.

---

## G. Pricing Intelligence

The project will design and, where technically and commercially feasible, implement a controlled pricing-intelligence workflow using:

- Product identity
- Current selling price
- Unit cost
- SOA
- Verified competitor price
- Product-match confidence
- Price variance
- Margin-floor rules
- Approval rules

The pricing workflow will support:

- Price recommendations
- Automatic blocking of margin-floor breaches
- Manager review for uncertain/out-of-policy cases
- Approval tracking
- Pricing audit logging

No uncertain product match should silently generate an automatic price change.

---

## H. AI Retail Assistant

The project will develop a natural-language decision-support interface over approved governed information.

The assistant will support approved question categories relating to:

- Sales
- Profitability
- Product performance
- Inventory
- Slow movers
- Reorder recommendations
- Approved pricing intelligence
- Product information

The assistant must use governed or verified sources and should expose source/refresh information.

---

## I. Product Knowledge Layer

The project will include a staff-facing product knowledge capability.

Planned functionality includes:

- Model-number lookup
- Barcode/QR lookup where mapping is available
- Product identity matching
- Match-confidence assessment
- Retrieval of manufacturer product information
- Structured specification extraction
- Validation of extracted information
- Product specification storage
- Comparative product information
- Staff-facing product specification cards

Product specifications must not be guessed when an exact or sufficiently confident product match cannot be established.

---

## J. Data Quality, Traceability and Control

The project will implement controls covering:

- Null values
- Duplicate records
- Product-key consistency
- Negative-value business rules
- Financial reconciliation
- Data refresh information
- Recommendation traceability
- Pricing auditability
- Version-controlled analytical logic



## 8.3 Conditional Scope

The following capabilities are part of the project roadmap but depend on
feasibility, data availability, external-system access or business
approval.

### A. Demand Forecasting

Demand forecasting is conditional on the Phase 3 data-sufficiency
assessment.

The available source data contains only a limited number of monthly
sales snapshots. Therefore, the project will not assume that reliable
SKU-level forecasting is possible.

Forecasting will proceed only where:

- Sufficient independent historical periods exist
- A valid time-based evaluation can be performed
- Forecast performance can be compared with an appropriate naive
  baseline
- The resulting forecast is sufficiently reliable for its intended use

Possible approaches may include:

- Naive baseline
- Moving average
- Seasonal-naive approach
- ARIMA/SARIMA
- Prophet
- Tree-based forecasting approaches

Complex models will only be considered if the data supports them.

If these conditions are not satisfied, forecasting will be formally
descoped or retained as baseline-only analysis.

---

### B. Automated Competitor Price Collection

Competitor pricing is included in the Pricing Intelligence design, but
the collection mechanism is conditional.

Preferred methods include:

1. Official retailer/product feeds
2. Approved APIs
3. Affiliate/product-data feeds
4. Authorized price-data providers

Web scraping should only be considered where technically appropriate
and permitted.

A competitor website blocking automated access must not be bypassed in
a way that introduces an unreliable or non-compliant production
dependency.

The competitor collection component must remain decoupled from the
pricing decision engine.

---

### C. Automatic ESL Price Push

The system will design the approval-to-ESL workflow.

Actual Electronic Shelf Label integration is conditional on:

- Identifying the ESL vendor
- Obtaining integration documentation
- Obtaining API/feed access
- Authentication credentials
- Availability of a safe test environment
- Business authorization

If live ESL access is unavailable, the portfolio implementation may
terminate at an approved price-update output or simulated integration
boundary.

---

### D. Automatic Pricing Approval

Automatic approval of routine pricing recommendations is conditional on:

- Approved margin-floor rules
- Approved variance boundaries
- High-confidence product matching
- Pricing/commercial authorization
- Successful testing
- Auditability

Until these controls are approved, pricing outputs should be treated as
recommendations requiring human review.

---

### E. Barcode / QR Product Resolution

Barcode/QR lookup is conditional on the availability of a reliable
mapping between the scanned identifier and the governed product model.

If existing barcodes cannot be reliably mapped to Product Master
records, model-number lookup will remain the primary supported method.

---

### F. Manufacturer Product Information Retrieval

Automated product-specification retrieval is conditional on:

- Availability of reliable manufacturer sources
- Ability to identify the exact product variant
- Accessible product pages or manuals
- Successful structured extraction and validation

Where automated retrieval is unavailable, the Product Knowledge Layer
may use manually curated verified product records.

---

### G. Live Production Deployment

The portfolio system may demonstrate production-style architecture,
testing and deployment patterns.

Deployment into an actual retailer's production environment remains
conditional on:

- Business authorization
- Infrastructure access
- Security review
- Data-access approval
- External-system credentials
- Operational ownership


## 8.4 Out of Scope

The following capabilities are outside the initial Smart AI Retail System project scope.

### A. Replacement of Core Retail Systems

The project will not replace:

- Point-of-Sale (POS) systems
- ERP systems
- Accounting systems
- Warehouse-management systems
- Existing stock-control systems

The Smart AI Retail System is a decision-support and intelligence layer, not a replacement transactional retail platform.

---

### B. Transaction Processing

The system will not initially process:

- Customer payments
- Refunds
- Till transactions
- Supplier payments
- Purchase-order financial settlement

---

### C. Fully Autonomous Purchasing

The Inventory Intelligence layer may recommend reorder actions.

It will not initially:

- Automatically create supplier purchase orders
- Select suppliers autonomously
- Commit purchasing expenditure
- Automatically approve inventory purchases

Reorder outputs remain decision-support recommendations unless a future approved integration extends the scope.

---

### D. Uncontrolled Autonomous Pricing

The project will not implement pricing logic that changes retail prices without the defined commercial controls.

Specifically excluded:

- Price changes based on low-confidence competitor matches
- Price changes below the approved margin floor
- Silent price pushes without audit records
- Uncontrolled AI-generated prices

---

### E. Customer-Specific Personalization

The initial project does not include:

- Customer profiling
- Individual recommendation engines
- Personalized pricing
- Loyalty-customer segmentation
- Customer lifetime value modelling

The currently available project datasets do not provide the required customer-level information.

---

### F. Customer Behaviour / Marketing Modelling

The project does not initially include:

- Churn prediction
- Customer propensity modelling
- Marketing attribution
- Campaign-response modelling
- Customer sentiment analysis

These require datasets outside the currently defined source inventory.

---

### G. Supplier Optimization

The initial system does not model:

- Supplier lead-time optimization
- Supplier reliability scoring
- Supplier price forecasting
- Supplier selection optimization

Supplier-level data is not part of the currently defined source inventory.

---

### H. Review-Based Product Recommendations

The initial Product Knowledge Layer will not generate product pros/cons from scraped customer reviews or external review sentiment.

Initial comparisons will be grounded in verified product specifications and catalogue-level comparisons.

---

### I. Unsupported AI Answers

The AI Retail Assistant will not act as an unrestricted general-purpose business authority.

It must not:

- Invent unavailable business figures
- Guess missing product specifications
- Present unverified competitor information as fact
- Override governed pricing rules
- Perform unauthorized write operations

---

# 9. Business Requirements

Detailed business, functional and non-functional requirements are maintained in:

`docs/03_Requirements_Acceptance_Criteria.xlsx`

The requirements matrix provides traceability between:

Business Problem
→ Project Objectives
→ Business Questions
→ KPIs
→ Requirements
→ Acceptance Criteria
→ Validation Evidence

Requirements are classified as:

- BR — Business Requirements
- FR — Functional Requirements
- NFR — Non-Functional Requirements

Each requirement has an assigned priority, target implementation phase, validation method and implementation status.

At the completion of Phase 1, requirements define the expected system behaviour but remain primarily in Pending status.

Requirements will transition to Passed only when objective validation evidence is produced during the relevant implementation phase.

---

# 10. Assumptions and Constraints

> To be completed during Phase 1.

---

# 11. Phase 1 — Define Gate


## 11.1 Gate Purpose

The purpose of the Define Gate is to confirm that the Smart AI Retail
System has a sufficiently clear business definition before data
engineering and governed dataset construction begin in Phase 2.

Phase 1 establishes what problem is being solved, for whom, what the
system is expected to achieve, how success will be measured and what
falls inside or outside the project boundary.

---

## 11.2 Define Gate Validation

| Gate Item                   | Validation                                                                                  | Status |
| --------------------------- | ------------------------------------------------------------------------------------------- | ------ |
| Business Problem            | Current retail data fragmentation and decision-support problem documented                   | PASS   |
| Business Impact             | Inventory, sales, profitability, pricing, reporting and decision-support impacts identified | PASS   |
| Desired Outcome             | Governed retail decision-support target state defined                                       | PASS   |
| Project Objectives          | Primary, business and conditional objectives documented                                     | PASS   |
| Stakeholders                | Business, operational and technical stakeholder groups identified                           | PASS   |
| AS-IS Process               | Current data and analytical state documented                                                | PASS   |
| TO-BE Process               | Future governed decision-support process documented                                         | PASS   |
| Business Questions          | Approved project question catalogue established                                             | PASS   |
| KPI Definitions             | KPI dictionary and governance principles documented                                         | PASS   |
| Project Scope               | In-scope capabilities documented                                                            | PASS   |
| Conditional Scope           | Forecasting and externally dependent integrations identified                                | PASS   |
| Out-of-Scope                | Explicit project exclusions documented                                                      | PASS   |
| Business Requirements       | BR requirements defined                                                                     | PASS   |
| Functional Requirements     | FR requirements defined                                                                     | PASS   |
| Non-Functional Requirements | NFR requirements defined                                                                    | PASS   |
| Acceptance Criteria         | Testable criteria associated with requirements                                              | PASS   |
| Requirements Traceability   | Business Questions → KPIs → Requirements → Validation structure defined                  | PASS   |
| Phase 2 Readiness           | Define-stage requirements sufficient to begin governed dataset construction                 | PASS   |

---

## 11.3 Phase 1 Gate Result

**Gate Result: PASS — Portfolio / Project Definition Approved**

The Smart AI Retail System has a sufficiently defined business problem, scope, stakeholder model, business-question catalogue, KPI framework and requirements baseline to proceed to Phase 2 — Measure.

This gate represents project-definition approval for the portfolio implementation.

It does not represent formal approval or sign-off by the retailer, management, finance, purchasing, pricing or other external business
stakeholders unless such approval is obtained separately.


## 11.4 Open Decisions Carried Forward

The following items are intentionally unresolved at the Define Gate and
will be resolved during their appropriate implementation or analysis
phase.

| Open Decision                                              | Resolution Phase     |
| ---------------------------------------------------------- | -------------------- |
| Final governed relationship between Stock Code and Model   | Phase 2              |
| Treatment/business interpretation of negative Level values | Phase 2              |
| Relationship between Master_data and monthly sales sheets  | Phase 2              |
| Final Sales Velocity time unit                             | Phase 2              |
| Financial reconciliation tolerance                         | Phase 2              |
| ABC classification boundaries                              | Phase 3              |
| High-demand / low-stock thresholds                         | Phase 3 / Phase 5    |
| Slow-mover threshold                                       | Phase 5              |
| Reorder rule boundaries                                    | Phase 5              |
| Forecasting feasibility                                    | Phase 3              |
| Forecast model selection                                   | Phase 6, if approved |
| Pricing margin floor                                       | Phase 7              |
| Pricing variance band                                      | Phase 7              |
| Competitor price collection mechanism                      | Phase 7              |
| Live ESL integration mechanism/vendor access               | Phase 7              |
| Barcode-to-model mapping availability                      | Phase 8              |
| Manufacturer specification retrieval coverage              | Phase 8              |


## 11.5 Confirmed Business Definition — SOA

During Phase 0, the business meaning of SOA was clarified.

**SOA = Sell Out Allowance**

SOA represents an additional discount/support value applicable to a
product during the corresponding Starts-to-Ends date window.

This definition will be used consistently throughout the governed data
model, analytical layer and Pricing Intelligence workstream.

The unit/financial interpretation of the stored SOA value should remain
consistent with the source/business rules and must not be assumed where
not explicitly established.
