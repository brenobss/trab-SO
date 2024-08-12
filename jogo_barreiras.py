import threading
import time
import random


#A classe Barrier é usada para sincronizar múltiplas threads.
# O objetivo é garantir que todas as threads esperem até que todas tenham chegado a um ponto de sincronização antes de continuar.

class Barrier:
    def __init__(self, count):
        self.count = count
        self.mutex = threading.Lock()
        self.condition = threading.Condition(self.mutex)
        self.waiting = 0

    def wait(self):
        with self.mutex:
            self.waiting += 1
            if self.waiting >= self.count:
                self.waiting = 0
                self.condition.notify_all()
            else:
                self.condition.wait()


class Player:
    def __init__(self, name, barrier):
        self.name = name
        self.health = 100
        self.barrier = barrier
        self.alive = True

    def attack(self, opponent):
        while self.health > 0 and opponent.alive:
            damage = random.randint(10, 20)
            print(f"{self.name} atacou {opponent.name} com {damage} de dano!\n")
            opponent.take_damage(damage)
            self.barrier.wait()  # Sincroniza após o ataque
            time.sleep(random.uniform(0.5, 1.5))  # Pausa entre os ataques

    def take_damage(self, damage):
        if self.alive:
            self.health -= damage
            if self.health <= 0:
                self.alive = False
                print(f"{self.name} sofreu {damage} de dano e perdeu a luta!\n")
            else:
                print(f"{self.name} sofreu {damage} de dano e agora tem {self.health} de vida.\n")
            self.barrier.wait()  # Sincroniza após receber dano


def fight(player1, player2):
    # Cria a barreira para sincronizar as threads de ataque e dano
    barrier = Barrier(2)

    # Cria e inicia as threads
    t1 = threading.Thread(target=player1.attack, args=(player2,))
    t2 = threading.Thread(target=player2.attack, args=(player1,))

    t1.start()
    t2.start()

    # Espera até que um jogador perca
    while player1.alive and player2.alive:
        time.sleep(0.1)  # Checa periodicamente se o combate terminou

    # Finaliza todas as threads
    t1.join()
    t2.join()


# Inicialização dos jogadores
barrier = Barrier(2)  # Cria uma barreira para sincronizar as ações
liu_kang = Player("Liu Kang", barrier)
scorpion = Player("Scorpion", barrier)

# Início do combate
print("Luta implementando Barreiras como solução de condição de corrida\n")
fight(liu_kang, scorpion)
