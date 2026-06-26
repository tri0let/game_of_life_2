
class Parent:
    def __init__(self):
        self.num1 = 1

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.num2 = 2

def func1(list: list[Parent]) -> bool:
    if isinstance(list[0], Parent):
        return True
    else: 
        return False

func1([Child()])