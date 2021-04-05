from personalcapital import (
    Client
)

#https://stackoverflow.com/questions/29987840/how-to-execute-python-code-from-within-visual-studio-code
# Python 2 and 3 compatibility
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

def main():
    client = Client()
    client.start_client()

if __name__ == '__main__':
    main()
