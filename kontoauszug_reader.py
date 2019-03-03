#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# kontoauszug_reader
# Mit diesem Script sollen kontoauszüge eingelesen werden können 
# um Ein- und Ausgehendes Geld mit Tags einzuordnen und entsprechend darzustellen

import pandas as pd
import numpy as np
from functions import *

# Variables
kontoauszug_path = "./kontoauszuege/umsaetze-325794-2019-03-02-16-34-32.csv"
start_row = 6 # int; first column to read in
separator = ";"
searchIndicator = "Verwendungszweck" # str; search this column for indicators to set tags
date_col = "Buchungstag" # str; this is the importatant date column
dateformat = "%d.%m.%Y" # str; specify how the date is formatted
drop_cols = ["Wertstellungstag"] # str-array; unimportand columns that will be deleted
sales_col = "Umsatz" # str; column containing sales
indicators = {
    "essen" : ["nahkauf", "Schmaelzle", "Alnatura", "SCHECK-IN"],
    "handy" : ["1u1 Telecom GmbH"],
    "paypal": ["Paypal"],
    "amazon": ["AMAZON"],
    "geldabheben" : ["KARTE 100041520", "KARTE 100038090"],
    "fixkosten" : ["1u1 Telecom GmbH", "Kontaktlinsen", "WOHNUNG", "Katzenversicherung", "Techniker Krankenkasse"]
}

# Prepare Dataframe
df = pd.read_csv(kontoauszug_path, sep=separator, header=start_row, index_col=False, skipfooter=1, engine="python")
df.drop(columns = drop_cols, inplace=True)
df[date_col] = pd.to_datetime(df[date_col],format=dateformat)
df[sales_col].replace({"\." : ""}, inplace=True, regex=True)
df[sales_col].replace({"," : "."}, inplace=True, regex=True)
df[sales_col] = df[sales_col].astype(float)
df["tags"] = "" 
for key,val in indicators.items():
    addTag(df, key, val, searchIndicator)

# Filter
filtered = filter(df, date_col, "2019-02-01","2019-02-28", ["essen", "fixkosten"])
pd.set_option("display.max_colwidth", 10000)
print(filtered.loc[:,[date_col, sales_col, "tags"]].to_string)
print("Summe: " + filtered[sales_col].sum().astype(str) + "EUR")
