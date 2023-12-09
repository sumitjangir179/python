class Student:
    # constructor -> automatically call when an object created
    def __init__(self,name,fatherName,mobileNumber,age,address):
        # class attribute
        self.name = name
        self.fatherName = fatherName
        self.mobileNumber= mobileNumber
        self.age = age
        self.address = address
     
    # class methods
    def showDetails(self):
        print(f'Name {self.name}')
        print(f'Father Name {self.fatherName}')
        print(f'mobile Number {self.mobileNumber}')
        print(f'Age {self.age}')
        print(f'Address {self.address}')
    
    def library(self):
        print(f"I am {self.name} I can access library")
    
    def computerLab(self):
        print(f"I am {self.name} I can access computer lab")


    
if __name__ == '__main__':
    # object of Student class
    stark = Student('Stark','Howard','9828XXXX',22,'Las Vagas')
    stark.showDetails()
    stark.library()
    stark.computerLab()
    print(stark.mobileNumber)