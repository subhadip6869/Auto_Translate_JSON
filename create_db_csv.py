import pandas as pd
import json

supported = json.load(open("supported_flutter_google.json", "r", encoding="utf8"))
db_table = []

for k, v in supported.items():
    obj = {
        "LANGUAGE": v,
        "LANGUAGE_CODE": k
    }
    db_table.append(obj)

df = pd.DataFrame(db_table)

df.to_csv("Language.csv", index=False)