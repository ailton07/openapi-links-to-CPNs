import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *
from openapi.openapi2cpn import OpenAPI2PetriNet



OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml'

def main():
    open_api_to_petri_parser = OpenAPI2PetriNet(OPENAPI_PATH)
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    transitions = petri_net.transition()
    petri_net.draw("value-0.png")


if __name__ == "__main__":
    main()