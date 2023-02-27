# Openapi Links to CPNs
Use the library Snakes to create CPNs modeling OpenAPI data-flows (Links)


## Installation
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
(Tested with Python 3.9)

## Usage
```
python3 run_examples.py
python3 execute_replay.py examples/OWASP-Juice-Shop-experiment.yaml logs/real_logs_experiment.log

```

## Example Cases

In ```logs/combined_example_structural_problem.json```, we have an example of an API in normal usage. The OpenAPI Specification associated is ```examples/Structural_Problem_Based_on_BOLA_Example.yaml```.
While in ```logs/combined_example_structural_problem_BOLA_case.json``` we have an example of an API under a BOLA attack.



## Naming convention
https://stackoverflow.com/a/42127721


## Parameter Locations

According to the [OpenAPI specification](https://swagger.io/specification/#parameter-object), the Parameter Locations are as following:
- path
- query
- header
- cookie
