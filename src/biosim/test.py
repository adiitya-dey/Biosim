import random
if __name__ == '__main__':

    list1 = [{'age': 5, 'weight': 10}, {'age': 4, 'weight': 100}, {'age': 2, 'weight': 60}]
    list2 = [{'age': 1000, 'weight': 10}, {'age': 4000, 'weight': 100}, {'age': 2000, 'weight': 60}, {'age': 6000, 'weight': 60}]
    list4 = [(0, {'age': 5, 'weight': 20, 'fitness': 0.9983}), (1, {'age': 5, 'weight': 20, 'fitness': 0.9983})]

    list3 = list1 + list4
    # list1.sort(key=lambda x :x['weight'])
    # list1.clear()
    # print(list1)
    (x, y) = random.choice(list4)
    print(x)
    print(y)

    # # delete_list = []
    # for _ in range(5):
    #     print(random.choice(list(enumerate(list3))))

    #
    # for i, x in enumerate(list1[::-1]):
    #     print(len(list1)-i-1,x)