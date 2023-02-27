from contextlib import redirect_stdout
import json

OUTPUT_FILE = 'find_in_logs.output.txt'
FILE = '/Users/ailton/Projects/openapi-links-to-CPNs/20220125-01-00_combined.log.txt'

email = ''
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MjEsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJuZXRvQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiMDlhNjEyZWNlNGI3ODkzYzExZWY0ZmI2MmMzZTdjYmYi'
# n de logins
#STR_1, STR_2 = email, 'POST /rest/user/login'
# n de requisições
#STR_1, STR_2 = '', token
# case 1
STR_1, STR_2 = 'GET /rest/basket/', token
# case 1: legitimous requests
#STR_1, STR_2 = 'GET /rest/basket/6', token
# case 2
#STR_1, STR_2 = 'POST /api/BasketItems/', token


def main():
    occurrences = 0
    tokens = set()
    ips = set()
    with open(FILE) as f:
        line_number = 1
        for line in f:
            if STR_1 in line and STR_2 in line:
                occurrences += 1
                print(line_number)
                print(line)
                try:
                    extract_data(tokens, ips, line)
                except:
                    continue
            line_number += 1
            
        print(f'{occurrences} ocorrências encontradas')

def extract_data(tokens, ips, line):
    json_object = json.loads(line)
    extract_tokens(tokens, json_object)
    extract_ips(ips, json_object)

def extract_tokens(tokens, json_object):
    if json_object.get('responseBody') \
                        and json_object.get('responseBody').get('authentication'):
        tokens.add(json_object.get('responseBody').get('authentication').get('token'))
    elif json_object.get('headerAuthorization'):
        tokens.add(json_object.get('headerAuthorization').replace('Bearer', ''))

def extract_ips(ips, json_object):
    if json_object.get('ip'):
        ips.add(json_object.get('ip'))


if __name__ == "__main__":
    with open(OUTPUT_FILE, 'w') as f:
        with redirect_stdout(f):
            main()
    