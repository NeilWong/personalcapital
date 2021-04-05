# types of data
# - https://home.personalcapital.com/api/newaccount/getAccounts2
    # returns a summary of user summary data: total assets, cash accounts total, credit cards total, liabilities, networth, etc
# - https://home.personalcapital.com/api/transaction/getUserTransactions
    # filtered by intervalType, returns: averageIn daily / weekly, net cash flow, money in / money out, etc
# - https://home.personalcapital.com/api/transactioncategory/getCategories
    # returns a list of all transaction categories
# - https://home.personalcapital.com/api/account/getUserSpending
    # returns user's weekly, monthly, and yearly spending
# - https://home.personalcapital.com/api/account/getRetirementCashFlow
# - https://home.personalcapital.com/api/financialplanner/getEmergencySavingsHistory
# - https://home.personalcapital.com/api/financialplanner/getDebtPaymentHistory
# - https://home.personalcapital.com/api/account/getHistories
    # returns a day by day record of user's account balances, networths & change in networth across multiple categories, and   networth summary
# - https://home.personalcapital.com/api/invest/getQuotes
    # returns stock quotes


# Data needed for excel...
    # Net worth information across checkings, investments, 401k, etc
        # https://home.personalcapital.com/api/newaccount/getAccounts2
    # Investment and savings summaries, cash, taxable, tax-deferred, tax-free, etc
    # Average monthly costs across different categories

def get_accounts(session):
    print("get_accoutns_summary")

def get_transactions(session):
    print("get_transactions")

def get_categories(session):
    pass

def get_spending(session):
    print("spending")

