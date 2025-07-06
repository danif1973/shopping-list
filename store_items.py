from item import Item

class StoreItems:
    def __init__(self, name: str):
        self.name = name
        self.items = []  # List[Item]

    def add_item(self, item: Item):
        self.items.append(item)

    def __repr__(self):
        return f"StoreItems(name={self.name!r}, items={self.items!r})" 