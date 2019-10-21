def something(val1, *otros):
    print(val1)
    for val in otros:
        print(val)


something(1, 2, 3, 4, 5)
