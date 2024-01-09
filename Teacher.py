def teach(func):
    def wrapper(*args, print_steps=True, **kwargs):
        generator = func(*args, **kwargs)
        try:
            while True:
                step = next(generator)
                if print_steps:
                    print(step)
        except StopIteration as stop_iteration:
            return stop_iteration.value if hasattr(stop_iteration, 'value') else None
        except TypeError:
            return generator

    return wrapper
