import os
import pprint

from dotenv import load_dotenv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
my_wc_majority = WriteConcern('majority', wtimeout=1000)

# step 0: Create collections, if they don't already exist.
# CRUD operations in transactions must be on existing collections.

client.get_database('webshop', write_concern=my_wc_majority).orders.insert_one(
    {"sku": "abc123", "qty": 0})

client.get_database("webshop", write_concern=my_wc_majority).inventory.insert_one(
    {"sku": "abc123", "qty": 1000})

# step 1: Define the operations and their sequence within the transaction


def update_orders_and_inventory(my_session):
    orders = session.client.webshop.orders
    inventory = session.client.webshop.inventory
    with session.start_transaction(
            read_concern=ReadConcern("snapshot"),
            write_concern=WriteConcern(w="majority"),
            read_preference=ReadPreference.PRIMARY):
        orders.insert_one({"sku": "abc123", "qty": 100}, session=my_session)
        commit_with_retry(my_session)

# step 2: Attempt to run and commit transaction with retry logic


def commit_with_retry(session):
    while True:
        try:
            # Commit uses write concern set at transaction start.
            session.commit_transaction()
            print("Transaction committed.")
            break
        except (ConnectionFailure, OperationFailure) as exc:
            # Can retry commit
            if exc.has_error_label("UnknownTransactionCommitResult"):
                print("UnknownTransactionCommitResult, retrying commit operation ...")
                continue
            else:
                print("Error during commit ...")
                raise


# step 3: Attempt with retry logic to run the transaction function txn_func
def run_transaction_with_retry(txt_func, session):
    while True:
        try:
            txn_func(session)  # performs transaction
            break
        except (ConnectionFailure, OperationFailure) as exc:
            # If transient error, retry the whole transaction
            if exc.has_error_label("TransientTransactionError"):
                print("TransientTransactionError, retrying transaction ...")
                continue
            else:

                raise


# step 4: Start a session.
with client.start_session() as my_session:

    # Step 5: Call the function 'run_transaction_with_retry' passing it the function
    # to call 'update_orders_and_inventory' and the session 'my_session' to associate with this transaction

    try:
        run_transaction_with_retry(update_orders_and_inventory, my_session)
    except Exception as exc:
        # do something with error. The error handling code is not
        print("Error")
        # implemented for you with the Core API
    raise
