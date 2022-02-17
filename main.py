import pandas
import numpy as np
pandas.set_option("display.precision", 2)
gla = pandas.read_csv('GLA.txt', sep="#\|#", engine="python")
glab = pandas.read_csv('GLAB.txt', sep="#\|#", engine="python")
jet = pandas.read_csv('JET.txt', sep="#\|#", engine="python")

# check all GLAB accounts are in GLA
#print(glab["accountNumber"].unique())
test1 =gla.merge(pandas.Series(glab["accountNumber"].unique(), name="unique_accountNumber"), how="right", left_on="accountNumber", right_on="unique_accountNumber")
print("GLAB accounts not in GLA:")
print(test1[test1.isnull()["accountNumber"]])
# check duplicate account numbers in GLA and GLAB

# check duplicated GLAB account-fiscalYear-financialPeriod combinations
print(test1.drop_duplicates())
# check each endingBalanceLC, amountLC fields have 2 precision
#print(gla['accountNumber'])

# check gla accounts: have only 3 entries in GLAB
test2_right = pandas.DataFrame(glab.accountNumber.value_counts())
test2=gla.merge(glab, how="right", on="accountNumber")
cond=test2.groupby("accountNumber").agg({'accountName': "count"}).accountName!=3
newtest2=gla.merge(cond, how="left", on="accountNumber")
# pandas.Series(test2.groupby("accountNumber").agg({'accountName': "count"}).accountName, name="accountNamecount")
print("GLAB 3 entries only:")
# print(newtest2[newtest2.accountName_y])

test2_right.reset_index(inplace=True)
print(test2_right.rename({"index":"accountNumber", 'accountNumber':"count"}, axis=1))

# completeness roll
glab['FP'] = glab.apply(lambda row: str(int(row.fiscalYear)) + "-"+str(int(row.financialPeriod)), axis=1)
glab = glab.sort_values(by='FP', axis=0, ascending=True)
comp=glab.pivot_table(values='endingBalanceLC', index=[glab.index, 'accountNumber'], columns='FP')
comp=comp.groupby(by='accountNumber').sum().reset_index().sort_values(by='accountNumber', axis=0, ascending=True)
comp=comp.rename_axis(columns=None)
print("\nCompleteness roll:")
jet_summary = jet.groupby(by='accountNumber').sum().reset_index().filter(items=['accountNumber','amountLC']).rename({'amountLC': "JEsummary"}, axis=1)

roll = comp.merge(jet_summary, how='left', on='accountNumber')
for je in roll.index:
    if np.isnan(roll.loc[je]['JEsummary']):
        roll.loc[je,'JEsummary']=0.00
    else:
        pass

roll['calcClosing']=roll.apply(lambda row: row[2]+row.JEsummary, axis=1)
roll = roll.loc[:, roll.columns!='JEsummary']
roll['difference']=roll.apply(lambda row: row[3]-row[4], axis=1)
print(roll)