# detector/state.py
import threading
from collections import Counter


class DetectionState:
    def __init__(self):
        self.lock = threading.Lock()
        self.counts = Counter()
        self.last_detector = 'face'

    def set_detector(self, name: str):
        with self.lock:
            self.last_detector = name

    def update_counts(self, labels):
        with self.lock:
            self.counts.update(labels)

    def reset(self):
        with self.lock:
            self.counts.clear()

    def snapshot(self):
        with self.lock:
            return {
                'detector': self.last_detector,
                'counts': dict(self.counts),
            }


GLOBAL_STATE = DetectionState()
