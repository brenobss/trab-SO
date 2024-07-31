import threading
import time
import random


class Semaphore:
    def __init__(self, value=1):
        self.value = value
        self.condition = threading.Condition()

    def acquire(self):
        # Adquire o lock associado à condição
        self.condition.acquire()
        try:
            # Se o valor do semáforo for menor ou igual a 0, a thread espera
            while self.value <= 0:
                self.condition.wait()
            # Decrementa o valor do semáforo
            self.value -= 1
        finally:
            # Libera o lock
            self.condition.release()

    def release(self):
        # Adquire o lock associado à condição
        self.condition.acquire()
        try:
            # Incrementa o valor do semáforo
            self.value += 1
            # Notifica uma das threads em espera
            self.condition.notify()
        finally:
            # Libera o lock
            self.condition.release()


class Player:
    def __init__(self, name, semaphore):
        self.name = name
        self.health = 100
        self.semaphore = semaphore

    def attack(self, opponent):
        if self.health > 0:
            damage = random.randint(10, 20)
            print(f"{self.name} atacou {opponent.name} com {damage} de dano!\n")
            opponent.take_damage(damage)
            return damage
        else:
            return 0

    def take_damage(self, damage):
        self.semaphore.acquire()
        try:
            self.health -= damage
            if self.health <= 0:
                print(f"{self.name} sofreu {damage} de dano e perdeu a luta!\n")
            else:
                print(f"{self.name} sofreu {damage} de dano e agora tem {self.health} de vida.\n")
        finally:
            self.semaphore.release()


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


# Inicialização do semáforo
semaforo = Semaphore()

# Inicialização dos jogadores
liu_kang = Player("Liu Kang", semaforo)
scorpion = Player("Scorpion", semaforo)

# Início do combate
fight(liu_kang, scorpion)
