import streamlit as st
from datetime import date
from database import initialize_database, add_transaction, add_income, add_ebt_refill, get_all_transactions
from calculations import (
    get_ebt_remaining,
    get_personal_budget_remaining,
    get_personal_budget_limit,
    get_personal_budget_used_pct,
    can_go_out_tonight,
    MONTHLY_INCOME,
    EBT_MONTHLY_BENEFIT
)

# ── Initialize ────────────────────────────────────────────────────────────────
initialize_database()
# Safe to call every time — only creates tables if they don't exist

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Finance Dashboard", page_icon="💰")
# This must be the first Streamlit command — sets the browser tab title and icon

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💰 Finance Dashboard")
st.caption(f"Monthly income: ${MONTHLY_INCOME} | Personal budget: ${get_personal_budget_limit()}")
# st.caption renders smaller grey text — good for secondary info

# ── Metric cards ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
# st.columns splits the page into side by side sections
# col1, col2, col3 are each their own container you write into

with col1:
    st.metric(
        label="EBT Remaining",
        value=f"${get_ebt_remaining()}"
    )

with col2:
    remaining = get_personal_budget_remaining()
    st.metric(
        label="Personal Budget Left",
        value=f"${remaining}",
        delta=f"{get_personal_budget_used_pct()}% used"
    )
    # delta shows a secondary value below the main number
    # Streamlit colors it green if positive, red if negative

with col3:
    answer = can_go_out_tonight()
    st.metric(
        label="Go Out Tonight?",
        value="✅ Yes" if answer else "❌ No"
    )
    # This is a ternary expression — a one line if/else
    # Read it as: "Yes if answer is True, otherwise No"

# ── Divider ───────────────────────────────────────────────────────────────────
st.divider()

# ── Add transaction form ──────────────────────────────────────────────────────
st.subheader("Add Transaction")

with st.form("transaction_form"):
    # st.form groups inputs together so Streamlit only reruns when Save is clicked
    # Without a form, it would rerun on every keystroke

    col_a, col_b = st.columns(2)

    with col_a:
        txn_date = st.date_input("Date", value=date.today())
        txn_amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)

    with col_b:
        txn_category = st.selectbox("Category", ["EBT", "personal"])
        txn_description = st.text_input("Description (optional)")

    submitted = st.form_submit_button("Save Transaction")

    if submitted:
        add_transaction(
            date=str(txn_date),
            amount=txn_amount,
            category=txn_category,
            description=txn_description
        )
        st.success("Transaction saved!")
        # st.success shows a green confirmation banner
# ── Log income form ───────────────────────────────────────────────────────────
st.divider()
st.subheader("Log Income")

with st.form("income_form"):
    inc_date = st.date_input("Date", value=date.today())
    inc_amount = st.number_input("Amount ($)", min_value = 0.01, step = 0.01)
    
    submitted = st.form_submit_button("Save Income")

    if submitted:
        add_income(
            pay_date = str(inc_date),
            amount = inc_amount
        )
        st.success("Income saved!")
# ── Log EBT Refill Form ───────────────────────────────────────────────────────────
st.divider()
st.subheader("EBT Refill")

with st.form("ebt_refill"):
    ref_date = st.date_input("Date", value=date.today())
    ref_amount = st.number_input("Amount ($)", min_value = 0.01, step = 0.01, value = float(EBT_MONTHLY_BENEFIT))

    submitted = st.form_submit_button("Save EBT Refill")

    if submitted:
        add_ebt_refill(
            refill_date = str(ref_date),
            amount = ref_amount
        )
        st.success("EBT Refill Saved!")

# ── Transaction history ───────────────────────────────────────────────────────
st.divider()
st.subheader("Transaction History")

transactions = get_all_transactions()

if transactions:
    st.dataframe(
        data=transactions,
        column_config={
            0: "Date",
            1: "Amount ($)",
            2: "Category",
            3: "Description"
        },
        use_container_width=True
    )
    # st.dataframe renders an interactive sortable table
    # column_config lets you rename the columns from their index numbers
else:
    st.info("No transactions yet — add one above!")
    # st.info shows a neutral blue info banner


