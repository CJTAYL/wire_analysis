#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 07:29:24 2025

@author: christopher_taylor
"""

import random 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from datetime import datetime
import helper_functions as help

# Generate data
wires = [random.randint(50, 500000) for _ in range(10)]
outliers = [600000, 3000000, 1200000, 1300000, 2500000]
amounts = wires + outliers
wire_type = random.choices(['domestic', 'international'], k = 15)
direction = random.choices(['outgoing', 'incoming'], k = 15)
recipient = random.choices(['Chris', 'Aliese', 'Jack', 'Johnathan', 'Lauren',
                            'Lucas', 'Charlotte'], k = 15)
sender = random.choices(['Chris', 'Aliese', 'Jack', 'Johnathan', 'Lauren', 
                         'Lucas', 'Charlotte'], k = 15)
accounts = help.account_number_generator(12) + help.general_ledger_generator(3)
dates = help.generate_random_dates(15, datetime(2025, 1, 1), datetime(2025, 1, 31))


data = {
       'date':dates,
       'account number':accounts,
       'direction':direction,
       'amount':amounts,
       'type':wire_type,
       'recipient':recipient,
       'sender':sender
        }

df = pd.DataFrame(data)

# Filter out accounts with less than 16 digits 
df_filtered = help.filter_out_general_ledgers(df, 'account number')

print(df_filtered)

# Calculate IQR
Q1 = np.percentile(df_filtered['amount'], 25)
Q3 = np.percentile(df_filtered['amount'], 75)
IQR = Q3 - Q1 

# Define thresholds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR 

# Identify outliers
outliers = df_filtered[(df_filtered['amount'] < lower_bound) | (df_filtered['amount'] > upper_bound)]

# Create boxplot 
plt.figure(figsize=(8, 5), dpi=600)
ax = sns.boxplot(data=df_filtered, y='amount')

ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Transfer Amount')
plt.title('January 2025 Outlier Analysis')

# Label outliers 
for i in outliers.index:
    plt.text(0, df_filtered['amount'][i], f"{df_filtered['amount'][i]:.1f}", ha='left', va='bottom', fontsize=10, color='red')
plt.show()

group_sums = df_filtered.groupby(['direction', 'type'])['amount'].sum().to_frame().reset_index()
group_sums.columns = ['Direction', 'Type', 'Sum']
group_sums['Sum'] = group_sums['Sum'].apply(lambda x: f'${x:,.2f}')

outliers_copy = outliers.copy()
outliers_copy['amount'] = outliers['amount'].apply(lambda x: f'${x:,.2f}')

print(group_sums)
print('')
print('Outliers')
print(outliers_copy)

