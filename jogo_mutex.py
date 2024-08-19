import threading
import time
import random

class Player:
    def __init__(self, name, global_lock):
        self.name = name
        self.health = 100
        self.global_lock = global_lock
        self.finished = threading.Event()

    def attack(self, opponent):
        if not self.finished.is_set():
            damage = random.randint(10, 20)
            print(f"{self.name} atacou {opponent.name} com {damage} de dano!")
            with self.global_lock:
                print(f"{self.name} está causando dano a {opponent.name}")
                opponent.health -= damage
                if opponent.health <= 0:
                    opponent.health = 0
                    print(f"{opponent.name} sofreu {damage} de dano e perdeu a luta!")
                    opponent.finished.set()
                print(f"{opponent.name} tem {opponent.health} de vida restante.")
            print(f"{self.name} liberou o bloqueio após atacar {opponent.name}")

def fight(player1, player2):
    round_counter = 0  # Contador de rodadas
    while not (player1.finished.is_set() or player2.finished.is_set()):
        print(f"\nRound {round_counter}")
        player1.attack(player2)
        if not player2.finished.is_set():
            player2.attack(player1)
        time.sleep(1)
        round_counter += 1  # Incrementa o contador de rodadas

    if player1.finished.is_set():
        print(f"{player1.name} perdeu a luta.")
    if player2.finished.is_set():
        print(f"{player2.name} perdeu a luta.")

global_lock = threading.Lock()

liu_kang = Player("Liu Kang", global_lock)
scorpion = Player("Scorpion", global_lock)

print("Luta implementando Mutex como solução de condição de corrida\n")
fight(liu_kang, scorpion)
