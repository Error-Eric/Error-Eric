"""
Today's task is to construct a predicted grade / gpa converter.
To make things simpler, we assume that each task is calculated individually.
"""

class assignment:
    def __init__(self, point: int, totalpoint: int):
        self.point = point
        self.total = totalpoint
    def score(self) -> int:
        percentage = self.point / self.total
        if 0.85 <= percentage <= 1.0 : return 7
        elif 0.75 <= percentage < 0.85: return 6
        elif 0.65 <= percentage < 0.75: return 5
        elif 0.55 <= percentage < 0.65: return 4
        elif 0.45 <= percentage < 0.55: return 3
        elif 0.35 <= percentage < 0.45: return 2
        else : return 1
    # Other functions

class subject: 
    def __init__(self):
        self.amlist = []
    def add_assignment(self, ax : assignment):
        self.amlist.append(ax)
    def gpa(self) -> float:
        tpoint = 0
        ttot = 0
        for ax in self.amlist:
            tpoint += ax.point

            ttot += ax.total
        return assignment(tpoint, ttot).score()
    # Other functionss


Chinese = subject()
Chinese.add_assignment(assignment(4, 5))
Chinese.add_assignment(assignment(3, 4))
print(Chinese.gpa())

"""
Task: implement the method:
Output the overall percentage and the percentage mark of each assignment.
Exapmle:
print(Chinese.percentage())
>[0.78] 0.80 0.75 
"""