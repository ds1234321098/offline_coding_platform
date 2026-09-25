import student_management
import teacher_management
def student_management_menu():
    while True:
        print("\n===== STUDENT MANAGEMENT =====")
        print("1. Add student")
        print("2. Find student")
        print("3. Update student")
        print("4. Delete student")
        print("5. View all students")
        print("6. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter student name: ")
            roll_number = input("Enter roll number: ")
            semester = int(input("Enter semester: "))
            branch = input("Enter branch: ")
            password=input("Enter password: ")
            candidate = student_management.student(name=name,roll_number=roll_number,semester=semester,branch=branch,password=password)
            if student_management.add(candidate):
                print("Student added successfully.")
            else:
                print("Student with this roll number already exists.")
        elif choice == "2":
            roll_number = input("Enter roll number: ")
            candidate = student_management.read(roll_number)
            if candidate:
                print("\nStudent found:")
                print(candidate)
            else:
                print("Student not found.")
        elif choice == "3":
            roll_number = input("Enter roll number of student to update: ")
            old_student = student_management.read(roll_number)
            if old_student is None:
                print("Student not found.")
                continue
            name = input("Enter new student name: ")
            new_roll_number = input("Enter new roll number: ")
            semester = int(input("Enter new semester: "))
            branch = input("Enter new branch: ")
            password=input("Enter password: ")
            candidate = student_management.student(name=name,roll_number=new_roll_number,semester=semester,branch=branch,password=password)
            if student_management.update(roll_number, candidate):
                print("Student updated successfully.")
            else:
                print("Student update failed.")
        elif choice == "4":
            roll_number = input("Enter roll number: ")
            if student_management.delete(roll_number):
                print("Student deleted successfully.")
            else:
                print("Student not found.")
        elif choice == "5":
            students = student_management.get_all()
            if len(students) == 0:
                print("No students found.")
            else:
                print("\n===== ALL STUDENTS =====")
                for candidate in students:
                    print(candidate)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")
def teacher_management_menu():
    while True:
        print("\n===== TEACHER MANAGEMENT =====")
        print("1. Add teacher")
        print("2. Find teacher")
        print("3. Update teacher")
        print("4. Delete teacher")
        print("5. View all teachers")
        print("6. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter teacher name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            candidate = teacher_management.teacher(name=name,username=username,password=password)
            if teacher_management.add(candidate):
                print("Teacher added successfully.")
            else:
                print("Teacher with this username already exists.")
        elif choice == "2":
            username = input("Enter username: ")
            candidate = teacher_management.read(username)
            if candidate:
                print("\nTeacher found:")
                print(candidate)
            else:
                print("Teacher not found.")
        elif choice == "3":
            username = input("Enter username of teacher to update: ")
            old_teacher = teacher_management.read(username)
            if old_teacher is None:
                print("Teacher not found.")
                continue
            name = input("Enter new teacher name: ")
            new_username = input("Enter new username: ")
            password = input("Enter new password: ")
            candidate = teacher_management.teacher(name=name,username=new_username,password=password)
            if teacher_management.update(username, candidate):
                print("Teacher updated successfully.")
            else:
                print("Teacher update failed.")
        elif choice == "4":
            username = input("Enter username: ")
            if teacher_management.delete(username):
                print("Teacher deleted successfully.")
            else:
                print("Teacher not found.")
        elif choice == "5":
            teachers = teacher_management.get_all()
            if len(teachers) == 0:
                print("No teachers found.")
            else:
                print("\n===== ALL TEACHERS =====")
                for candidate in teachers:
                    print(candidate)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")
def main():
    while True:
        print("\n==============================")
        print(" UNIVERSITY MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Student management")
        print("2. Teacher management")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            student_management_menu()
        elif choice == "2":
            teacher_management_menu()
        elif choice == "3":
            print("Exiting management system.")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    main()