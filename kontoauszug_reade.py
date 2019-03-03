#!/usr/bin/env python
# -*- coding: utf-8 -*-
# kontoauszug_reader
# Mit diesem Script sollen kontoauszüge eingelesen werden können 
# um Ein- und Ausgehendes Geld in Kategorien einzuordnen und entsprechend darzustellen

import pandas as pd

kontoauszug_path = "./kontoauszuege/umsaetze-325794-2019-03-02-16-34-32.csv"

kontoauszug_df = pd.read_csv(kontoauszug_path, header=11)

print(kontoauszug_df.head())
