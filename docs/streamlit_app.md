# Smart AI Retail Assistant

Run from the project root:

```powershell
python -m pip install -r requirements-streamlit.txt
python -m streamlit run ai_assistant_app.py
```

Business Analytics uses the Phase 8 rule-based query functions extracted into
`retail_backend.py`. Supported questions include top selling products, highest
revenue, highest profit, category performance, urgent reorders, slow movers,
and active SOA. Other questions receive an unsupported-question response.
SOA eligibility uses today's date against saved offer windows. Sales summaries
cover all periods in the saved sales dataset; stock is a saved snapshot.

Product Lookup matches normalized model identifiers against the product master
and displays sales, stock, SOA, and inventory recommendations. Ambiguous model
matches are shown for review rather than selected automatically.

Product Knowledge reads `notebooks/Phase_8_AI Retail Assistant/euri_pilot_results.json`.
It matches manufacturer and exact model, including suffixes, and labels all
candidate specifications and source links unverified. It does not run the pilot.

The app uses no API keys, makes no model API calls, and does not execute the notebook.
Data files are resolved relative to the app location. Restart Streamlit after
updating CSV files to reload the backend datasets. Saved JSON is read on lookup.
