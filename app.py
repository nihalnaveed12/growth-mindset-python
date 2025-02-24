import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.title("Expense Tracker App")

# Initialize expenses list in session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Sidebar for Budget Setting
st.sidebar.write("### Set Monthly Budget")
budget = st.sidebar.number_input("Enter your monthly budget", min_value=0.0, format="%.2f")

# Form for adding expenses
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.text_input("Category (e.g., Food, Transport)")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submit_button = st.form_submit_button("Add Expense")

    if submit_button:
        expense = {"Date": date, "Category": category, "Amount": amount}
        st.session_state.expenses.append(expense)
        st.success("Expense added successfully!")

# Display expenses in a table
if st.session_state.expenses:
    st.write("### Your Expenses")
    expenses_df = pd.DataFrame(st.session_state.expenses)
    st.table(expenses_df)

    # Feature 1: Expense Delete Karne Ka Option
    st.write("### Delete Expenses")
    for i, expense in enumerate(st.session_state.expenses):
        if st.button(f"Delete Expense {i + 1}"):
            st.session_state.expenses.pop(i)
            st.success(f"Expense {i + 1} deleted successfully!")
            st.rerun()

    # Feature 2: Monthly Summary
    st.write("### Monthly Summary")
    expenses_df["Month"] = pd.to_datetime(expenses_df["Date"]).dt.to_period("M")
    monthly_summary = expenses_df.groupby("Month")["Amount"].sum().reset_index()
    st.table(monthly_summary)

    # Feature 3: Expense Filter Karne Ka Option
    st.write("### Filter Expenses")
    filter_option = st.selectbox("Filter by", ["All", "Category", "Month"])
    
    if filter_option == "Category":
        categories = expenses_df["Category"].unique()
        selected_category = st.selectbox("Select Category", categories)
        filtered_df = expenses_df[expenses_df["Category"] == selected_category]
    elif filter_option == "Month":
        months = expenses_df["Month"].unique()
        selected_month = st.selectbox("Select Month", months)
        filtered_df = expenses_df[expenses_df["Month"] == selected_month]
    else:
        filtered_df = expenses_df

    st.write("### Filtered Expenses")
    st.table(filtered_df)

    # Feature 4: Budget Setting and Alerts
    if budget > 0:
        total_expenses = expenses_df["Amount"].sum()
        remaining_budget = budget - total_expenses
        st.write(f"### Remaining Budget: ₹{remaining_budget:.2f}")
        if remaining_budget < 0:
            st.error("You have exceeded your monthly budget!")
        else:
            st.success("You are within your budget!")

    # Visualize expenses by category (Pie Chart)
    st.write("### Expenses by Category (Pie Chart)")
    category_summary = expenses_df.groupby("Category")["Amount"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(category_summary["Amount"], labels=category_summary["Category"], autopct="%1.1f%%")
    st.pyplot(fig)