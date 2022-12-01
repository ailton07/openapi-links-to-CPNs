import argparse
from replay.replay import Replay

# Important examples
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/combined_logs_juice_shop_signup_view_basket.log'
# a vulnerabilidade é explorada por HTTP Parameter Pollution
OPENAPI_PATH, LOGS_PATH = 'examples/OWASP-Juice-Shop-BOLA-cases.yaml', 'logs/combined_logs_Juic_Shop_manipulate_basket.log'

parser = argparse.ArgumentParser(description='Execute the replay of logs on OpenAPI Specifications')
parser.add_argument('open_api_path',
                       metavar='open_api_path',
                       type=str,
                       help='the path to the OpenApi Specification')
parser.add_argument('logs_path',
                       metavar='logs_path',
                       type=str,
                       help='the path to the log file')

def main():
    openapi_path, logs_path = vars(parser.parse_args()).values()
    if openapi_path and logs_path:
        Replay.replay_execution_on_log(openapi_path, logs_path)
        return None
    print("Positional arguments open_api_path and/or logs_path not found")
    Replay.replay_execution_on_log(OPENAPI_PATH, LOGS_PATH)
    return None

if __name__ == "__main__":
    main()
