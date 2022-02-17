# -*- coding: utf-8 -*-
'''
To implement:
- import account names and distinguish between TB accounts and GL only accounts
- instead of JE summary, do total debits and total credits

'''
import pandas
import numpy as np

# import data files
gla = pandas.read_csv('GLA.txt', sep="#\|#", engine="python")
glab = pandas.read_csv('GLAB.txt', sep="#\|#", engine="python")
jet = pandas.read_csv('JET.txt', sep="#\|#", engine="python")

# Pivot the GLAB
glab['FP'] = glab.apply(lambda row: str(int(row.fiscalYear)) + "-"+str(int(row.financialPeriod)), axis=1)
glab = glab.sort_values(by='FP', axis=0, ascending=True)
glab_piv=glab.pivot_table(values='endingBalanceLC', index=[glab.index, 'accountNumber'], columns='FP')
glab_piv=glab_piv.groupby(by='accountNumber').sum().reset_index().sort_values(by='accountNumber', axis=0, ascending=True)
glab_piv=glab_piv.rename_axis(columns=None)

# Summarize activity in JET file
jet_summary = jet.groupby(by='accountNumber').sum().reset_index().filter(items=['accountNumber','amountLC']).rename({'amountLC': "JEsummary"}, axis=1)
jet_summary=jet_summary.round(decimals=2)

# Find the summary of JE activity for accounts that show up in GL but not TBs
gl_acc=jet_summary.merge(glab_piv, how='left',on='accountNumber')
gl_acc = gl_acc[np.isnan(gl_acc.iloc[:,-1])].fillna(0.00)
gl_acc_columns = gl_acc.columns.tolist()
gl_acc_columns = [gl_acc_columns[0]] + gl_acc_columns[2:] + ['JEsummary']
gl_acc = gl_acc[gl_acc_columns]

# Find JE summary for each account in pivoted GLAB 
roll = glab_piv.merge(jet_summary, how='left', on='accountNumber')
for je in roll.index:
    if np.isnan(roll.loc[je]['JEsummary']):
        roll.loc[je,'JEsummary']=0.00
    else:
        pass

# Union the TB accounts with the accounts listed on the GL only
roll=pandas.concat([roll,gl_acc])
# Calculate expected closing balance of all accounts
roll['calcClosing']=roll.apply(lambda row: row[2]+row.JEsummary, axis=1)
# Remove 'JEsummary' from DataFrame
roll = roll.loc[:, roll.columns!='JEsummary']
# Calculate the difference between expected and imported closing balances
roll['difference']=roll.apply(lambda row: row[3]-row[4], axis=1)
roll = roll.round(decimals=2)
# Output completeness roll to console and save as Excel file.
print("\nCompleteness roll:")
print(roll)
roll.to_excel(r'completeness.xlsx', index=False)