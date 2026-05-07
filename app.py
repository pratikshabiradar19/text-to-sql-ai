import streamlit as st
import subprocess
subprocess.run(["python", "database.py"])
from sql_chain import ask

st.set_page_config(
    page_title="Text-to-SQL AI Assistant",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Text-to-SQL AI Assistant")
st.markdown("**Ask any question in plain English — get database results instantly.**")
st.markdown("No SQL knowledge needed!")

with st.sidebar:
    st.header("📋 Try these questions")
    st.markdown("Click any question to auto-fill it:")

    examples = [
        "Show all customers from Pune",
        "Which product is the most expensive?",
        "Total revenue from each city",
        "Which customer spent the most money?",
        "Show all orders placed in January 2024",
        "List all Electronics products",
        "How many orders does each customer have?",
        "Show top 3 products by total quantity sold",
        "What is the average order value?",
        "Show all orders above 50000 rupees",
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.question = example

    st.divider()
    st.markdown("**Database contains:**")
    st.markdown("- 7 Customers")
    st.markdown("- 8 Products")
    st.markdown("- 15 Orders")
    st.markdown("- 3 Categories: Electronics, Footwear, Clothing")

if "history" not in st.session_state:
    st.session_state.history = []
if "question" not in st.session_state:
    st.session_state.question = ""

col1, col2 = st.columns([4, 1])

with col1:
    question = st.text_input(
        "Type your question here:",
        value=st.session_state.question,
        placeholder="e.g. Show me all customers from Mumbai"
    )

with col2:
    run_button = st.button("🔍 Run Query", type="primary", use_container_width=True)

st.divider()

if run_button and question:
    with st.spinner("Generating SQL query and fetching results..."):
        sql, df, error = ask(question)

    st.subheader("Generated SQL Query")
    st.code(sql, language="sql")

    if error:
        st.error(f"Error running query: {error}")
        st.info("Try rephrasing your question and run again.")

    elif df is not None and not df.empty:
        st.subheader(f"Results — {len(df)} rows found")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download results as CSV",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv"
        )

        st.session_state.history.append({
            "question": question,
            "sql": sql,
            "rows": len(df)
        })

        st.session_state.question = ""

    else:
        st.warning("No results found. Try a different question.")

elif run_button and not question:
    st.warning("Please type a question first!")

if st.session_state.history:
    st.divider()
    st.subheader("📜 Your Query History")

    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {item['question']} — {item['rows']} rows"):
            st.code(item["sql"], language="sql")