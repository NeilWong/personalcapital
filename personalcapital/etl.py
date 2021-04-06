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
    data = get_data(session, '/newaccount/getAccounts2')

    accounts = data.json()['spData']
    #print('Networth: {0}'.format(accounts['networth']))
    print(accounts)

def get_transactions(session):
    data = get_data(session, '/transaction/getUserTransactions')

    transactions = data.json()['spData']
    print(transactions)

def get_categories(session):
    data = get_data(session, '/transactioncategory/getCategories')
    print(data)
    categories = data.json()['spData']
    print(categories)

def get_spending(session):
    data = get_data(session, '/account/getUserSpending')
    spending = data['spData']
    print(spending)

def get_data(session, endpoint):
    response = session.fetch(endpoint)
    if is_valid_response(response, endpoint):
        return response.json()
    else:
        raise ValueError('Request for ' + endpoint + ' data failed with error: ' + str(response.status_code))
def is_valid_response(response, endpoint):
    return response.status_code == 200