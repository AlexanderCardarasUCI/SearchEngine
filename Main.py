from Indices import Query

# 10,000 x 20 x 28 = 5,600,000 = 5.6M

from GUI import WindowManager

# def Search():
#     urls = Query.search(gui.searchEntry.get())
#     gui.remove_labels()
#     for url in urls:
#         gui.add_label(url)
#         print(url)
#     print("=====================================\n\n")
#
#
# gui = WindowManager.WindowManager("Search Engine", 1000, 600, Search)
# gui.run()


while True:
    query = input("Enter Query: ")
    if query == "exit":
        break
    urls = Query.search(query)
    for url in urls:
        print(url)

    print("=====================================\n\n")
