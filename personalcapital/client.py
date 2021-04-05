
class Client():

    def __init__(self, session):
        self.session = session
        self.session_active = True

    def start_client(self) -> None:
        while self.session_active:
            cmd = input('$: ')
            self.process_cmd(cmd)

    def process_cmd(self, cmd) -> None:
        if cmd == 'exit':
            self.__set_session_active(False)

    def __set_session_active(self, state):
        self.session_active = state
        
    # Actions that can be performed based on user input