"""
Below is a Student class and its subclass, GraduateStudent.
These represent students in a record system like ACORN.

Read the docstring for Student, GraduateStudent, and their methods.

Your tasks are listed below.

    1.  Look at the if __name__ == '__main__' block.
        We have written some client code that *should* work. However, there
        is a bug. Your task is to find and fix the bug.

    2.  GraduateStudents must earn a grade of 70 or higher to earn credit for
        a course. Implement this change, but do NOT modify the complete_course
        method in the Student class.

        Run test_example() and make sure it passes on your revised code.
        If it does not pass, make sure:
            - You fixed the bug in Task 1
            - You did not modify Student.complete_course


Submit your code on MarkUs and run the automated self-test.
Your grade on the quiz will be based solely on the results of the self-test.
(i.e. if you pass all of the tests, you get full marks on the quiz.)
"""
from typing import Dict, List
import pytest


class Student:
    """A university student.

    === Instance attributes ===
    st_num:
        This student's student number.
    name:
        This student's name.
    courses:
        A dictionary containing the courses this student has taken.
        Each key is a course code like 'csc148',
        and its value is the student's grade in the course.
    credits:
        The number of credits this student has earned.
        One credit is earned each time the student passes a course.
    """
    st_num: int
    name: str
    courses: Dict[str, int]
    credits: int

    def __init__(self, st_num: int, name: str) -> None:
        """Initialize this student.
        """
        self.st_num = st_num
        self.name = name
        self.courses = {}
        self.credits = 0

    def complete_course(self, course: str, grade: int) -> None:
        """Record the fact that this student has completed a course.
        """
        self.courses[course] = grade
        if grade >= 50:
            self.credits += 1


class GraduateStudent(Student):
    """A graduate student.

    === Additional instance attributes ===
    supervisor:
        The name of this graduate student's supervisor.
    meetings:
        The dates on which this graduate student's thesis committee met.
        Each date is represented as a str.
    """
    supervisor: str
    meetings: List[str]

    def __init__(self, st_num: int, name: str, supervisor: str) -> None:
        """Initialize this graduate student.
        """
        Student.__init__(self, st_num, name)
        self.supervisor = supervisor
        self.meetings = []

    def complete_course(self, course: str, grade: int) -> None:
        """Record the fact that this student has completed a course.
        """
        self.courses[course] = grade
        if grade >= 70:
            self.credits += 1


def test_example():
    """Test that a Student and a Graduate student can be made and that
    credits are properly recorded.

    Do not change this function.
    You should only run this test case after you finish Task 2.
    """
    s = Student(0, 'Alice')
    s.complete_course('csc148', 50)
    assert s.credits == 1
    assert s.courses['csc148'] == 50

    g = GraduateStudent(1, 'Bob', 'Professor Horton')
    g.complete_course('csc148', 60)
    assert g.credits == 0
    assert g.courses['csc148'] == 60

    g.complete_course('csc207', 70)
    assert g.credits == 1
    assert g.courses == {'csc148': 60, 'csc207': 70}


if __name__ == '__main__':
    # The code below should run properly, but it doesn't.
    # Find the bug and fix it. Do not change any of the lines below.
    g = GraduateStudent(1234567, 'Ursula', 'Professor Fleet')
    g.complete_course('csc148', 92)
    g.supervisor = 'Professor McIlraith'

    pytest.main(['quiz3.py'])
