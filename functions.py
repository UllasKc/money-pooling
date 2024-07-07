import streamlit as st
import json
import bcrypt
import os
import pandas as pd
import datetime
registered_admin_users = ["ullas"]
registered_non_admin_users = ["vishwas","sahana","shashi","uppi"]

def add_to_pool(names, amount, date,comment="No Comments"):
    for name in names:
        st.session_state.pool_amount += amount
        st.session_state.friend_balance[name] += amount
        st.success(f"Added Rs.{amount:.2f} to {name}'s balance.")

    current_transaction = { "User" : st.session_state.email.capitalize(),
                            "Type":"Add Money",
                            "Pool Amount":st.session_state.pool_amount,
                            "Transaction":"+"+str(amount*len(names)),
                            'Vishwas': st.session_state.friend_balance["Vishwas"], 
                           'Sahana': st.session_state.friend_balance['Sahana'],
                            'Ullas': st.session_state.friend_balance['Ullas'],
                            'Shashi': st.session_state.friend_balance["Shashi"],
                            'Uppi': st.session_state.friend_balance["Uppi"],
                            'Date': str(date),
                            'Comments':comment}

    #Read
    with open("data.json", "r") as f:
        transactions = json.load(f)
    #append
    transactions.append(current_transaction)
    #Write 
    with open("data.json", "w") as f:
        json.dump(transactions, f)

# Function to use money from pool
def use_money(names, amount,date,comment="No Comments"):
    if amount <= st.session_state.pool_amount:
        st.session_state.pool_amount -= amount
        individual_amount_used = amount/len(names)
            
        for name in names:
            st.session_state.friend_balance[name] -= individual_amount_used
            st.success(f"Rs.{individual_amount_used:.2f} used by {name}.")

        current_transaction = { "User" : st.session_state.email.capitalize(),
                                "Type":"Use Money",
                                "Pool Amount":st.session_state.pool_amount,
                                "Transaction":"-"+str(amount),
                                'Vishwas': st.session_state.friend_balance["Vishwas"], 
                               'Sahana': st.session_state.friend_balance['Sahana'],
                                'Ullas': st.session_state.friend_balance['Ullas'],
                                'Shashi': st.session_state.friend_balance["Shashi"],
                                'Uppi': st.session_state.friend_balance["Uppi"],
                                'Date': str(date),
                                'Comments':comment}
        
        #Read
        with open("data.json", "r") as f:
            transactions = json.load(f)
        #append
        transactions.append(current_transaction)
        #Write 
        with open("data.json", "w") as f:
            json.dump(transactions, f)
    else:
        st.error("Not enough money in the pool.")

def initialize():
    with open("data.json", "r") as f:
        transactions = json.load(f)
    if transactions:
        data =  transactions[-1]  
        pool_amount = data["Pool Amount"]
        Vishwas =  data["Vishwas"]
        Sahana =  data["Sahana"]
        Ullas = data["Ullas"]
        Shashi = data["Shashi"]
        Uppi =  data["Uppi"]
    else:
        pool_amount = 0
        Vishwas =  0
        Sahana = 0
        Ullas = 0
        Shashi = 0
        Uppi = 0
    st.session_state.pool_amount = pool_amount
    st.session_state.friend_balance = {'Vishwas': Vishwas,'Sahana':Sahana, 'Ullas': Ullas, 
                                    'Shashi': Shashi, 'Uppi': Uppi}
    

# Function to display transactions
def upload_transactions():

    uploaded_file = st.file_uploader("Choose your transcation file")
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            actual_columns = ['User', 'Type', 'Pool Amount', 'Transaction', 'Vishwas','Sahana', 'Ullas',
                                    'Shashi', 'Uppi','Date', 'Comments']
            if df.columns.tolist() == actual_columns:
                df[['Pool Amount', 'Transaction']] = df[['Pool Amount', 'Transaction']].astype(int)
                df[['Vishwas','Sahana', 'Ullas','Shashi', 'Uppi']] = df[['Vishwas','Sahana', 'Ullas','Shashi', 'Uppi']].astype(float)
                df[['Date']] = df[['Date']].astype(str)
                df = df.fillna("Null")
                df = df.to_dict(orient='records')
                with open("data.json", "w") as f:
                    json.dump(df, f)
                initialize()
            else:
                st.error("Upload the correct transactions file")
    except:
        st.error("corrupt transactions file")


