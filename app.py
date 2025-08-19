import streamlit as st
from app.generator import generate_cold_email, get_llm
from app.scraper import scrape_text_from_url
from app.utils import get_env
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Cold Email Gen", layout="centered")

st.title("Cold Email Generator -> RAG + Local LLM (Ollama)")

st.markdown("""
Enter the job/apply URL and a few details — the app scrapes the page, stores job text locally,
retrieves relevant parts, and generates a tailored cold email using a local LLM.
""")

with st.form("email_form"):
    url = st.text_input("Apply / Job URL", placeholder="https://company.com/careers/job-123")
    name = st.text_input("Your full name", placeholder="Uday Kumar")
    role = st.text_input("Target role / position", placeholder="Software Engineer Intern")
    portfolio = st.text_area("Portfolio links (comma separated)", placeholder="https://github.com/..., https://your-site.com")
    tone = st.selectbox("Tone", ["professional", "friendly", "concise", "enthusiastic"])
    reindex = st.checkbox("Force re-scrape & reindex (use if page changed)", value=False)
    submit = st.form_submit_button("Generate cold email")

if submit:
    if not url.strip():
        st.error("Please provide a URL.")
    else:
        with st.spinner("Scraping and generating..."):
            try:
                # optional quick preview of scraped text (inside an expander)
                txt = scrape_text_from_url(url)
                with st.expander("Preview: extracted page text (truncated)", expanded=False):
                    # show a truncated preview inside the expander
                    preview_text = txt[:3000] + ("..." if len(txt) > 3000 else "")
                    st.text(preview_text)

                email = generate_cold_email(url=url, name=name, role=role, portfolio_links=portfolio, tone=tone)
                st.subheader("Generated cold email")
                st.code(email)
                st.success("Copy and send! Edit before sending to customize further.")
            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Common fixes: ensure Ollama is running (`ollama serve`) and you pulled a model (e.g. `ollama pull llama3`).")
