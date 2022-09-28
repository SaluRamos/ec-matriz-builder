import string
from tokenize import String
from lxml import etree
import time
import sys

class Subject:

    def __init__(self, id:int, opt:string, code:string, name:string, model:string, workload:string, dependencies:list, semester:int) -> None:
        self.id = id
        self.opt = opt
        self.code = code
        self.name = name
        self.model = model
        self.workload = workload
        self.dependencies = dependencies
        self.semester = semester

if __name__ == "__main__":
    with open("matriz.html", "r", encoding="utf-8") as f:
        matrix_html = f.read()

    dependencies = {}
    root = etree.HTML(matrix_html)

    semesters = 0
    while(True):
        semesters += 1
        elem = root.xpath(f"/html/body/table/tbody[{semesters}]")
        if elem == []:
            semesters -= 1
            break
        dependencies[semesters] = {"amount_subjects":0, "subjects":[]}
    print(f"existem {len(dependencies)} semestres")

    subject_id = 1
    for atual_semester in range(1, semesters + 1):
        while(True):
            dependencies[atual_semester]['amount_subjects'] += 1
            elem = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{dependencies[atual_semester]['amount_subjects']}]")
            if elem == []:
                dependencies[atual_semester]['amount_subjects'] -= 1
                break
        for atual_subject in range(dependencies[atual_semester]['amount_subjects']):
            try:
                subject_opt = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[2]/font/a")[0].tiptitle
            except:
                subject_opt = "Obrigatória"
            try:
                subject_code = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[3]/font/a[2]")[0].text
            except:
                subject_code = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[3]/font/a[1]")[0].text
            subject_name = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[4]/font")[0].text
            subject_model = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[5]/font")[0].text
            subject_workload = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[12]/font")[0].text.strip()
            subject_dependecies = []
            atual_dependencie = 1
            while(True):
                try:
                    new_dependencie = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[13]/font/a[{atual_dependencie}]")
                    print(f"nova dependencia na materia {atual_subject} do semestre {atual_semester}: {new_dependencie[0].text}")
                    subject_dependecies.append(new_dependencie[0].text)
                    atual_dependencie += 1
                except:
                    break
            new_subject = Subject(subject_id, subject_opt, subject_code, subject_name, subject_model, subject_workload, subject_dependecies, atual_semester)
            dependencies[atual_semester]['subjects'].append(new_subject)
            subject_id += 1
        print(f"semestre {atual_semester + 1} possui {len(dependencies[atual_semester]['subjects'])} matérias")
    print(dependencies)