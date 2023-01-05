from project_code import *


def create_student_handler(request, context):
    """
        creating data in dynamodb
    """
    payload = json.loads(request.get('body'))       # python object

    return CodeService().create_student(payload)


def get_student_handler(request, context):
    """
        Getting specific student data
    """
    payload = request.get("queryStringParameters")
    return CodeService().get_student(payload)


def get_all_student_data_handler(request, context):
    """
        Getting all student data
    """
    return CodeService().get_all_student_data()


def update_student_data_handler(request, context):
    """
        updating specific student data
    """
    payload = json.loads(request.get('body'))
    return CodeService().update_student_data(payload)


def delete_student_data_handler(request, context):
    """
        deleting specific student data
    """
    payload = json.loads(request.get('body'))
    return CodeService().delete_student_data(payload)






