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
kontoauszug_path = "./kontoauszuege/umsaetze-325794-2019-07-19-00-36-56.csv"
start_row = 6 # int; first column to read in
separator = ";"
searchIndicator = "Verwendungszweck" # str; search this column for indicators to set tags
date_col = "Buchungstag" # str; this is the importatant date column
dateformat = "%d.%m.%Y" # str; specify how the date is formatted
drop_cols = ["Wertstellungstag"] # str-array; unimportand columns that will be deleted
sales_col = "Umsatz" # str; column containing sales
indicators = {
    "essen" : ["nahkauf", "lidl", "unverpackt", "edeka", "Schmaelzle", "aldi", "Alnatura", "SCHECK-IN", "real", "studierendenwerk karlsruhe", "rewe", "STREB WEIN- UND GETRAENKE"],
    "kleidung" : ["Karstadt sports gmbh", "p+c", "reno", "basislager", "h+m", "decathlon"],
    "stadtmobil" : ["stadtmobil Carsharing GmbH"],
    "paypal": ["Paypal"],
    "katzen": ["Fressnapf"],
    "amazon": ["AMAZON"],
    "geldabheben" : ["KARTE "],
    "fixkosten" : ["1u1 Telecom GmbH", "Kontaktlinsen", "spotify",  "WOHNUNG", "Katzenversicherung", "Techniker Krankenkasse"]
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
df.loc[df[sales_col] > 0, "tags"] += " " + "einnahmen"
df.loc[df["tags"] == "", "tags"] += " " + "sonstiges"
df.loc[df[sales_col] < 0, "tags"] += " " + "ausgaben"

# Filter
date_start = "26.06.2019"
date_end = ""
tags = ["essen", "kleidung", "katzen",  "stadtmobil", "fixkosten", "paypal", "amazon",  "geldabheben", "sonstiges"]
if date_start == "":
    date_start = df[date_col].min()
else:
    date_start = pd.to_datetime(date_start, format=dateformat) 
if date_end == "":
    date_end = df[date_col].max()
else: 
    date_end = pd.to_datetime(date_end, format=dateformat) 
filtered = filter(df, date_col, date_start, date_end)
UmsatzByTags=[]
for item in tags:
    UmsatzByTags.append(np.abs(filtered.loc[filtered["tags"].str.contains(item), sales_col].sum()))
UmsatzByTags.append(filtered.loc[filtered["tags"].str.contains("einnahmen"), sales_col].sum() + filtered.loc[filtered["tags"].str.contains("ausgaben"), sales_col].sum())
tags.append("gewinn")
plot_df= pd.DataFrame({ sales_col: UmsatzByTags }, index=[tags])
print(plot_df.sort_values(sales_col))
print("-------------------------")
print("Gesamtausgaben  " + (-1*filtered.loc[filtered["tags"].str.contains("ausgaben"), sales_col].sum()).astype(str))

Sonstiges_verwendung = filtered["tags"].str.contains("sonstiges")
print("\nFolgende Umsätze befinden sich in Sonstiges:")
print(filtered.loc[Sonstiges_verwendung, searchIndicator].str[:50] + "..." + "                    " + filtered.loc[Sonstiges_verwendung, sales_col].astype(str))
print("\n")
print("-------------------------")

# Pie Chart
if plot_df.loc["gewinn", sales_col].item() < 0: # dont show "gewinn" if negative
    plot_df=plot_df.drop(["gewinn"])
plt.xkcd()
ax =plot_df.plot(y=sales_col, labels=tags, kind="pie", autopct="%1.1f%%", figsize=(5,5))
ax.set_ylabel("")
ax.set_title("Ausgaben " + date_start.strftime("%d.%m.%Y") + " - " + date_end.strftime("%d.%m.%Y"))
ax.get_legend().remove()
plt.show()
