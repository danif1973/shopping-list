import csv
from store_items import StoreItems

class PriceMatrix:
    def __init__(self):
        self.stores = []  # List[StoreItems]

    def add_store(self, store: StoreItems):
        self.stores.append(store)

    def _format_rtl_text(self, text):
        """Format RTL text with proper Unicode control characters for terminal display"""
        # Add RLE (Right-to-Left Embedding) and PDF (Pop Directional Format) for RTL text
        return f"\u202B{text}\u202C"

    def _get_visual_width(self, text):
        """Get the visual width of text, excluding Unicode control characters"""
        # Remove Unicode control characters for width calculation
        import re
        # Remove RLE, PDF, and other directional formatting characters
        clean_text = re.sub(r'[\u202A-\u202E\u2066-\u2069]', '', text)
        return len(clean_text)

    def Print(self):
        if not self.stores:
            print("No data to display.")
            return
        # Collect all unique product names
        product_names = set()
        for store in self.stores:
            for item in store.items:
                product_names.add(item.name)
        product_names = sorted(product_names)
        
        # Calculate column widths - use visual width for RTL text
        headers = ["Product Name"] + [store.name for store in self.stores]
        col_widths = [self._get_visual_width(header) for header in headers]
        
        # Find maximum width for each column
        for product in product_names:
            col_widths[0] = max(col_widths[0], self._get_visual_width(product))
            for i, store in enumerate(self.stores):
                price = next((item.price for item in store.items if item.name == product), "N/A")
                price_str = str(price) if price is not None else "N/A"
                col_widths[i + 1] = max(col_widths[i + 1], len(price_str))
        
        # Print header in RTL order (product name first, then store columns in reverse order)
        product_header = self._format_rtl_text(headers[0])  # Format RTL text
        store_headers = [headers[i].ljust(col_widths[i]) for i in range(len(headers)-1, 0, -1)]
        header_row = " | ".join([product_header] + store_headers)
        print(header_row)
        print("-" * len(header_row))
        
        # Print rows in RTL order
        for product in product_names:
            row = [product]
            for store in self.stores:
                price = next((item.price for item in store.items if item.name == product), "N/A")
                price_str = str(price) if price is not None else "N/A"
                row.append(price_str)
            
            # Product name with RTL formatting, store columns aligned
            product_col = self._format_rtl_text(row[0])  # Format RTL text
            store_cols = [row[i].ljust(col_widths[i]) for i in range(len(row)-1, 0, -1)]
            formatted_row = " | ".join([product_col] + store_cols)
            print(formatted_row)

    def Save(self, filename="prices.csv"):
        if not self.stores:
            print("No data to save.")
            return
        product_names = set()
        for store in self.stores:
            for item in store.items:
                product_names.add(item.name)
        product_names = sorted(product_names)
        headers = ["Product Name"] + [store.name for store in self.stores] + ["hh_order"]
        
        # Save with UTF-8 BOM
        with open(filename, mode="w", newline='', encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for product in product_names:
                row = [product]
                for store in self.stores:
                    price = next((item.price for item in store.items if item.name == product), "N/A")
                    row.append(str(price) if price is not None else "N/A")
                # Add hh_order from the first store that has this product
                hh_order = None
                for store in self.stores:
                    item = next((item for item in store.items if item.name == product), None)
                    if item and item.hh_order is not None:
                        hh_order = item.hh_order
                        break
                row.append(str(hh_order) if hh_order is not None else "N/A")
                writer.writerow(row) 