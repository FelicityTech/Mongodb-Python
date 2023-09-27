# Connect to MongoDB cluster with MongoClient 
import os
import pprint

from dotenv import load_dotenv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


db = client.bank
account_collection = db.accounts

# calculate the balance in GBP, divide the original balance by the conversion rate
conversion_rate_usd_to_gbp = 1.3

# Select checking accounts with balance of more than $1,500

select_accounts = {"$match": {"account_type": "checking", "balance": {"$gt": 1500}}}

#organise documents in order from highest balance to lowest.
organize_by_original_balance = {"$sort": {"balance": -1}}

#Return only the account type & balance fields, plus a new field containing balance
return_specified_fields = {
    "$project": {
        "account_type": 1,
        "balance": 1,
        "gbp_balance": {"$divide": ["$balance", conversion_rate_usd_to_gbp]},
        "_id": 0
    }
}
 # Create an aggregation pipline containing the four stages created above
pipeline = [
     select_accounts,
     organize_by_original_balance,
     return_specified_fields,
 ]
 
 # Perform an aggregation on 'pipeline'.
results = account_collection.aggregate(pipeline)
 
print(
     "Account type original balance and balance in GDP of checking acounts with original balance greater than $1,500,"
     "in order from highest original balance to lowest to lowest: ", "\n"
 )
 
for item in results:
    pprint.pprint(item)
     
     
client.close()