# ⚖️ Hakk (حق)

**Understand your contract before you sign.**

Hakk is a contract reader for migrant workers in the UAE. A worker pastes in their employment contract, picks their language, and gets a plain-language summary, the risky clauses quoted word for word, the UAE labour law rule each one relates to, and questions to ask the employer.

> **Not legal advice.** Hakk gives information about your rights only.

## 🚀 Try it

- **Live demo:** https://h6mbobcpadamqvxnnxfgeq.streamlit.app/
- **Demo video:** [Watch on YouTube](YOUR-YOUTUBE-LINK)
- **Source code:** [GitHub repository]((https://github.com/asnahar1s/-Hakk---your-right-))

**Want to test it quickly?** Open the live demo, choose a language, and paste this sample text:

```
The employer will hold the employee's passport during the contract period. A recruitment fee of AED 3,000 will be deducted from the first three salaries.
```

Then click **Check my contract**. Hakk should flag both clauses and show the UAE law each one relates to.

## The problem

Many migrant workers in the Gulf sign contracts they cannot fully read. Illegal terms like passport retention, recruitment fees charged to the worker, and unfair wage deductions often sit inside long legal text in a language the worker does not speak well.

## What Hakk does

- **Plain-language summary** of the contract in very simple words
- **7 languages:** English, Hindi, Urdu, Malayalam, Bengali, Tagalog, Arabic
- **Quoted evidence:** every flagged clause is shown with the exact text from the contract
- **Official sources:** every flag links to the UAE law it relates to
- **Questions to ask your employer** before signing
- **Help contact:** MOHRE website and call centre

## What it checks

The rules come from Federal Decree-Law No. 33 of 2021 (UAE labour law):

| Topic | Article |
|---|---|
| Passport / document retention | Article 13(2) |
| Recruitment fees charged to the worker | Article 6(4) |
| Wage deductions | Article 25 |
| Overtime | Article 19 |
| Complaints (MOHRE) | Article 54 |

## How it avoids made-up answers

AI models can invent things, so Hakk checks the model's output before showing it:

1. A flag is shown **only if its quote really appears in the contract** the user pasted.
2. A flag is shown **only if it cites a rule from the fixed rule list**. Anything else is discarded.
3. If the model is unsure, it must mark the flag as low confidence and phrase it as a question, not as "illegal".

## Tech stack

- [Streamlit](https://streamlit.io) for the web app
- [Nebius Token Factory](https://tokenfactory.nebius.com) for model hosting
- NVIDIA Nemotron model for the analysis
- Python with the `openai` client library

## Run it on your computer

1. Install Python 3.10 or newer.
2. Install the requirements:

   ```
   pip install -r requirements.txt
   ```

3. Set your API key (Windows PowerShell):

   ```
   $env:NEBIUS_API_KEY="your-key-here"
   ```

   On Mac or Linux:

   ```
   export NEBIUS_API_KEY="your-key-here"
   ```

4. Start the app:

   ```
   streamlit run app.py
   ```

5. Open the address shown in the terminal, usually `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** and pick this repo, branch `main`, main file `app.py`.
4. Under **Advanced settings → Secrets**, add:

   ```toml
   NEBIUS_API_KEY = "your-key-here"
   ```

5. Click **Deploy**.

Never commit your API key to GitHub.

## Settings

| Variable | Purpose | Default |
|---|---|---|
| `NEBIUS_API_KEY` | Your Nebius API key (required) | none |
| `NEBIUS_BASE_URL` | API address | `https://api.tokenfactory.nebius.com/v1/` |
| `NEBIUS_MODEL` | Model name | `nvidia/Nemotron-3-Ultra-550b-a55b` |

## Project structure

```
Hakk
├── app.py                  # the whole app
├── requirements.txt        # Python packages
├── README.md               # this file
└── .streamlit
    └── config.toml         # light theme colors
```

## Limitations

- Hakk covers only the five topics in the rule list above. A contract with no flags is not guaranteed to be fine.
- Translations are produced by an AI model and can contain mistakes, especially in less common languages.
- It reads pasted text only. It does not read photos or PDFs yet.
- It does not replace a lawyer or MOHRE.
- The live demo may be slow on the first load, because free Streamlit apps go to sleep when nobody uses them.

## Need help?

Contact the Ministry of Human Resources and Emiratisation (MOHRE):

- Website: [mohre.gov.ae](https://mohre.gov.ae)
- Call centre: **600590000**

## Disclaimer

Hakk provides general information about workers' rights. It is not legal advice and does not create any lawyer-client relationship.
