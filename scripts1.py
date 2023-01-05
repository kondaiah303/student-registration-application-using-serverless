from dynamodb_connections import *
from difflib import get_close_matches
from boto3.dynamodb.conditions import Attr, Key


def get_student_by_phone_number():
    response = table.query(
        IndexName='phone-index',
        KeyConditionExpression=Key('phone').eq("6789123456")
    )
    print(response['Items'])


def count_of_students():

    print("Total No of students =", len(DynamodbService().scan_table_data()))


def count_of_male_students():
    response = table.scan(
        FilterExpression=Attr('gender').eq('male')
    )
    items = response['Items']
    print('No of male students =', len(items))


def count_of_female_students():
    response = table.scan(
        FilterExpression=Attr('gender').eq('female')
    )
    items = response['Items']
    print('No of female students =', len(items))


def get_all_final_year_students():
    course = input('enter the course name: ')
    course_year = int(input('enter the course_year: '))
    response = table.scan(
        FilterExpression=Attr('course').eq(course) & Attr('course_year').eq(course_year)
    )
    items = response['Items']
    print(len(items))


def get_students_data(data):
    empty_list = []
    for items in DynamodbService().scan_table_data():
        if items.get('name') == data:
            student_id = items.get('student_id')
            empty_list.append(DynamodbService().get_data(student_id))
    return empty_list


def get_all_students_names_matches():
    name = input('enter the name: ')
    student_data_list = [items.get('name').lower() for items in DynamodbService().scan_table_data()]
    student_names_list = get_close_matches(name, student_data_list)
    matching_data_list = []
    for data in student_names_list:
        for matching_data in get_students_data(data):
            matching_data_list.append(matching_data)
    response = json.dumps(matching_data_list, indent=2, cls=DecimalEncoder)
    print(response)


def main():
    get_student_by_phone_number()
    count_of_students()
    count_of_male_students()
    count_of_female_students()
    get_all_final_year_students()
    get_all_students_names_matches()


if __name__ == "__main__":
    main()
