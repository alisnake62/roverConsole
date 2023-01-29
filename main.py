from src.console import Console
from src.marsLink import MarsLink

if __name__ == '__main__':

    # initialisation de la connextion avec le rover sur mars (Module MarsLink)
    with MarsLink() as marsLink:

        # initialisation de la console qui va envoyer les instructions
        console = Console(marsLink=marsLink)
        console.run()
