import streamlit as st
import json
import random
import datetime
import pandas as pd

st.set_page_config(page_title="Bank Account Management System", page_icon="🏦")

st.header("🏦 Bank Account Management System")

class BankAccount:
    def __init__(self):
       pass


    def create_account(self, name, password, balance=0):

        with open("accounts.json", "r") as file:
            accounts = json.load(file)
        
        id = str(random.randint(10000000, 999999999999))
        new_account = {
            'id': id,
            'name': name,
            'password': password,
            'balance': balance
        }

        accounts.append(new_account)
        st.session_state.accounts = accounts
        st.session_state.page = "main"
        st.session_state.current_user = name

        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)


    def deposit(self, amount):

        with open("accounts.json", "r") as file:
            accounts = json.load(file)

        for account in accounts:
            if account['name'] == st.session_state.current_user:
                account['balance'] += amount
                updated_balance = account["balance"]
                break

        st.session_state.accounts = accounts
        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)

        return updated_balance


    def withdraw(self, amount):
        with open("accounts.json", "r") as file:
            accounts = json.load(file)

        for account in accounts:
            if account['name'] == st.session_state.current_user:
                account['balance'] -= amount
                updated_balance = account["balance"]
                break

        st.session_state.accounts = accounts
        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)

        return updated_balance


    def transfer(self, recipient_id, amount):

        with open("accounts.json", "r") as file:
            accounts = json.load(file)

        sender_account = next((acc for acc in accounts if acc["name"] == st.session_state.current_user), None)
        recipient_account = next((acc for acc in accounts if str(acc["id"]) == recipient_id), None)
        
        if sender_account and recipient_account:
            sender_account['balance'] -= amount
            recipient_account['balance'] += amount

        st.session_state.accounts = accounts
        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)

        return sender_account['balance']


    def transaction_history(self, history: dict):
        
        with open("transaction_history.json", "r") as file:
            histories = json.load(file)

        histories.append(history)

        with open("transaction_history.json", "w") as file:
            json.dump(histories, file, indent=4)


bank = BankAccount()


if "page" not in st.session_state:
    st.session_state.page = "create_account"

if "show_form" not in st.session_state:
    st.session_state.show_form = False

with open("accounts.json", "r") as file:
    st.session_state.accounts = json.load(file)

if "current_user" not in st.session_state:
    st.session_state.current_user = None


