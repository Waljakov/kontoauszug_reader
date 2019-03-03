#!/usr/bin/env python
# -*- coding: utf-8 -*-



# df: Dataframe;    tagname: str  
# indicator: str-array;    searchColumn: str - name of column which contains indicators
def addTag(df, tagname, indicator, searchColumn):
    for i in range(0, len(indicator)):
        indicator_found = df[searchColumn].str.contains(indicator[i], False);
        for i in range(0, len(indicator_found)):
            if indicator_found[i]:
                df.loc[i, "tags"] += " " + tagname
    return df


# df: Dataframe;    date_col: str - columname containing the date
# datestart, dateend: date;   tags: str-array
def filter(df, date_col="", datestart="", dateend="", tags=[""]):
    results = df
    if date_col!="":
        if datestart!="": 
            results = results[(results[date_col] >= datestart)]
        if dateend!="":
            results = results[(results[date_col] <= dateend)]
    if tags[0]!="":
        results = results[results["tags"].str.contains('|'.join(tags))]
    return results
