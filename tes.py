class Storage():

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print(key, value)



a = Storage(name = 'Name', price = 'Price')