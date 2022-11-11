import operator
from functools import reduce

from .Project import *


class InnovationCourse:
    def __init__(self, course_id, name):
        self.id = course_id
        self.name = name
        self.projects = []

    def find_project(self, project_id):
        for p in self.projects:
            if p.id == project_id:
                return p
        return None

    @property
    def students(self):
        return reduce(lambda curr, p: curr + p.students, self.projects, [])

    def find_student(self, student_id):
        for p in self.projects:
            for s in p.students:
                if s.id == student_id:
                    return s
        return None

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'projects': list(map(lambda p: p.to_json(), self.projects))
        }

    @staticmethod
    def from_dict(data_dict):
        crs = InnovationCourse(data_dict['id'], data_dict['name'])
        crs.projects = list(map(lambda p: Project.from_dict(p), data_dict['projects']))
        return crs
