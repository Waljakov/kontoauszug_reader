#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# kontoauszug_reader
# Mit diesem Script sollen kontoauszüge eingelesen werden können 
# um Ein- und Ausgehendes Geld mit Tags einzuordnen und entsprechend darzustellen

import pandas as pd
pd.set_option("display.max_colwidth", 10000)
import numpy as np
import matplotlib.pyplot as plt
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
date_start = ""
date_end = ""
tags = ["essen", "fixkosten", "paypal", "amazon"]
if date_start == "":
    date_start = df[date_col].min()
else:
    date_start = pd.to_datetime(date_start, format=dateformat) 
if date_end == "":
    date_end = df[date_col].max()
else: 
    date_end = pd.to_datetime(date_end, format=dateformat) 
filtered = filter(df, date_col, date_start, date_end, tags)
UmsatzByTags=[]
for item in tags:
    UmsatzByTags.append(np.abs(filtered.loc[filtered["tags"].str.contains(item), sales_col].sum()))
print(UmsatzByTags)
plot_df= pd.DataFrame({ sales_col: UmsatzByTags }, index=[tags])

# Pie Chart
plt.xkcd()
ax =plot_df.plot(y=sales_col, labels=tags, kind="pie", autopct="%1.1f%%", figsize=(5,5))
ax.set_ylabel("")
ax.set_title("Ausgaben " + date_start.strftime("%d.%m.%Y") + " - " + date_end.strftime("%d.%m.%Y"))
ax.get_legend().remove()
plt.show()
