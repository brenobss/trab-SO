import threading
import time
import random


class Mutex:
    def __init__(self):
        self.locked = False
        self.condition = threading.Condition()

    def acquire(self):
        self.condition.acquire()
        try:
            while self.locked:
                # Espera até que o mutex esteja disponível
                self.condition.wait()
            self.locked = True
        finally:
            # Libera o lock após a atualização
            self.condition.release()

    def release(self):
        self.condition.acquire()
        try:
            self.locked = False
            # Notifica uma thread que está esperando
            self.condition.notify()
        finally:
            # Libera o lock após a atualização
            self.condition.release()


class Player:
    def __init__(self, name, mutex):
        self.name = name
        self.health = 100
        self.mutex = mutex

    def attack(self, opponent):
        if self.health > 0:
            damage = random.randint(10, 20)
            print(f"{self.name} atacou {opponent.name} com {damage} de dano!\n")
            opponent.take_damage(damage)
            return damage
        else:
            return 0

    def take_damage(self, damage):
        self.mutex.acquire()
        try:
            self.health -= damage
            if self.health <= 0:
                print(f"{self.name} sofreu {damage} de dano e perdeu a luta!\n")
            else:
                print(f"{self.name} sofreu {damage} de dano e agora tem {self.health} de vida.\n")
        finally:
            self.mutex.release()


def fight(player1, player2):
    while player1.health > 0 and player2.health > 0:
        # Ambos atacam ao mesmo tempo
        t1 = threading.Thread(target=player1.attack, args=(player2,))
        t2 = threading.Thread(target=player2.attack, args=(player1,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        time.sleep(1)


mutex = Mutex()

# Inicialização dos jogadores
liu_kang = Player("Liu Kang", mutex)
scorpion = Player("Scorpion", mutex)

# Início do combate
print("Luta implementando Mutex como solução de condição de corrida\n")
fight(liu_kang, scorpion)
