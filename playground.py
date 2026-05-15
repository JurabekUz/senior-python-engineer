
def coroutine():
    print("coroutine started")
    x = 5
    while True:
        x = yield x
        print("you entered", x)

cor = coroutine()
print(next(cor))
print(next(cor))
cor.send("hello")

