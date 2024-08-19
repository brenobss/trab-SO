import threading
import time
import random
import queue


class Player:
    def __init__(self, name, own_queue, opponent=None):
        self.name = name
        self.health = 100
        self.own_queue = own_queue
        self.opponent = opponent
        self.alive = True

    def set_opponent(self, opponent):
        self.opponent = opponent

    def attack(self):
        while self.health > 0 and self.opponent.alive:
            damage = random.randint(10, 20)
            print(f"{self.name} atacou com {damage} de dano!\n")
            self.opponent.own_queue.put(damage)
            time.sleep(random.uniform(0.5, 1.5))  # Pausa entre os ataques

    def take_damage(self):
        while self.health > 0:
            damage = self.own_queue.get()  # Espera até receber uma mensagem (dano)
            self.health -= damage
            if self.health <= 0:
                self.alive = False
                print(f"{self.name} sofreu {damage} de dano e perdeu a luta!\n")
                break
            else:
                print(f"{self.name} sofreu {damage} de dano e agora tem {self.health} de vida.\n")


def fight(player1, player2):
    t1 = threading.Thread(target=player1.attack)
    t2 = threading.Thread(target=player2.attack)
    t3 = threading.Thread(target=player1.take_damage)
    t4 = threading.Thread(target=player2.take_damage)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    # Espera até que um jogador perca
    while player1.alive and player2.alive:
        time.sleep(0.1)  # Checa periodicamente se o combate terminou

    # Finaliza todas as threads
    t1.join()
    t2.join()
    t3.join()
    t4.join()


# Inicialização das filas de mensagens
queue1 = queue.Queue()
queue2 = queue.Queue()

# Inicialização dos jogadores
liu_kang = Player("Liu Kang", queue1)
scorpion = Player("Scorpion", queue2)

# Definição dos oponentes
liu_kang.set_opponent(scorpion)
scorpion.set_opponent(liu_kang)

# Início do combate
print("Luta implementando Trocas de Mensagens como solução de condição de corrida\n")
fight(liu_kang, scorpion)