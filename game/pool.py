"""Reusable object pool."""
class Pool:
    def __init__(self, factory, size):
        self.items = [factory() for _ in range(size)]
    def acquire(self):
        for item in self.items:
            if not item.active:
                item.active = True
                return item
        return None
    def active_items(self):
        return (item for item in self.items if item.active)
