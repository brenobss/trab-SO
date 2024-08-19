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
        self.lock = threading.Lock()  # Adicionando um lock para sincronizar acesso ao estado do jogador
        self.fight_over = threading.Event()  # Evento para sinalizar o fim da luta

    def attack(self, opponent):
        if self.health > 0 and not self.fight_over.is_set() and not opponent.fight_over.is_set():
            self.semaphore.acquire()

            if not self.fight_over.is_set() and not opponent.fight_over.is_set():
                damage = random.randint(10, 20)
                print(f"{self.name} atacou {opponent.name} com {damage} de dano!\n")
                opponent.take_damage(damage)

            self.semaphore.release()

    def take_damage(self, damage):
        with self.lock:  # Usando o lock para garantir acesso exclusivo
            if self.health > 0:
                self.health -= damage
                if self.health <= 0:
                    self.health = 0
                    print(f"{self.name} sofreu {damage} de dano e perdeu a luta!\n")
                    self.fight_over.set()
                else:
                    print(f"{self.name} sofreu {damage} de dano e agora tem {self.health} de vida.\n")


def fight(player1, player2):
    while not player1.fight_over.is_set() and not player2.fight_over.is_set():
        t1 = threading.Thread(target=player1.attack, args=(player2,))
        t2 = threading.Thread(target=player2.attack, args=(player1,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        if player1.fight_over.is_set() or player2.fight_over.is_set():
            break
        time.sleep(1)

    if player1.health > 0:
        print(f"{player2.name} perdeu a luta.")
    if player2.health > 0:
        print(f"{player1.name} perdeu a luta.")


# Inicialização do semáforo
semaforo = Semaphore(1)

# Inicialização dos jogadores
liu_kang = Player("Liu Kang", semaforo)
scorpion = Player("Scorpion", semaforo)

# Início do combate
fight(liu_kang, scorpion)
