while True:
    print("====== 水稻成本配置管理器 ======")
    print("1. 查看农资成本")
    print("2. 修改农资成本")
    print("0. 退出")

    choice = input("请选择功能：")

    if choice == "1":
        print("你选择了：查看农资成本")

    elif choice == "2":
        print("你选择了：修改农资成本")

    elif choice == "0":
        print("程序已退出。")
        break

    else:
        print("输入错误，请重新选择。")

    print()