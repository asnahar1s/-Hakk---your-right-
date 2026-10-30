"""Hakk - contract reader for Gulf migrant workers.
Runs on Nebius Token Factory with an NVIDIA Nemotron model.
Not legal advice. Information about your rights only.
"""
import json, os, re
import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
    api_key=os.environ["NEBIUS_API_KEY"],
)
MODEL = os.getenv("NEBIUS_MODEL", "nvidia/Nemotron-3-Ultra-550b-a55b")

LAW_URL = "https://uaelegislation.gov.ae/en/legislations/1541/download"

RULES = [
    {"id": "R1", "topic": "passport retention",
     "text": "Federal Decree-Law No. 33 of 2021, Article 13(2): the employer must not withhold the worker's official documents or force him to leave the State when the labour relation ends.",
     "source": LAW_URL},
    {"id": "R2", "topic": "recruitment fees",
     "text": "Federal Decree-Law No. 33 of 2021, Article 6(4): the employer is prohibited from charging the worker the fees and costs of recruitment and employment, or collecting them from him, directly or indirectly.",
     "source": LAW_URL},
    {"id": "R3", "topic": "wage deductions",
     "text": "Federal Decree-Law No. 33 of 2021, Article 25: no amount may be deducted from the worker's wage except in the listed cases (for example loan recovery with written consent, overpayments up to 20% of the wage, approved disciplinary penalties up to 5%). Total deductions may never exceed 50% of the wage.",
     "source": LAW_URL},
    {"id": "R4", "topic": "overtime",
     "text": "Federal Decree-Law No. 33 of 2021, Article 19: overtime is limited to two hours per day and must be paid at the normal wage plus at least 25%, or at least 50% extra between 10 pm and 4 am.",
     "source": LAW_URL},
    {"id": "R5", "topic": "complaints",
     "text": "Federal Decree-Law No. 33 of 2021, Article 54: a worker with a dispute applies to the Ministry of Human Resources and Emiratisation (MOHRE), which tries to settle it. Website: mohre.gov.ae. Call centre: 600590000.",
     "source": LAW_URL},
]

LANGS = ["English", "Hindi", "Urdu", "Malayalam", "Bengali", "Tagalog", "Arabic"]

SYSTEM = """You help migrant workers understand employment contracts.
You give information, not legal advice.
Return ONLY JSON:
{"summary": "<plain-language summary in TARGET_LANG>",
 "flags": [{"clause_quote": "<EXACT text copied from the contract>",
            "rule_id": "<id from RULES>",
            "why": "<short explanation in TARGET_LANG>",
            "confidence": "high|medium|low"}],
 "questions_to_ask": ["<question in TARGET_LANG>"]}
Hard rules:
- Never flag without an exact clause_quote copied from the contract.
- Never cite a rule that is not in RULES.
- If unsure, use confidence "low" and phrase it as a question, not as 'illegal'.
- Use very simple words.
- Write every TARGET_LANG field ONLY in TARGET_LANG, in its own script.
- Never mix in words from any other language (no French, Russian, Japanese or other words).
- If you do not know a word in TARGET_LANG, write the simple English word instead.
- Keep sentences short. Short sentences make fewer mistakes."""


def analyse(contract: str, lang: str) -> dict:
    user = (f"TARGET_LANG: {lang}\n"
            f"Write summary, why and questions_to_ask ONLY in {lang}. No other languages.\n"
            f"RULES: {json.dumps(RULES)}\nCONTRACT:\n{contract}")
    r = client.chat.completions.create(
        model=MODEL, temperature=0,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}],
    )
    text = r.choices[0].message.content
    m = re.search(r"\{.*\}", text, re.S)  # tolerate extra text around JSON
    return json.loads(m.group(0))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


st.set_page_config(page_title="Hakk", page_icon="⚖️")

st.markdown("""
<style>
.stApp {background: linear-gradient(160deg, #F6EFE3 0%, #E4F2EC 100%);}
header[data-testid="stHeader"] {background: transparent;}
.block-container {max-width: 820px; padding-top: 5rem;}

.hero {padding: 30px 28px; border-radius: 20px; margin-bottom: 1.6rem;
       background: linear-gradient(135deg, #0F5C4D 0%, #1F8A70 100%);
       box-shadow: 0 10px 30px rgba(15,92,77,.25);}
.hero .tag {color: #F5D98B !important; letter-spacing: .14em; font-size: .78rem; text-transform: uppercase;}
.hero h1 {margin: .2rem 0 0; font-size: 2.6rem; color: #ffffff !important;}
.hero p {margin: .5rem 0 0; color: #E3F4EE !important; font-size: 1.02rem;}

h3 {color: #0F5C4D !important;}
label p {color: #12372F !important; font-weight: 600;}

[data-testid="stVerticalBlockBorderWrapper"] {
       background: #ffffff; border: 1px solid #CFE3DA;
       border-radius: 16px; box-shadow: 0 4px 16px rgba(15,92,77,.08);}

textarea, div[data-baseweb="select"] > div {
       background: #ffffff !important; color: #12372F !important;
       border: 1.5px solid #BFD8CE !important; border-radius: 12px !important;}

div.stButton > button {background: #0F5C4D; color: #ffffff; font-weight: 700;
       border: 0; border-radius: 12px; padding: .65rem 1.6rem;
       box-shadow: 0 4px 12px rgba(15,92,77,.3);}
div.stButton > button:hover {background: #1F8A70; color: #ffffff;}
.stApp, .stApp p, .stApp li, .stApp span, .stApp label,
.stApp [data-testid="stMarkdownContainer"] {color: #111111;}
.hero h1 {color: #ffffff !important;}
.hero p {color: #E3F4EE !important;}
.hero .tag {color: #F5D98B !important;}
h2, h3 {color: #0F5C4D !important;}
div.stButton > button p {color: #ffffff !important;}
</style>
<div class="hero">
  <div class="tag">Know your rights</div>
  <h1>⚖️ Hakk &nbsp;حق</h1>
  <p>Understand your contract before you sign. Plain language, quoted evidence, official sources.</p>
  <p style="font-size:.85rem;opacity:.85;">Information about your rights, not legal advice.</p>
</div>
""", unsafe_allow_html=True)

lang = st.selectbox("Explain in", LANGS)
contract = st.text_area("Paste your contract text", height=260)

if st.button("Check my contract") and contract.strip():
    with st.spinner("Reading..."):
        try:
            out = analyse(contract, lang)
        except Exception as e:
            st.error(f"Could not analyse: {e}")
            st.stop()

    st.subheader("Summary")
    st.write(out.get("summary", ""))

    rules = {r["id"]: r for r in RULES}
    st.subheader("Clauses to look at")
    shown = 0
    for f in out.get("flags", []):
        # Evidence check: quote must really exist in the contract, rule must exist.
        if norm(f.get("clause_quote", "")) not in norm(contract):
            continue
        rule = rules.get(f.get("rule_id"))
        if not rule:
            continue
        shown += 1
        icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(f.get("confidence"), "🟡")
        with st.container(border=True):
            st.markdown(f"{icon} **Contract says:** “{f['clause_quote']}”")
            st.markdown(f"**Related rule:** {rule['text']}  \n[Source]({rule['source']})")
            st.markdown(f"**Why it matters:** {f.get('why', '')}")
    if shown == 0:
        st.success("No clearly risky clauses found. Still read everything carefully.")

    st.subheader("Ask your employer")
    for q in out.get("questions_to_ask", []):
        st.markdown(f"- {q}")

    st.info("Need help? Contact MOHRE at mohre.gov.ae or call 600590000. "
            "This is information about your rights, not legal advice.")