if st.session_state.page == "create_account":

    col1, col2 = st.columns(2, gap="large", width=1000)

    with col1:
        if st.button("🆕 Create Account"):
            st.session_state.show_form = True
            st.session_state.form_type = "create"
            st.rerun()
    
    with col2:
        if st.button("🔐 Login"):
            st.session_state.show_form = True
            st.session_state.form_type = "login"
            st.rerun()
    

    if st.session_state.show_form:
        if st.session_state.form_type == "login":
            st.write("### Login to Your Account")
            with st.form(key="login_form"):
                name = st.text_input("Name:")
                password = st.text_input("Password:", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    user_account = next((acc for acc in st.session_state.accounts
                                         if acc["name"] == name and acc["password"] == password), None)
                    if user_account:
                        st.success(f"Welcome back, {name}!")
                        st.session_state.page = "main"
                        st.session_state.current_user = name
                        st.session_state.show_form = False
                        st.rerun()
                    else:
                        st.error("Invalid name or password.")


        elif st.session_state.form_type == "create":
            st.write("### Create a New Account")
            with st.form(key="create_form"):
                name = st.text_input("Name:")
                password = st.text_input("Password:", type="password")
                balance = st.number_input("Initial Balance:", min_value=0.0, step=500.0)
                submitted = st.form_submit_button("Create Account")
                if submitted:
                    if name and password:
                        user_account = next((acc for acc in st.session_state.accounts
                                             if acc["name"] == name), None)
                        if not user_account:
                            bank.create_account(name, password, balance)
                            st.success(f"Account created for {name} with balance {balance:.2f}PKR!")
                            st.session_state.show_form = False
                            st.rerun()
                        else:
                            st.error("Account already exists with this name.")
                    else:
                        st.warning("Please fill in all required fields!")

    st.write("---")


elif st.session_state.page == "main":

    if "sub_page" not in st.session_state:
        st.session_state.sub_page = "home"


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏠 Home"):
            st.session_state.sub_page = "home"
            st.rerun()

    with col2:
        if st.button("💰 Deposit"):
            st.session_state.sub_page = "deposit"
            st.rerun()

    with col3:
        if st.button("💸 Withdraw"):
            st.session_state.sub_page = "withdraw"
            st.rerun()

    with col4:
        if st.button("🔄 Transfer"):
            st.session_state.sub_page = "transfer"
            st.rerun()

    st.sidebar.title("Navigation")
    if st.sidebar.button("📜 Transaction History", width=200):
        st.session_state.sub_page = "history"
        st.rerun()
    if st.sidebar.button("⚙️ Account Settings", width=200):
        st.session_state.sub_page = "settings"
        st.rerun()

    st.write("---")


    if st.session_state.sub_page == "home":
        st.title(f"Welcome, {st.session_state.current_user}")
        st.write("### Account Dashboard")

        user_account = next((acc for acc in st.session_state.accounts
                             if acc["name"] == st.session_state.current_user), None)
        if user_account['name'] == st.session_state.current_user:
            st.write(f"**Account ID:** {user_account['id']}")
            st.write(f"**Name:** {user_account['name']}")
            st.info(f"**Balance: {user_account['balance']:,.2f}PKR**")


    elif st.session_state.sub_page == "deposit":
        st.title("💰Deposit Money")
        st.write("### Add money to your account")

        with st.form("deposit_form"):
            deposit_amount = st.number_input(
                "Enter amount to deposit:", min_value=100.0, step=100.0)
            password = st.text_input("Enter your password:", type="password")
            deposit_submitted = st.form_submit_button("Deposit")

            if deposit_submitted:
                if password:
                    user_account = next((acc for acc in st.session_state.accounts
                                        if acc["name"] == st.session_state.current_user and acc["password"] == password), None)

                    if user_account:

                        history = {
                            "account_id": user_account["id"],
                            "recipient_id": None,
                            "type": "Deposit",
                            "amount": deposit_amount,
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "Success"
                        }

                        bank.transaction_history(history)
                        new_balance1 = bank.deposit(deposit_amount)
                        st.success(
                            f"✅ Successfully deposited {deposit_amount:.2f}PKR!")
                        st.success(
                            f"New balance: {new_balance1:.2f}PKR")
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("Password is required")


    elif st.session_state.sub_page == "withdraw":
        st.title("💸Withdraw Money")
        with st.form("withdraw_form"):
            deposit_amount = st.number_input(
                "Enter amount to withdraw:", min_value=100.0, step=100.0)
            password = st.text_input("Enter your password:", type="password")
            deposit_submitted = st.form_submit_button("Withdraw")

            if deposit_submitted:
                if password:
                    user_account = next((acc for acc in st.session_state.accounts
                                        if acc["name"] == st.session_state.current_user and acc["password"] == password), None)

                    if user_account:
                        if user_account['balance'] >= deposit_amount:
                            history = {
                                "account_id": user_account["id"],
                                "recipient_id": None,
                                "type": "Withdraw",
                                "amount": deposit_amount,
                                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status": "Success"
                            }
                            bank.transaction_history(history)
                            new_balance2 = bank.withdraw(deposit_amount)
                            st.success(
                                f"✅ Successfully Withdraw {deposit_amount:.2f}PKR!")
                            st.success(
                                f"New balance: {new_balance2:.2f}PKR")
                        else:
                            st.error("Insufficient funds")
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("Password is required")


    elif st.session_state.sub_page == "transfer":
        st.title("🔄Transfer Money")
        with st.form("transfer_form"):
            recipient_id = st.text_input("Recipient ID")
            transfer_amount = st.number_input(
                "Enter amount to transfer:", min_value=100.0, step=100.0)
            password = st.text_input("Enter your password:", type="password")
            transfer_submitted = st.form_submit_button("Transfer")

            if transfer_submitted:
                if recipient_id and password:
                    sender_account = next((acc for acc in st.session_state.accounts
                                           if acc["name"] == st.session_state.current_user and acc["password"] == password), None)
                    recipient_account = next((acc for acc in st.session_state.accounts
                                              if str(acc["id"]) == recipient_id), None)

                    if sender_account and recipient_account:
                        if sender_account['balance'] >= transfer_amount:
                            history = {
                                "account_id": sender_account["id"],
                                "recipient_id": recipient_account["id"],
                                "type": "Transfer",
                                "amount": transfer_amount,
                                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status": "Success"
                            }
                            bank.transaction_history(history)
                            new_balance3 = bank.transfer(recipient_id, transfer_amount)
                            st.success(f"✅ Successfully transferred {transfer_amount:.2f}PKR to {recipient_account['name']}!")
                            st.success(f"New balance: {new_balance3:.2f}PKR")
                        else:
                            st.error("Insufficient funds")
                    else:
                        st.error("Invalid recipient ID or password.")
                else:
                    st.error("Recipient ID and Password are required")


    elif st.session_state.sub_page == "history":
        st.title("📜 Your Transaction History")

        with open("transaction_history.json", "r") as file:
            histories = json.load(file)
        
        df = pd.DataFrame(histories)

        user_account = next((acc for acc in st.session_state.accounts
                             if acc["name"] == st.session_state.current_user), None)
        user_histories = df[df['account_id'] == user_account['id']]
        st.dataframe(user_histories, width="stretch")
        
       
    elif st.session_state.sub_page == "settings":
        st.title("⚙️ Account Settings")
        user_account = next((acc for acc in st.session_state.accounts
                             if acc["name"] == st.session_state.current_user), None)
        st.subheader("Account Information")
        st.write(f"**Account ID:** {user_account['id']}")
        st.write(f"**Name:** {user_account['name']}")
        st.write(f"**Balance:** {user_account['balance']:,.2f}PKR")
        st.write("")
        st.write("")

        with st.expander("Change Password"):
          with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                password_submitted = st.form_submit_button("Change Password")

                if password_submitted:
                    if current_password and new_password and confirm_password:
                        if current_password == user_account["password"]:
                            if new_password == confirm_password:
                                user_account["password"] = new_password
                                with open("accounts.json", "w") as file:
                                    json.dump(st.session_state.accounts, file, indent=4)
                                st.success("Password changed successfully!")
                            else:
                                st.error("New passwords do not match.")
                        else:
                            st.error("Current password is incorrect.")
                    else:
                        st.error("All fields are required.")

        st.write("")
        st.write("")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔒 Logout", type="secondary", width=200):
                st.session_state.page = "create_account"
                st.session_state.show_form = False
                st.session_state.current_user = None
                st.session_state.sub_page = "home"
                st.rerun()

        with col2:
            if st.button("❌ Delete Account", type="secondary", width=200):
                st.session_state.accounts = [acc for acc in st.session_state.accounts
                                            if acc["name"] != st.session_state.current_user]
                with open("accounts.json", "w") as file:
                    json.dump(st.session_state.accounts, file, indent=4)
                st.success("Account deleted successfully.")
                st.session_state.page = "create_account"
                st.session_state.show_form = False
                st.session_state.current_user = None
                st.session_state.sub_page = "home"
                st.rerun()

