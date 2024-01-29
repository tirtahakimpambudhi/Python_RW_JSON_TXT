import datetime
import json
import os


class Order():
    def __init__(self,menu,filename):
        self.menu = menu
        self.orders = []
        self.total_price = 0
        self.name = ""
        self.filepath = os.path.join(os.getcwd(), "database", filename)
        self.bill = {}
    def show_orders(self):
        print()
        print("===========================================")
        print('===== DAFTAR MENU MAKANAN DAN MINUMAN =====')
        print(f"| {'Kode':7} | {'Menu':15} | {'Harga':8} |")
        print("===========================================")
        for key,value in self.menu.items():
            print(f"| {value['kode']:7} | {key:15} | {value['harga']:8} |")
        print("===========================================")
    def take_order(self):
        self.name = input("Enter your name  : ")

        while True:
            try:
                order = input("Enter your order  (Example : 3, 2): ")
                if order.lower() == "0":
                    break
                code_order, total_order = order.split(",")
                if code_order in [value['kode'] for value in self.menu.values()]:
                    choose_item = next(key for key,value in self.menu.items() if value['kode'] == code_order)
                    choose_price = self.menu[choose_item]['harga']
                    print(f"Anda memesan {choose_item} Dengan harga Rp.{choose_price}")
                    if choose_item in self.menu:
                        price = choose_price * int(total_order)
                        self.total_price += price
                        self.orders.append({'item': choose_item, 'price': int(price),'total_order':int(total_order)})
                    else:
                        print(f"Item {choose_item} Tidak Ada Di Menu")
                else : print("Invalid Kode")
            except:
                print("Format Input Invalid")
    def save_orders(self):
        order_detail = {
            'Nama Pelanggan':self.name,
            'orders': self.orders,
            'Total Harga': self.total_price,
        }
        with open(self.filepath,"+a")as file :
            file.write(json.dumps(order_detail)+"\n")

    def read_orders(self):
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            row_last = lines[-1]
            order_details = json.loads(row_last)
            print()
            print('|=======================================|')
            print(f"| Nama Pelanggan: {order_details['Nama Pelanggan']:18}    |")
            print('|=======================================|')
            print('|               DETAIL PESANAN          |')
            print('|=======================================|')
            print(f"|  {'Menu':16}| {'Porsi' :6}|    {'Harga':6}  |")
            print('|=======================================|')
            for order in order_details['orders']:
                print(f"| {order['item']:16} | {order['total_order']:5} | Rp{order['price']:8} |")
            print('|=======================================|')
            print(f"|Total Harga {'':15} Rp{order_details['Total Harga']:8} |")
            print('|---------------------------------------|')
            print('|=======================================|')
            print('|               TERIMA KASIH            |')
            print('|=======================================|')

    def take_transaction(self):
        try:
            with open(self.filepath, "r") as file:
                lines = file.readlines()
                if not lines:
                    print("No transaction data available.")
                    return

                row_last = lines[-1]
                order_details = json.loads(row_last)
                pay = int(input("Enter your Money: "))

                while pay < order_details["Total Harga"]:
                    print("Insufficient payment. Please enter sufficient amount.")
                    pay = int(input("Enter your Money: "))

                exchange = pay - order_details["Total Harga"]
                date = datetime.datetime.now()
                id = f"{date.year}{date.month}{date.day}{date.time().hour}{date.time().minute}{date.time().second}"
                format_date = f"{date.year}-{date.month}-{date.day} {date.time().hour}:{date.time().minute}:{date.time().second}"

                self.bill = {
                    'id': id,
                    'date': format_date,
                    'order_details': order_details,
                    'pay': pay,
                    'exchange': exchange
                }
        except Exception as err:
            print(f"Error: {err}")
    def show_transaction(self):

        print("=======================================")
        print(f"| Kode Transaksi: {self.bill['id']}      |")
        print("=======================================")
        print(f"| Nama Pelanggan: {self.bill['order_details']['Nama Pelanggan']} -              |")
        print("=======================================")
        print(f"| Tanggal: {self.bill['date']}       |")
        print("=======================================")
        print("|                DETAIL PESANAN        |")
        print("=======================================")
        print("| Menu                | Porsi | Harga  |")
        print("|---------------------|-------|--------|")
        for order in self.orders:
            print(f"| {order['item']}         | {order['total_order']}     | Rp{order['price']}|")
        print("=======================================")
        print(f"| Total Harga: Rp{self.bill['order_details']['Total Harga']}                 |")
        print(f"| Uang Bayar: Rp{self.bill['pay']}            |")
        print(f"| Kembalian: Rp{self.bill['exchange']}             |")
        print("=======================================")
        print("|                TERIMA KASIH          |")
        print("=======================================")
    def save_transaction(self):
        with open(self.filepath,"+a")as file :
            file.write(json.dumps(self.bill)+"\n")