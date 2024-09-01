import json


def aggregate_course_info(prereqs, course_details):
    spaced_course_code = f'{course_details["subj"]} {course_details["crse"]}' # e.g. ADMN 0001

    return {
        **course_details,
        'prereqs': list(map(lambda code: code.replace(' ', '-'), prereqs.get(spaced_course_code, {'prereqs': []})['prereqs'])),
        'descendants': [],
    }

if __name__ == '__main__':
    with open('data/catalog.json', 'r') as catalog_file, open('data/prereq_graph.json', 'r') as prereqs_file, open('data/aggregated.json', 'w') as aggregated_file:
        catalog = json.load(catalog_file)
        prereqs = json.load(prereqs_file)
        aggregated_data = {dashed_course_code: aggregate_course_info(prereqs, course_details) for dashed_course_code, course_details in catalog.items()}
        # list immediate descendants
        for course_code, course_details in aggregated_data.items():
            for prereq_code in course_details['prereqs']:
                if prereq_code in aggregated_data:
                    aggregated_data[prereq_code]['descendants'].append(course_code)
                else:
                    print(f'Invalid prereq (course does not exist): {prereq_code}')

        aggregated_file.write(json.dumps(aggregated_data, indent=4))