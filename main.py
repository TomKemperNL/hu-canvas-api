import json

from canvasapi import *
from credentials import token
import datetime

import re

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/', token)

# Ik gebruik op Windows Fiddler als debugger, moet nog even een manier vinden requests beter te debuggen
# api = CanvasAPI('https://canvas.hu.nl/api/v1/', token, proxy)


with open('inno-ids.json') as f:
    raw = json.load(f)
    this_year_id = raw['main']
    project_ids = raw['projects']
    this_year_raw = api.get(f'courses/{this_year_id}')
    this_year = InnovationCourse(this_year_raw['id'], this_year_raw['name'])

holistiq = HolisticAPI(api, this_year, "SD")
holistiq.init(project_ids)  # TODO: uitzoeken hoe dit netter kan, zo'n magische method call is niks natuurlijk

all_todos = []
for project in this_year.projects:
    (grades_per_student, todos) = holistiq.get_grades_in_project(project, [
        'Gedreven ontwerpen',
        'Gedistribueerde systemen'
    ])
    all_todos = all_todos + todos

    print(project.name)
    for student in grades_per_student.keys():
        print('\t' + student)
        total_submissions = 0
        last_submission = None
        for assignment in grades_per_student[student].keys():
            submissions = grades_per_student[student][assignment]
            total_submissions += len(submissions.values())

            grades = []
            if submissions is not None and len(submissions) > 0:
                last = max(map(lambda s: s.submitted_at, submissions.values()))
                grades = list(map(lambda s: s.grade, submissions.values()))
                last_submission = last if last_submission is None else max([last_submission, last])

            print(f'\t\t{assignment}: {", ".join(grades)}')
        print('')
        print(f'\t\tAantal opleveringen: {total_submissions}')
        last_formatted = "-" if last_submission is None else last_submission.strftime("%d %b")
        print(f'\t\tLaatste opleveringen: {last_formatted}')

opdrachten = [
    'Tennis Data case (SQL)'
]

(grades_per_student, todos) = holistiq.get_inno_grades(opdrachten)


for todo in all_todos:
    print(todo)
