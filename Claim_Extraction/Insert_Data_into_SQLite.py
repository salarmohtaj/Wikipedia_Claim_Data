import sqlite3
import pickle
import json
import os

data_dir = "Data"
json_filename = "Claims_JSON.LIST"

def insertVaribleIntoTable(journalid, text, wiki_label):
    try:
        sqliteConnection = sqlite3.connect('/home/salar/PycharmProjects/Wikipedia_Claim_Data/DjangoProject/crowdcheck/db.sqlite3')
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO webapp_sentences
                          (journal_id, sentence, wikilabel) 
                          VALUES (?, ?, ?);"""
        data_tuple = (journalid, text, wiki_label)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


with open(os.path.join(data_dir,json_filename),"rb") as tempfile:
    dic = pickle.load(tempfile)
for item in dic[:10]:
    id = item["id"]
    claims = item["claims"]
    non_claims = item["non_claims"]
    for s in claims:
        insertVaribleIntoTable(id , s , 1)
    for s in non_claims:
        insertVaribleIntoTable(id , s , 0)