#####################################################
# Comparison of Conversion Rates of Bidding Methods Using A/B Testing
#####################################################

#####################################################
# Business Problem
#####################################################

# Facebook recently introduced a new bidding method called "average bidding" as an alternative to the existing "maximum bidding" method.
# One of our clients, bombabomba.com, decided to test this new feature to determine if average bidding yields more conversions than maximum bidding.
#To do this, they set up an A/B test.
# The A/B test has been running for one month, and now bombabomba.com expects an analysis of the results.
# The primary success metric for bombabomba.com is the number of Purchases. Therefore, statistical tests and analysis should focus on the Purchase metric.


#####################################################
# Dataset Story
#####################################################

# This dataset contains information about a company's website, including the number of ads users saw and clicked on, as well as the revenue generated from these ads.
# There are two separate datasets: Control and Test groups. These datasets are located on separate sheets in the ab_testing.xlsx Excel file.
# The Control group used Maximum Bidding, while the Test group used Average Bidding.

# impression: Number of ad impressions
# Click: Number of clicks on the displayed ads
# Purchase: Number of products purchased after clicking on the ads
# Earning: Revenue generated from the purchased products
#####################################################
# Project Tasks
#####################################################

#####################################################
# Task 1: Prepare and Analyze the Data
#####################################################
# Step 1: Read the dataset named ab_testing_data.xlsx, which consists of control and test group data. Assign the control and test group data to separate variables.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel('ab_testing.xlsx', sheet_name="Control Group")
dataframe_test = pd.read_excel('ab_testing.xlsx', sheet_name="Test Group")


df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Step 2: Analyze the control and test group data.

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

# Step 3: After the analysis, use the concat method to combine the control and test group data.
# Add appropriate labels to ensure they do not get mixed up in the same dataframe.
df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], ignore_index=False, axis=0)
df.head()
df.tail()


#####################################################
# Task 2: Defining the Hypothesis for A/B Testing
#####################################################

# Step 1: Define the hypothesis.

# H0: M1 = M2 (There is no difference between the mean purchase amounts of the control group and the test group.)
# H1: M1 ≠ M2 (There is a difference between the mean purchase amounts of the control group and the test group.)

# Step 2: Analyze the mean purchase amounts for the control and test groups.
df.groupby("group")["Purchase"].mean()

# control    550.894059
# test       582.106097  # A difference has been observed, but is it statistically significant?

#####################################################
# TASK 3: Performing the Hypothesis Test
#####################################################

# Step 1: Before performing the hypothesis test, check the assumptions. These are the Normality Assumption and Homogeneity of Variance.

# Test whether the control and test groups meet the normality assumption separately using the Purchase variable.
# Normality Assumption:
# H0: The assumption of normal distribution is met.
# H1: The assumption of normal distribution is not met.
# p < 0.05 H0 REJECTED
# p > 0.05 H0 CANNOT BE REJECTED
# Based on the test results, does the normality assumption hold for the control and test groups?
# Interpret the obtained p-value results.

# Normality Assumption (Shapiro-Wilk test)
# Homogeneity of Variance

# Normality Assumption:
test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#  p-value = 0.5891 > 0.05 H0 cannot be rejected.

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.1541 H0 cannot be rejected.

# t-test (parametric test)
test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#  p-value = 0.3493 > 0.05 H0 cannot be rejected.
# H0: M1 = M2 (There is no difference between the mean purchase amounts of the control group and the test group.)