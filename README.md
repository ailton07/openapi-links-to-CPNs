# Links2CPN - OpenAPI Links to CPNs

A tool to create a Colored Petri Net from an OpenAPI Specification (with Links), using the library Snakes, and apply the conformance checking algorithm from Carrasquel, Mecheraoui & Lomazova, 2021 with custom event log files.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---
## Installation
Make sure you already have Python 3.x installed in your system (Tested with Python 3.9) and execute:

```
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
Besides that, you may want to install [GraphViz](https://graphviz.org/) to be able to draw nets.
```
sudo apt install graphviz
```


## Usage
```
$ cd src/
$ python3 execute_replay.py <open_api_specification_path> <event_logs_path>

// Example
$ python3 execute_replay.py examples/OWASP-Juice-Shop-experiment.yaml logs/real_logs_experiment.log
```
Creating as an output the CPN states in `.png` format within `./draws` folder and printing on the console:
```
Cleaning draw_dir: draws/
Processing...
Line 1 is not present in the model: GET /rest/admin/application-configuration 200 9ms
Line 2 is not present in the model: GET /rest/admin/application-version 200 2ms
Line 3 is not present in the model: GET /api/Challenges/?name=Score%20Board 200 39ms
[...]
Line 147 is not present in the model: GET /api/BasketItems/11 200 33ms
Line 148 is not present in the model: PUT /api/BasketItems/11 200 31ms
Done in 3.7537190914154053 seconds
```
Alternatively, you can execute the `run_examples.py` script that already has set an example of `<open_api_specification_path>` and  `<event_logs_path>` information and saves the output in `run_examples.output.txt`.

```

$ python3 run_examples.py

```

---
## Reference
[SNAKES is the net algebra kit for editors and simulators](https://snakes.ibisc.univ-evry.fr/)

## License

Licensed under the [GNU GPLv3](LICENSE) license.