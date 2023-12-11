class A:
    def get_num1_data(self):
        self.num1 = int(input("Enter First Number : "))

class B(A):
    def get_num2_data(self):
        self.num2 = int(input("Enter Second Number : "))

class C(B):
    def get_num3_data(self):
        self.num3 = int(input("Enter Third Number : "))
    
    def show(self):
        print(f"Number's are {self.num1, self.num2, self.num3}")

    def sum(self):
        print(f"sum = {self.num1 + self.num2 + self.num3}") 
    

if __name__ == "__main__":
    obj = C()
    obj.get_num1_data()
    obj.get_num2_data()
    obj.get_num3_data()
    obj.show()
    obj.sum()
