import argparse
import time
from replay.replay import Replay
from utils.draw_utils import DrawUtils

# Important examples
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/real_logs_juice_shop_signup_view_basket.log'
# a vulnerabilidade é explorada por HTTP Parameter Pollution
#OPENAPI_PATH, LOGS_PATH = 'examples/OWASP-Juice-Shop-BOLA-cases.yaml', 'logs/combined_logs_Juic_Shop_manipulate_basket.log'

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
    started_at = time.time()
    # clean output directory
    DrawUtils.clean_draw_dir()
    print ('Processing...')
    # start the processment
    openapi_path, logs_path = vars(parser.parse_args()).values()
    if openapi_path and logs_path:
        Replay.replay_execution_on_log(openapi_path, logs_path)
        done_at = time.time()
        print (f'Done in {done_at - started_at} seconds')
        return None
    print("Positional arguments open_api_path and/or logs_path not found")
    return None

if __name__ == "__main__":
    main()
