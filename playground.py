import time


def timer_dec(base_fn):

    def enhanced_fn(*args, **kwargs):
        start_time = time.time()

        result = base_fn(*args, **kwargs)

        end_time = time.time()
        print(f"Time taken: {end_time - start_time}")
        return result
    
    return enhanced_fn

@timer_dec
def brew_tea(tea_type, steep_time):
    print(f"start brewing {tea_type}")
    time.sleep(steep_time)
    print(f"{tea_type} is ready")
    return f"{tea_type} is ready"


@timer_dec
def make_matcha():
    print("start making matcha")
    time.sleep(2)
    print("matcha is ready")
    return "matcha is ready"

brew_tea(tea_type="green", steep_time=2)
print(make_matcha())