# Function to display transactions
def display_transactions():
    with open("data.json", "r") as file:
        transactions = json.load(file)

    data = pd.DataFrame(data=transactions)
    csv_data = data.to_csv(index=False).encode('utf-8')
    st.download_button(
    "Download as CSV",
    csv_data,
    "data.csv",
    "text/csv",
    key='download-csv',
    type="primary"
    )
    st.table(transactions)

def get_data():
    with open("data.json", "r") as file:
        transactions = json.load(file)
    return transactions
                   
def revert_last_transaction():
    #Read
    with open("data.json", "r") as f:
        transactions = json.load(f)
    #update
    if transactions:
        last_transaction =  transactions[-1]
        last_transaction_user = last_transaction["User"].lower()
        if st.session_state.email in registered_non_admin_users and last_transaction_user in registered_admin_users:
            st.error(f'Sorry {st.session_state.email.capitalize()}, You can not delete the transaction made by {last_transaction_user.capitalize()}')
        else:
            transactions.pop()  
            st.success(f"Last transaction reverted")
    else:
        st.error("No Transactions in the Database")
    #Write 
    with open("data.json", "w") as f:
        json.dump(transactions, f)

def reset_all_transactions():
    with open("data.json", "w") as f:
        json.dump([], f)

def display_balance():
    # Display total available balance
    total_balance = sum(st.session_state.friend_balance.values())
    st.header("Total Available Balance")
    st.write(f"Rs.{total_balance:.2f}")

    # Display individual balances
    st.header("Individual Balances")
    for friend, balance in st.session_state.friend_balance.items():
        st.write(f"{friend}: Rs.{balance:.2f}")

def validate_password(entered_password, hashed_password):
    # Check if the entered password matches the hashed password
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def json_file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path) and file_path.endswith('.json')

def main():

    if 'pool_amount' not in st.session_state:
        initialize()
    # Sidebar for adding and using money
    st.sidebar.title("Actions")
    option = st.sidebar.selectbox("Choose an action:", ["Add Money to Pool", "Use Money from Pool","Transactions"])

    if option == "Add Money to Pool":
        names = st.sidebar.multiselect("Select friends to add money:", ['Vishwas','Sahana', 'Ullas', 'Shashi', 'Uppi'], default=['Ullas'])
        amount = st.sidebar.number_input("Enter amount to add to selected friends:", min_value=10, step=500)
        date = st.sidebar.date_input("Enter recharge date:", value="default_value_today",format="DD/MM/YYYY")
        comment = st.sidebar.text_input(placeholder="Enter comments",label="Enter Comments")
        if st.sidebar.button("Add"):
            add_to_pool(names, amount,date,comment)
        display_balance()

    elif option == "Use Money from Pool":
        names = st.sidebar.multiselect("Select friends who used the money:", ['Vishwas','Sahana', 'Ullas', 'Shashi', 'Uppi'], default=['Ullas'])
        amount = st.sidebar.number_input("Enter amount used by selected friends:", min_value=10, step=500)
        date = st.sidebar.date_input("Enter match played date:", value="default_value_today",format="DD/MM/YYYY")
        comment = st.sidebar.text_input(placeholder="Enter comments",label="Enter Comments")
        if st.sidebar.button("Use"):
            use_money(names, amount,date,comment)
        display_balance()

    elif option == "Transactions":
        st.header("Transaction History")
        if st.session_state.email in registered_admin_users:
            upload_transactions()
            if st.button("Revert last transaction",type="primary"):
                revert_last_transaction()
                initialize()
            if st.button("Reset all transactions",type="primary"):
                reset_all_transactions()
                initialize()
                st.success(f"All transactions deleted")
        else:
            if st.button("Revert last transaction",type="primary"):
                revert_last_transaction()
                initialize()
        display_transactions()
