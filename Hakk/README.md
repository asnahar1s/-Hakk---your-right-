# Hakk (حق)
AI contract reader for Gulf migrant workers. Explains contracts in the worker's language and flags risky clauses with a quoted clause and a quoted rule. Information, not legal advice.

Built on Nebius Token Factory with NVIDIA Nemotron.

## Run
pip install -r requirements.txt
export NEBIUS_API_KEY=...
export NEBIUS_MODEL=<nemotron model id>
streamlit run app.py

## Safety design
- No flag is shown unless its clause quote exists verbatim in the contract (checked in code).
- Rules come from a fixed list with source links; the model cannot invent rules.
- Unsure cases are phrased as questions to ask, not accusations.

## License
MIT
