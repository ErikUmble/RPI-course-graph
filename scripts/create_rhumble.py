
import json
from openpyxl import load_workbook, Workbook

headers = ["id", "type", "name", "short name", "student rating", "credits", "course link", "stroke::", "radius::", "r::", "rel::dir::has prerequisite of", "rel::undir::has corequisite of", "rel::parent::belongs to", "fill::", "is_node::"]
row_data = []

def create_rhumble():

    # load prereq data 
    with open("./data/prereq_graph.json", "r") as f:
        for course_id, course_info in json.load(f).items():
            row_data.append(
                {
                    "id": course_id,
                    "name": course_info["title"],
                    "rel::dir::has prerequisite of": "; ".join(course_info["prereqs"]),
                }
            )

    # add other data
    for row in row_data:
        row["type"] = "Course"
        row["short name"] = row["name"]
        row["student rating"] = 0
        row["credits"] = 4
        row["course link"] = ""
        row["stroke::"] = "#000000"
        row["radius::"] = 10
        row["r::"] = 10
        row["rel::undir::has corequisite of"] = ""
        row["rel::parent::belongs to"] = ""
        row["fill::"] = "#FFFFFF"
        row["is_node::"] = "TRUE"

    # add root node
    row_data.append(
        {
            "id": "root",
            "type": "root",
            "name": "RPI",
            "short name": "RPI",
            "rel::dir::has prerequisite of": "",
        }
    )

    # add departments
    for department in ["CSCI", "MATH", "PHYS", "ECSE", "ENGR", "HASS", "ARCH", ]:
        row_data.append(
            {
                "id": department,
                "type": "Department",
                "name": department,
                "short name": department,
                "rel::dir::has prerequisite of": "",
            }
        )

    wb = Workbook()
    wb.create_sheet("rhumble")
    ws = wb["rhumble"]

    # add headers 
    for i, header in enumerate(headers):
        ws.cell(row=1, column=i+1, value=header)

    # add data
    for i, data in enumerate(row_data):
        for j, key in enumerate(headers):
            ws.cell(row=i+2, column=j+1, value=data.get(key, ""))

    # save to file
    wb.save("./rhumble.xlsx")

if __name__ == "__main__":
    create_rhumble()