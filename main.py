import string
from lxml import etree
import time
import pyperclip

class Subject:

    def __init__(self, id:int, code:string, name:string, model:string, workload:int, dependencies:list, semester:int, opt:string) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.model = model
        self.workload = workload
        self.dependencies = dependencies
        self.semester = semester
        self.opt = opt

    def print(self) -> None:
        print("--------------------------------")
        print(f"{self.id},{self.code},{self.name},{self.model},{self.workload},{self.dependencies},{self.semester}, {self.opt}")
        print("--------------------------------")

def get_course_subjects() -> dict:
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
    subject_id = 1
    for atual_semester in range(1, semesters + 1):
        amount_subjects = 0
        while(True):
            amount_subjects += 1
            elem = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{amount_subjects}]")
            if elem == []:
                amount_subjects -= 1
                break
        for atual_subject in range(amount_subjects):
            #get subject info
            try:
                subject_opt = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[2]/font/a")[0].text
            except:
                subject_opt = "Obrigatória"
            try:
                subject_code = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[3]/font/a[2]")[0].text
            except:
                subject_code = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[3]/font/a[1]")[0].text
            subject_name = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[4]/font")[0].text
            subject_model = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[5]/font")[0].text
            subject_workload = int(root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[12]/font")[0].text.replace(" horas ", ""))
            subject_dependecies = []
            atual_dependencie = 1
            while(True):
                try:
                    new_dependencie = root.xpath(f"/html/body/table/tbody[{atual_semester}]/tr[{atual_subject + 1}]/td[13]/font/a[{atual_dependencie}]")
                    subject_dependecies.append(new_dependencie[0].text)
                    atual_dependencie += 1
                except:
                    break
            #save subject info
            new_subject = Subject(subject_id, subject_code, subject_name, subject_model, subject_workload, subject_dependecies, atual_semester, subject_opt)
            # new_subject.print()
            dependencies[subject_code] = new_subject
            subject_id += 1
    return dependencies

if __name__ == "__main__":
    dependencies = get_course_subjects()
    #começa a criar o grafo
    course_graph = ""
    for i in dependencies.values():
        if i.opt != "Obrigatória":
            atual_subject_graph_name = f"{i.name} OPCIONAL"
        else:
            atual_subject_graph_name = f"{i.name} OBRIGATÓRIA"



        if i.dependencies == []:
            new_direction = f"{atual_subject_graph_name}-{atual_subject_graph_name}\n"
            course_graph += new_direction
        else:
            for j in i.dependencies: #ittera entre as dependencias
                atual_subject_dependencie_graph_name = dependencies[j].name
                if i.opt != "Obrigatória":
                    atual_subject_dependencie_graph_name = f"{atual_subject_dependencie_graph_name} OPCIONAL"
                else:
                    atual_subject_dependencie_graph_name = f"{atual_subject_dependencie_graph_name} OBRIGATÓRIA"




                new_direction = f"{atual_subject_dependencie_graph_name}>{atual_subject_graph_name}\n"
                course_graph += new_direction



    print(course_graph)
    pyperclip.copy(course_graph)