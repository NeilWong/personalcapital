from datetime import (
    datetime, timedelta
)
from .connectorsessionhandler import (
    ConnectorSessionHandler
)

class Client():

    def __init__(self):
        self.session = ConnectorSessionHandler()
        self.session_active = True

    def start_client(self) -> None:
        print('startinf client')
        self.session.load_session()
        self.session.start_session()
        self.get_sample_response(self.session)
        while self.session_active:
            cmd = input('$: ')
            self.process_cmd(cmd)
        
        self.session.save_session()

    def process_cmd(self, cmd) -> None:
        if cmd == 'exit':
            self.__set_session_active(False)

    def __set_session_active(self, state):
        self.session_active = state
        
    def get_sample_response(self, pc: ConnectorSessionHandler):
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
        # Actions that can be performed based on user input