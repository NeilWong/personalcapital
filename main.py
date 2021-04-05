from personalcapital import (
    ConnectorSessionHandler
)

from datetime import datetime, timedelta

#https://stackoverflow.com/questions/29987840/how-to-execute-python-code-from-within-visual-studio-code
# Python 2 and 3 compatibility
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

def main():
    pc = ConnectorSessionHandler()
    pc.load_session()
    pc.start_session()

    get_sample_response(pc)

    pc.save_session()

def get_sample_response(pc: ConnectorSessionHandler):
    accounts_response = pc.fetch('/newaccount/getAccounts')

    now = datetime.now()
    date_format = '%Y-%m-%d'
    days = 90
    start_date = (now - (timedelta(days=days+1))).strftime(date_format)
    end_date = (now - (timedelta(days=1))).strftime(date_format)
    transactions_response = pc.fetch('/transaction/getUserTransactions', {
        'sort_cols': 'transactionTime',
        'sort_rev': 'true',
        'page': '0',
        'rows_per_page': '100',
        'startDate': start_date,
        'endDate': end_date,
        'component': 'DATAGRID'
    })
    accounts = accounts_response.json()['spData']
    print('Networth: {0}'.format(accounts['networth']))

    # transactions = transactions_response.json()['spData']
    # print('Number of transactions between {0} and {1}: {2}'.format(transactions['startDate'], transactions['endDate'], len(transactions['transactions'])))

if __name__ == '__main__':
    main()
