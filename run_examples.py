import os

OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml', 'logs/combined_example_structural_problem.json'
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml', 'logs/combined_example_structural_problem.json'
#OPENAPI_PATH, LOGS_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_03.yaml', 'logs/combined_example_structural_problem_example_03.json'
#OPENAPI_PATH, LOGS_PATH = 'examples/BOLA_Example_login_and_accounts_id.yaml', 'logs/combined_bola_example.json'

# Juice Shop Cases
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/combined_login.json'
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/combined_login_multiuser.json'
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/log_signup_login_basket_with_false_positive.log'
#OPENAPI_PATH, LOGS_PATH = 'examples/JuiceShop.yaml', 'logs/combined_logs_juice_shop_signup_view_basket.log'
# a vulnerabilidade é explorada por HTTP Parameter Pollution
#OPENAPI_PATH, LOGS_PATH = 'examples/OWASP-Juice-Shop-BOLA-cases.yaml', 'logs/combined_logs_Juic_Shop_manipulate_basket.log'
EXECUTABLE = "execute_replay.py"



def main():
    os.system(f'python3 {EXECUTABLE} {OPENAPI_PATH} {LOGS_PATH}')



if __name__ == "__main__":
    main()