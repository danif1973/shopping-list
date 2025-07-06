class Item:
    def __init__(self, name: str, price: float = None, hh_order: int = None):
        self.name = name
        self.price = price
        self.hh_order = hh_order

    def __repr__(self):
        return f"Item(name={self.name!r}, price={self.price!r}, hh_order={self.hh_order!r})" 