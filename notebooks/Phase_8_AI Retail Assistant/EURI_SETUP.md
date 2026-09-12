# Euri product pilot

The root `.env` contains `EURI_API_KEY` and is ignored by Git. No key is
embedded in the notebook or Python files. An environment variable overrides
the `.env` value. The pilot model defaults to `gpt-5.6`; set `EURI_MODEL` in
the process environment to override it.

Run Step 13 in `08_AI_Retail_Assistant.ipynb`, or from the project root:

```powershell
python "notebooks/Phase_8_AI Retail Assistant/euri_product_pilot.py"
```

Each run makes five live requests and overwrites `euri_pilot_results.json`
beside the script. The original specification prompt is preserved in
`product_specs_prompt.py`. The API uses Chat Completions response handling.

The `web_search` tool is an experimental compatibility probe. HTTP 200,
generated links, and statements that the model searched do not prove search
execution. `NO_SEARCH_EVIDENCE` means the response exposed no checked search
metadata. `METADATA_REQUIRES_REVIEW` means metadata was returned but still
needs inspection; tool calls can be requests for client execution.

`candidate_specs` and `api_response` are diagnostic, unverified model output.
The main specification fields stay null, with `match_status=UNVERIFIED`.
Do not ingest candidate output into the Product Knowledge layer as verified
facts. A working retrieval integration and review of exact-model source
content are needed before promoting those values.

Provider reference: https://docs.euri.ai/api-reference/chat-completions
