import utils.files as utils_files
import service.order as service_order


def main ():
    try:
        file = utils_files.Files()
        menu = file.read_file_json("menu.json")
        order = service_order.Order(menu, "customer")
        order.show_orders()
        order.take_order()
        order.save_orders()
        order.read_orders()
        order.take_transaction()
        order.show_transaction()
        order.save_transaction()
    except Exception as err :
        print(err)
if __name__ == "__main__":
    main()