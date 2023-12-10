class Employee:
    def __init__(self,name,company,age,mobileNo,address):
        self.name = name
        self.company = company
        self.age = age
        self.mobileNo = mobileNo
        self.address = address

    def showDetails(self):
        print(f'Name {self.name}')
        print(f'mobile Number {self.mobileNo}')
        print(f'Age {self.age}')
        print(f'Address {self.address}')

class Programmer(Employee):
    def __init__(self, name, company, age, mobileNo, address,salary,level):
        super().__init__(name, company, age, mobileNo, address)
        self.salary = salary
        self.level = level
        self.role = 'Programmer'

    
    def showDetails(self):
        print(f'Name {self.name}')
        print(f'mobile Number {self.mobileNo}')
        print(f'Age {self.age}')
        print(f'Address {self.address}')
        print(f'Salary {self.salary}')
        print(f'Level {self.level}')
        print(f'Role {self.role}')


class SoftwareDeveloper(Programmer,Employee):
    def __init__(self, name, company, age, mobileNo, address, salary, level,techStack):
        super().__init__(name, company, age, mobileNo, address, salary, level)
        self.role = "FullStack Developer"
        self.techStack = techStack

    
    def showDetails(self):
        print(f'Name {self.name}')
        print(f'mobile Number {self.mobileNo}')
        print(f'Age {self.age}')
        print(f'Address {self.address}')
        print(f'Salary {self.salary}')
        print(f'Level {self.level}')
        print(f'Role {self.role}')
        print(f'Tech Stack {self.techStack}')
    

if __name__ == '__main__':
    stark = SoftwareDeveloper("stark",'google',22,'9828xxxx', 'India',"5LPA","Senior","MERN")
    stark.showDetails()

