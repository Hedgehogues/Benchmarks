import threading
import random
from queue import Queue

# Структуры данных для TCP соединений
class TCPSession:
    def __init__(self):
        self.state = "CLOSED"
        self.tx_seq = 0
        self.rx_seq = 0
        self.window_size = 1024  # Размер окна для управления потоком
        self.unacked_packets = Queue()  # Пакеты, которые ожидают подтверждения (ACK)

# Таблица конечных состояний для TCP
tcp_fsm = {
    "CLOSED": {
        "SYN": "SYN_SENT",
    },
    "SYN_SENT": {
        "SYN_ACK": "ESTABLISHED",
        "RST": "CLOSED"
    },
    "ESTABLISHED": {
        "FIN": "CLOSE_WAIT",
        "ACK": "ESTABLISHED",
        "DATA": "ESTABLISHED"
    },
    "CLOSE_WAIT": {
        "FIN": "LAST_ACK",
    },
    "LAST_ACK": {
        "ACK": "CLOSED"
    }
}

# Инициализация глобальных переменных и структур
tcp_sessions = {}
global_queue = Queue()

# Функции для работы с очередями
def enqueue_event(event):
    global_queue.put(event)

def dequeue_event():
    try:
        event = global_queue.get(timeout=1)
        return event
    except:
        return None

# Обработка события FSM для TCP
def process_tcp_event(event, session):
    current_state = session.state
    if event in tcp_fsm[current_state]:
        next_state = tcp_fsm[current_state][event]
        session.state = next_state
        print(f"Transition: {current_state} -> {next_state}")
    else:
        print(f"No transition for event {event} in state {current_state}")

# Обработчик сетевых пакетов
def process_tcp_packet(packet):
    if packet["type"] == "SYN":
        session = tcp_sessions.get(packet["session_id"], TCPSession())
        session.state = "SYN_SENT"
        tcp_sessions[packet["session_id"]] = session
        enqueue_event("SYN")

    elif packet["type"] == "SYN_ACK":
        session = tcp_sessions.get(packet["session_id"])
        if session:
            enqueue_event("SYN_ACK")

    elif packet["type"] == "DATA":
        session = tcp_sessions.get(packet["session_id"])
        if session:
            # Принять данные и отправить подтверждение (ACK)
            session.rx_seq += len(packet["data"])
            enqueue_event("DATA")
            enqueue_event("ACK")

    elif packet["type"] == "FIN":
        session = tcp_sessions.get(packet["session_id"])
        if session:
            enqueue_event("FIN")

    elif packet["type"] == "ACK":
        session = tcp_sessions.get(packet["session_id"])
        if session:
            # Подтвердить получение данных
            if not session.unacked_packets.empty():
                session.unacked_packets.get()  # Удалить подтверждённый пакет
            enqueue_event("ACK")

# Основной цикл обработки событий
def tcp_event_loop():
    while True:
        event = dequeue_event()
        if event:
            # Поиск соответствующей сессии и обработка события
            for session_id, session in tcp_sessions.items():
                process_tcp_event(event, session)

# Инициализация модуля TCP
def init_tcp_module():
    print("Initializing TCP Module...")

    # Запуск потока обработки событий
    event_thread = threading.Thread(target=tcp_event_loop)
    event_thread.start()

    print("TCP Module Initialized")

# Функция завершения работы модуля
def exit_tcp_module():
    print("Shutting down TCP Module...")

# Симуляция получения TCP пакетов
def simulate_tcp_network_activity():
    packet_types = ["SYN", "SYN_ACK", "DATA", "ACK", "FIN"]
    while True:
        packet = {
            "type": random.choice(packet_types),
            "session_id": random.randint(1, 100),
            "data": "Hello" if random.choice(packet_types) == "DATA" else None
        }
        process_tcp_packet(packet)
        threading.Event().wait(1)  # Задержка для симуляции активности

# Точка входа
if __name__ == "__main__":
    init_tcp_module()
    
    # Симуляция активности сети в другом потоке
    network_thread = threading.Thread(target=simulate_tcp_network_activity)
    network_thread.start()
