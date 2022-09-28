import string
from lxml import etree
import time

class Subject:

    def __init__(self, id:int, code:string, name:string, model:string, workload:int, dependencies:list, semester:int) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.model = model
        self.workload = workload
        self.dependencies = dependencies
        self.semester = semester

    def print(self) -> None:
        print("--------------------------------")
        print(f"{self.id},{self.code},{self.name},{self.model},{self.workload},{self.dependencies},{self.semester}")
        print("--------------------------------")

def get_course_subjects() -> list:
    with open("matriz.html", "r", encoding="utf-8") as f:
        matrix_html = f.read()
    dependencies = []
    root = etree.HTML(matrix_html)
    semesters = 0
    while(True):
        semesters += 1
        elem = root.xpath(f"/html/body/table/tbody[{semesters}]")
        if elem == []:
            semesters -= 1
            break
        dependencies[semesters] = {"amount_subjects":0, "subjects":[]}
    subject_id = 1
    for atual_semester in range(1, semesters + 1):
        amount_subjects = 0
        while(True):
            amount_subjects += 1
            elem = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{amount_subjects}]")
            if elem == []:
                amount_subjects -= 1
                break
        for atual_subject in range(amount_subjects):
            #get subject info
            try:
                subject_code = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[3]/font/a[2]")[0].text
            except:
                subject_code = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[3]/font/a[1]")[0].text
            subject_name = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[4]/font")[0].text
            subject_model = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[5]/font")[0].text
            subject_workload = int(root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[12]/font")[0].text.replace(" horas ", ""))
            subject_dependecies = []
            atual_dependencie = 1
            while(True):
                try:
                    new_dependencie = root.xpath(f"/html/body/table/tbody[{atual_semester + 1}]/tr[{atual_subject + 1}]/td[13]/font/a[{atual_dependencie}]")
                    subject_dependecies.append(new_dependencie[0].text)
                    atual_dependencie += 1
                except:
                    break
            #save subject info
            new_subject = Subject(subject_id, subject_code, subject_name, subject_model, subject_workload, subject_dependecies, atual_semester)
            new_subject.print()
            dependencies.append(new_subject)
            subject_id += 1
    return dependencies

if __name__ == "__main__":
    dependencies = get_course_subjects()
