import pytest
from replay.replay import Replay

# TODO: Improve test cases
# TODO: fix intermitent error
@pytest.mark.parametrize("OAS_filename, logs_name, expected_results", [
    ("tests/examples/Structural_Problem_Based_on_BOLA_Example.yaml",
     "logs/combined_example_structural_problem.json",
     ['0-initial-state.png', 'line-1-fire-line.png', 'line-3-fire-line.png']),
     ("tests/examples/JuiceShop.yaml",
     "logs/combined_login.json",
     ['0-initial-state.png', 'line-1-fire-line.png', 'line-3-fire-line.png'])
])
def test_replay_execution_on_log(OAS_filename, logs_name, expected_results):
    draws = Replay.replay_execution_on_log(OAS_filename, logs_name)
    draw_names = list(draws.keys())
    assert len(draw_names) == len(expected_results)
    for expected_result in expected_results:
        if expected_result in draw_names == False:
            assert True == False
    assert True
