import management

# main 함수 정의
def main():
    restaurant = management.ManagementSystem()

    while True:
        # 사용자에게 작업 선택 받기
        work = input("작업을 입력하세요:\n 0:메뉴\n 1:대기\n 2:주문\n 3:서빙\n 4:테이블 계산\n 10:장사종료\n")

        if work == '0':
            # 메뉴 작업 선택
            sub_work = input("작업을 입력하세요:\n 0:메뉴추가\n 1:메뉴제거\n 2:메뉴판보기\n")
            if sub_work == '0':
                restaurant.add_menu()
            elif sub_work == '1':
                restaurant.subtract_menu()
            elif sub_work == '2':
                restaurant.display_menu()
            else:
                print("잘못된 입력입니다.")

        elif work == '1':
            # 대기열 작업 선택
            sub_work = input("작업을 입력하세요:\n 0:대기열 추가\n 1:대기열 보기\n")
            if sub_work == '0':
                restaurant.add_waiting()
            elif sub_work == '1':
                restaurant.display_waiting()

        elif work == '2':
            # 주문 작업 선택
            sub_work = input("작업을 입력하세요:\n 0:주문하기\n 1:주문내역 보기\n 2:서빙된 음식\n")
            if sub_work == '0':
                restaurant.take_order()
            elif sub_work == '1':
                restaurant.display_orders()
            elif sub_work == '2':
                restaurant.display_complete_orders()

        elif work == '3':
            # 서빙 작업
            restaurant.kitchen_out()

        elif work == '4':
            # 무조건 첫 번째 손님을 뺀다고 가정했기에...
            restaurant.remove_table()

        elif work == '10':
            # 장사 종료
            print(f"오늘의 총 수입 : {restaurant.total_income}")
            break

        else:
            print("잘못된 입력입니다.")


# main 함수 호출
main()
