class Option:
    """ An Option type inspired by the type by the same name in OCaml and other
    functional languages. Allows a value to either exist or is None otherwise.
    The use of this type is debatable given python's dynamic types. I've added
    it because I didn't like the idea of returning None in a function that
    might also return a value, and I thought that this might make the code more
    expressive

    Example:
        def foo(num):
            if num % 2 == 0:
                return Option(num)
            else:
                return Option()
        x = foo(5)
        if x.does_contain():
            print(x.get_val())
    """

    def __init__(self, val=None):
        self.val = val
        self.type = True if val else False

    def does_contain(self):
        return self.type

    def get_val(self):
        if self.is_none():
            raise Exception("attempt to access a None value in an Option type")
        else:
            return self.val
