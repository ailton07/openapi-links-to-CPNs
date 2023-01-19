import os

EXECUTABLE = "execute_replay.py"
# strutuctural problem based on BOLA_Example, that is the same endpoint POST /login with 2 different resulting status codes
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml', 'logs/combined_example_structural_problem.json'

# strutuctural problem based on BOLA_Example, /login accepting POST and PUT methods. /accounts/{id} is accepting GET
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml', 'logs/combined_example_structural_problem.json'

# strutuctural problem based on BOLA_Example, /login accepting POST and PUT methods. /accounts is accepting POST
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_03.yaml', 'logs/combined_example_structural_problem_example_03.json'

# BOLA example, we have /login and /accounts/{id}. Logs describing a no attack scenario
#OPENAPI_PATH, LOGS_PATH = 'examples/BOLA_Example_login_and_accounts_id.yaml', 'logs/combined_bola_example.json'

# Juice Shop Cases
# /rest/basket/{bid} and /rest/user/login, no attack scenario
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/combined_login.json'

# /rest/basket/{bid} and /rest/user/login, no attack scenario with multiple users
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/combined_login_multiuser.json'

# /rest/basket/{bid} and /rest/user/login, no attack scenario, but app running in AWS
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/real_log_signup_login_basket.log.log'

# /rest/basket/{bid} and /rest/user/login, attack scenario view basket, but app running in AWS
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/real_logs_juice_shop_signup_view_basket.log'

# /rest/basket/{bid} and /rest/user/login, attack exploring HTTP Parameter Pollution, created artificially
#OPENAPI_PATH, LOGS_PATH = 'examples/OWASP-Juice-Shop-BOLA-cases.yaml', 'logs/combined_logs_Juic_Shop_manipulate_basket.log'

# /rest/basket/{bid} and /rest/user/login, attack exploring HTTP Parameter Pollution, real log, at the logs, it's shown only one BasketId (the last one)
OPENAPI_PATH, LOGS_PATH = 'examples/OWASP-Juice-Shop-BOLA-cases.yaml', 'logs/real_log_Juice_Shop_manipulate_basket.log'


def main():
    os.system(f'python3 {EXECUTABLE} {OPENAPI_PATH} {LOGS_PATH}')



if __name__ == "__main__":
    main()