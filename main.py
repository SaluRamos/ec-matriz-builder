from lxml import etree
import time

with open("matriz.html", "r", encoding="utf-8") as f:
    matrix_html = f.read()

dependencies = {}
root = etree.HTML(matrix_html)
# information_columns = {13:{"path":"/font/a[2]", "element":"text"}}



semesters = 0
while(True):
    semesters += 1
    elem = root.xpath(f"/html/body/table/tbody[{semesters}]")
    if elem == []:
        semesters -= 1
        break
    dependencies[semesters] = {"amount_subjects":0}
print(f"existem {len(dependencies)} semestres")


subject_id = 1
for i in range(1, semesters + 1):
    while(True):
        dependencies[i]['amount_subjects'] += 1
        elem = root.xpath(f"/html/body/table/tbody[{i}]/tr[{dependencies[i]['amount_subjects']}]")[0]
        if elem == []:
            dependencies[i]['amount_subjects'] -= 1
            break
        dependencies[i]['subjects'] = {}
    print(f"semestre {i} possui {dependencies[i]['amount_subjects']} matérias")
    for j in range(1, dependencies[i]['amount_subjects'] + 1):
        for k in range(6):
            if k == 0:
                elem = root.xpath(f"/html/body/table/tbody[{i}]/tr[{j}]/td/font/a[3]")[0].text
                dependencies[i]['subjects'][subject_id] = f"{elem}"
            elif k == 1 or k == 2 or k == 3 or k == 4:
                elem = root.xpath(f"/html/body/table/tbody[{i}]/tr[{j}]/td/font")[0].text
                dependencies[i]['subjects'][subject_id] = f"{elem}"
            elif k == 6:
                elem = root.xpath(f"/html/body/table/tbody[{i}]/tr[{j}]/td/font/a[2]")[0].text
                dependencies[i]['subjects'][subject_id] = f"{elem}"
            subject_id += 1
print(dependencies)