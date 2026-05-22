class User:
    lang = "python"

    def __init__(self, name):
        print("ishladi")
        self.name = name
        self.age = 0

    def __getattribute__(self, attr):
        print("attr ishladi")
        return super().__getattribute__(attr)

    def __getattr__(self, attr):
        return attr + " topilmadi"
    
    def __setattr__(self, attr, val):
        print("set attr")
        if attr == "age" and val < 0:
            return "cannot"
        super().__setattr__(attr, val)


ali = User("Ali")

print(ali.fam)

ali.age = -10
print(ali.age)

print(ali.name)

print(ali.__getattribute__("name"))
