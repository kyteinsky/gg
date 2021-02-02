import pandas as pd
import streamlit as st
import re

'# App to analyse working of'
'# *The Mind*'

df = pd.read_csv('dump.csv', skiprows=[0])

with open('dump.csv', 'r') as f:
	first_row = f.readline()

first_row = first_row.split(',')[:-1]
roles = [(re.findall('[a-z]+', seg)[0]) for seg in first_row]
first_row = [int(re.findall('[0-9]+', seg)[0]) for seg in first_row]


summ = 0
dfs = {}

for i in range(len(first_row)):
	if not i == 0: summ += first_row[i]
	dfs[roles[i]] = df.iloc[:, summ:(first_row[i]+summ)].values
	# print(df.iloc[:, summ:(first_row[i]+summ)].values)

del summ, roles

for i in dfs.items():
	'##',i[0]
	st.line_chart(i[1])
