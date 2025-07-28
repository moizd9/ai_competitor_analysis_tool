import streamlit as st
import pandas as pd
import time
from scraper import scrape_site_metadata
from gpt_engine import generate_swot_and_recommendations

st.set_page_config(page_title="AI Competitor Analyzer", layout="centered")

# ---- HEADER ----
st.title("🔍 AI Competitor Analyzer")
st.markdown("Compare your website against your competitors and get actionable insights.")

# ---- Inputs ----
st.header("🔗 Enter Your Website")
user_site = st.text_input("Your Website URL (e.g., https://yourcompany.com)", placeholder="https://example.com")

st.header("🖋️ Enter Competitor Websites")
comp1 = st.text_input("Competitor 1 URL", placeholder="https://competitor1.com")
comp2 = st.text_input("Competitor 2 URL", placeholder="https://competitor2.com")
comp3 = st.text_input("Competitor 3 URL", placeholder="https://competitor3.com")

# ---- Run Button ----
if st.button("🔎 Analyze"):
    if not user_site:
        st.error("Please enter your website URL.")
    else:
        st.success("URLs received. Starting analysis...")
        time.sleep(1)

        with st.spinner("🧠 Scraping your website..."):
            user_data = scrape_site_metadata(user_site)
            st.session_state["user_data"] = user_data
            st.session_state["user_url"] = user_site

        if comp1:
            with st.spinner("🧠 Scraping Competitor 1..."):
                comp1_data = scrape_site_metadata(comp1)
                st.session_state["comp1_data"] = comp1_data
                st.session_state["comp1_url"] = comp1

        if comp2:
            with st.spinner("🧠 Scraping Competitor 2..."):
                comp2_data = scrape_site_metadata(comp2)
                st.session_state["comp2_data"] = comp2_data
                st.session_state["comp2_url"] = comp2

        if comp3:
            with st.spinner("🧠 Scraping Competitor 3..."):
                comp3_data = scrape_site_metadata(comp3)
                st.session_state["comp3_data"] = comp3_data
                st.session_state["comp3_url"] = comp3

        st.success("✅ Scraping completed and debug print: done.")

# ---- Display Options ----
if "user_data" in st.session_state:
    st.markdown("### ✅ Analysis Ready")
    show_swot = st.checkbox("🧠 Show GPT SWOT & Recommendations")
    show_comparison = st.checkbox("📊 Show Side-by-Side Comparison")
    show_export = st.checkbox("📄 Export CSV")

    # ---- SWOT Analysis ----
    if show_swot:
        st.subheader("🧠 SWOT Analysis for Your Website")
        try:
            user_swot = generate_swot_and_recommendations(
                st.session_state["user_data"],
                st.secrets["OPENAI_API_KEY"]
            )
            st.markdown(user_swot)
        except Exception as e:
            st.error(f"Error generating GPT response for your website: {e}")

        for i in range(1, 4):
            comp_key = f"comp{i}_data"
            if comp_key in st.session_state:
                st.subheader(f"🧠 SWOT Analysis for Competitor {i}")
                try:
                    comp_swot = generate_swot_and_recommendations(
                        st.session_state[comp_key],
                        st.secrets["OPENAI_API_KEY"]
                    )
                    st.markdown(comp_swot)
                except Exception as e:
                    st.error(f"Error generating GPT response for Competitor {i}: {e}")

    # ---- Comparison Table ----
    if show_comparison:
        st.subheader("📊 SEO & UX Comparison Table")
        rows = [{
            "Website": "Your Website",
            "URL": st.session_state.get("user_url", ""),
            "Title": st.session_state["user_data"].get("title", ""),
            "Word Count": st.session_state["user_data"].get("word_count", 0),
            "Load Time (s)": st.session_state["user_data"].get("load_time", 0),
            "Missing Alt Tags": st.session_state["user_data"].get("missing_alt_count", 0),
            "Has Canonical": st.session_state["user_data"].get("has_canonical", False)
        }]

        for i in range(1, 4):
            comp_key = f"comp{i}_data"
            url_key = f"comp{i}_url"
            if comp_key in st.session_state:
                rows.append({
                    "Website": f"Competitor {i}",
                    "URL": st.session_state.get(url_key, ""),
                    "Title": st.session_state[comp_key].get("title", ""),
                    "Word Count": st.session_state[comp_key].get("word_count", 0),
                    "Load Time (s)": st.session_state[comp_key].get("load_time", 0),
                    "Missing Alt Tags": st.session_state[comp_key].get("missing_alt_count", 0),
                    "Has Canonical": st.session_state[comp_key].get("has_canonical", False)
                })

        df = pd.DataFrame(rows)
        st.dataframe(df)

    # ---- Export CSV ----
    if show_export:
        st.subheader("📄 Download Report")
        all_data = [st.session_state["user_data"]]
        for i in range(1, 4):
            comp_key = f"comp{i}_data"
            if comp_key in st.session_state:
                all_data.append(st.session_state[comp_key])

        df_export = pd.DataFrame(all_data)
        csv = df_export.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv, file_name="ai_competitor_analysis.csv", mime="text/csv")
