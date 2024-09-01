import json

def aggregate_course_info(prereqs, course_details):
    spaced_course_code = f'{course_details["subj"]} {course_details["crse"]}' # e.g. ADMN 0001

    return {
        **course_details,
        'prereqs': list(map(lambda code: code.replace(' ', '-'), prereqs.get(spaced_course_code, {'prereqs': []})['prereqs'])),
        'descendants': [],
        'total_descendant_count': None,
    }

def calculate_descendant_count(aggregated_data, course_code):
    course_details = aggregated_data[course_code]
    if course_details['total_descendant_count'] is not None:
        # already calculated, include this course
        return 1 + course_details['total_descendant_count']
    # base case: no descendants
    # otherwise calculate recursively
    total_count = 0 # 1 for this course
    for descendant_code in course_details['descendants']:
        total_count += calculate_descendant_count(aggregated_data, descendant_code)
    aggregated_data[course_code]['total_descendant_count'] = total_count
    return 1 + total_count # include this course in return

if __name__ == '__main__':
    max_descendant = ('', -1)
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

        # calculate total count of descendants
        for course_code in aggregated_data.keys():
            max_descendant = max(
                (course_code, calculate_descendant_count(aggregated_data, course_code)),
                max_descendant,
                key=lambda code_count_pair: code_count_pair[1],
            )

        aggregated_file.write(json.dumps(aggregated_data, indent=4))
        print(f'the maximum number of descendants is {max_descendant[0]} at {max_descendant[1]}!')