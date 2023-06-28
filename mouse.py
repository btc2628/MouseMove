from pynput import mouse
from threading import Event, Thread
import time
from datetime import datetime

class MouseTracker:
    def __init__(self):
        self.last_moved = time.time()
        self.last_position = (0, 0)
        self.directions = [(10, 0), (0, 10), (-10, 0), (0, -10)]  # Right, Down, Left, Up
        self.current_direction = 0
        self.listener = mouse.Listener(on_move=self.on_move)
        self.controller = mouse.Controller()

    def on_move(self, x, y):
        self.last_moved = time.time()
        self.last_position = (x, y)

    def check_mouse_moved(self):
        return (time.time() - self.last_moved) <= 30

    def move_mouse(self):
        # Calculate new position
        move_x, move_y = self.directions[self.current_direction]
        new_position = (self.last_position[0] + move_x, self.last_position[1] + move_y)
        self.controller.position = new_position
        # Cycle to the next direction
        self.current_direction = (self.current_direction + 1) % 4

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

class TimerThread(Thread):
    def __init__(self, tracker):
        Thread.__init__(self)
        self.tracker = tracker
        self.stop_event = Event()

    def run(self):
        while not self.stop_event.is_set():
            current_hour = datetime.now().hour
            if 8 <= current_hour < 17:
                if not self.tracker.check_mouse_moved():
                    print("Mouse did not move in the last 30 seconds. Moving mouse.")
                    self.tracker.move_mouse()
                else:
                    print("Mouse moved in the last 30 seconds")
            time.sleep(1)

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    tracker = MouseTracker()
    tracker.start()

    timer_thread = TimerThread(tracker)
    timer_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        timer_thread.stop()
        timer_thread.join()

        tracker.stop()
