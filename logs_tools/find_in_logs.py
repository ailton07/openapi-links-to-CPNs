from contextlib import redirect_stdout
import json

""" 
    This file is an auxiliar script to analyze logs
"""

OUTPUT_FILE = 'logs_tools/find_in_logs.output.txt'
FILE = ''
#FILE = 'logs_experiment_with_students/20220125-01-00_combined.log.txt'
#FILE = 'logs_experiment_with_students/20220127-00-00_combined-2.log.txt'
#FILE = 'logs_experiment_with_students/20220207-13-44_combined-3.log.txt'

email = ''
token = ''

# n de logins
STR_1, STR_2 = email, 'POST /rest/user/login'
# n de requisições
#STR_1, STR_2 = '', token
# case 1
#STR_1, STR_2 = 'GET /rest/basket/', token
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
                except Exception as e:
                    print (f'Exception in line {line_number}: {e}')
                    line_number += 1
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
    