import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class InvoiceItem:
    plu: str
    name: str
    price: float
    quantity: int


class AbstractInvoice(ABC):
    def __init__(self, invoice=None):
        self._invoice = invoice
        self._item = None

    def __call__(self, items: List[InvoiceItem]):
        self._items = items
        if self._invoice:
           self._invoice(items)
        self.modify_invoice_content()
        return self._items

    @abstractmethod
    def modify_invoice_content(self) -> None:
        pass


class DiscountIfTotal(AbstractInvoice):
    """
    if total invoice > 30 -> discount 5% on all items
    """

    def modify_invoice_content(self):
        if (_ := sum(item.price * item.quantity for item in self._items)) > 30:
            print("Discount to all items..")
            for item in self._items:
                item.price = round(item.price * 0.95, 2)


class HappyOurs(AbstractInvoice):
    """
    for given happy hours modify price for plu 002 to fixed value
    """

    def modify_invoice_content(self):
        now_hour = datetime.datetime.now().hour
        if now_hour in (14, 15, 16):
            print("Happy ours applied..")
            for item in self._items:
                if item.plu == "002":
                    item.price = 0.5


class FreePLU001(AbstractInvoice):
    """
    if more than 5 of plu 001 -> one beer free of charge
    """

    def modify_invoice_content(self):
        if sum(item.quantity for item in self._items if item.plu == "001") > 5:
            print("Free beer added..")
            self._items.append(InvoiceItem("001", "Bier Pilsner", 0, 1))


if __name__ == "__main__":
    invoice_items = [
        InvoiceItem("001", "Bier Pilsner", 1.2, 15),
        InvoiceItem("002", "Heineken", 1.5, 10),
        InvoiceItem("001", "Bier Pilsner", 1.2, 4),
    ]

    a = DiscountIfTotal()
    b = FreePLU001(a) 
    c = HappyOurs(b)
    print("Original invoice:")
    print(invoice_items)
    invoice_items = c(invoice_items)
    print("Modified invoice:")
    print(invoice_items)