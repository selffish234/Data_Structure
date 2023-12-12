from CircularQueue import CircularQueue


class StockMap:
    def __init__(self):
        self.menus = []
        self.stocks = []

    def search(self, key):
        if key in self.menus:
            return self.menus.index(key)
        else:
            return 'Q'

    def insert(self, key, entry):
        self.menus.append(key)
        self.stocks.append(entry)

    def delete(self, key):
        location = self.search(key)
        self.menus.remove(key)
        self.stocks.pop(location)


class ManagementSystem:
    def __init__(self):
        self.total_income = 0
        self.data = StockMap()
        self.menu = {}
        self.counter = 0
        self.max_table = int(input("테이블 자리 수를 입력해주세요 : ")) + 1
        self.waitinglist = CircularQueue(500)
        self.order = {}
        self.complete_order_dict = {}
        self.tables = CircularQueue(self.max_table)
        self.workqueue = {}

    def add_menu(self):
        menu_name = ''
        menu_price = 0
        while True:
            add_menu = input("메뉴와 가격을\n메뉴 : 가격\n과 같이 입력하세요 (끝내려면 Q 를 입력하세요.)>> ")
            if add_menu != 'Q':
                add_menu = add_menu.split(':')
                menu_name = add_menu[0].strip()
                menu_price = int(add_menu[1])
                if menu_name not in self.menu.keys():
                    stock = int(input("예상 재고를 입력하세요 : "))
                    self.menu[menu_name] = menu_price
                    self.data.insert(menu_name, stock)
                self.workqueue[menu_name] = CircularQueue(self.max_table * 2)
                self.display_menu()
            else:
                break

    def display_menu(self):
        for menu in self.menu.keys():
            print("{0} : {1}".format(menu, self.menu[menu]))

    def subtract_menu(self):
        subtract_menu_name = input("제거하고자하는 메뉴의 이름을 입력하세요 : ")
        menu_name_strip = subtract_menu_name.strip()
        if menu_name_strip in self.menu.keys():
            del self.menu[menu_name_strip]
            self.delete_menu(menu_name_strip)
            del self.workqueue[menu_name_strip]
        else:
            print(f"{menu_name_strip}은(는) 메뉴 목록에 없습니다.")


    def add_waiting(self):
        self.counter += 1
        nickname = input("이름을 입력해주세요 : ")
        self.waitinglist.enqueue([self.counter, nickname]) # 1번부터 시작
        print(f"{nickname}님의 대기번호는 {self.counter}입니다.")
        self.add_table(self.counter)

    def display_waiting(self):
        print(f"현재 {self.waitinglist.size()}명의 대기 인원이 있습니다.")

    def take_order(self):
        table_number = int(input("주문하는 팀의 대기번호를 입력하세요: "))
        if table_number in self.order:
            while True:
                self.display_menu()
                order_item = input("주문할 음식을 입력하세요 (끝내려면 Q 를 입력하세요.)>> ")
                if order_item.upper() != 'Q':
                    if self.is_orderable(order_item):
                        self.order[table_number].append(order_item)
                        self.after_order(order_item)
                        self.workqueue[order_item].enqueue(table_number)
                    else:
                        print("품절된 품목입니다.")
                else:
                    break
            result = self.order[table_number][1:]
            print(f"{table_number}팀의 주문 목록:")
            for key in result:
                print(f"{key} : {self.menu[key]}원")
        else:
            print("존재하지 않는 테이블입니다.")

    def display_orders(self):
        table_number = int(input("보고 싶은 팀의 대기번호를 입력하세요: "))
        if table_number in self.order:
            order_list = self.order[table_number][1:]
            print(f"{table_number}팀의 주문 목록:")
            for key in order_list:
                print(f"{key} : {self.menu[key]}원")
        else:
            print(f"{table_number}번 대기번호는 주문이 없습니다.")

    def kitchen_out(self):
        for key in self.workqueue.keys():
            print(key, end=' ')
        print("\n")
        out = input("완성된 메뉴의 이름을 입력하세요 : ")
        if not self.workqueue[out].size() == 0:
            number = self.workqueue[out].dequeue()
            lis = self.complete_order_dict[number]
            lis.append(out)
            self.complete_order_dict[number] = lis
            print(f"{out}이 {number}번 대기번호 팀에 서빙되었습니다.")
        else:
            print("주문이 없습니다.")
    # def complete_order_item(self):
    #     table_number = input("주문이 완료된 테이블 번호를 입력하세요: ")
    #     if table_number in self.order:
    #         order_list2 = list(self.order[table_number])
    #         print(order_list2)
    #         item_to_complete = input("완료된 음식의 이름을 입력하세요: ")
    #         if item_to_complete in order_list2:
    #             order_list2.remove(item_to_complete)
    #
    #             if table_number not in self.complete_order_dict:
    #                 self.complete_order_dict[table_number] = []
    #
    #             self.complete_order_dict[table_number].append(item_to_complete)
    #             print(f"{table_number} 테이블의 주문 목록에서 {item_to_complete}이(가) 완료 처리되었습니다.")
    #             print(f"남은 주문 목록: {order_list2}")
    #         else:
    #             print(f"{item_to_complete}은(는) 해당 테이블의 주문 목록에 없습니다.")
    #     else:
    #         print(f"{table_number} 테이블은 주문이 없거나 이미 처리되었습니다.")

    def display_complete_orders(self):
        print("완료된 주문 목록:")
        print(self.complete_order_dict)

    # ------------------------------------------
    # 테이블 추가
    def add_table(self, table_number):
        if not self.tables.is_full():
            self.waitinglist.dequeue()
            print(f"{table_number}번 손님이 입장하셨습니다.")
            table = int(input("테이블 번호를 입력해주세요 : "))
            self.tables.enqueue(table_number)
            self.order[table_number] = [table]
            self.complete_order_dict[table_number] = [table]
        else:
            print("테이블이 다 찼습니다.")

    def remove_table(self):
        if not self.tables.is_empty():
            trigger = 0
            if self.tables.is_full():
                trigger = 1
            table_number = self.tables.dequeue()
            total_price = 0
            for i in self.order[table_number][1:]:
                total_price += self.menu[i]
            self.order.pop(table_number)
            self.complete_order_dict.pop(table_number)
            print(f"테이블 {table_number}번 정리중입니다. 총 가격: {total_price}")
            self.total_income += total_price
            if trigger == 1 and not self.waitinglist.is_full():
                self.add_table(self.waitinglist.dequeue())
        else:
            print("테이블이 모두 비었습니다.")

    # def display_tables(self):
    #     table2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
    #     print("현재 사용중인 테이블:", self.tables)
    #     print("현재 테이블 수:", len(self.tables))
    #     print("남은 테이블:", table2 - self.tables)

    def input_menus(self, name, stock):
        self.data.insert(name, int(stock))

    def delete_menu(self, name):
        self.data.delete(name)

    def is_orderable(self, menu):
        if self.data.search(menu) != 'Q':
            return True
        else:
            return False

    def after_order(self, menu):  # 주문 후 재고를 재조정합니다.
        self.data.stocks[self.data.search(menu)] -= 1
        if self.data.stocks[self.data.search(menu)] <= 0:  # 주문이 불가능해진 메뉴는 그 즉시 삭제합니다.
            self.data.delete(menu)
            del self.workqueue[menu]
