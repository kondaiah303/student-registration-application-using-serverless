import uuid
from dynamodb_connections import *


class CodeService:
    @staticmethod
    def create_student(payload):
        """
            creating data in dynamodb
        """
        unique_id = uuid.uuid1()  # getting unique number
        update_payload = {'student_id': str(unique_id)}
        update_payload.update(payload)  # updating student_id into update_payload
        DynamodbService().put_data(update_payload)
        return {'statuscode': 200, "body": json.dumps(update_payload)}

    @staticmethod
    def get_student(payload):
        """
            Getting specific student data
        """
        student_id = payload.get('student_id')
        student_data = DynamodbService().get_data(student_id=student_id)
        response = json.dumps(student_data, cls=DecimalEncoder)
        status_code = 404  # not found
        body = {
            "message": f"student_id = {student_id} is not existed"
        }
        if response is None or response == "null":
            return {"statusCode": status_code, "body": json.dumps(body)}
        return {"statusCode": 200, "body": response}

    @staticmethod
    def get_all_student_data():
        """
            Getting all student data
        """
        stud_data = DynamodbService().scan_table_data()
        student_details_list = []
        for data in stud_data:
            student_details_list.append(data)
        response = json.dumps(student_details_list, cls=DecimalEncoder)
        return {"statusCode": 200, "body": response}

    @staticmethod
    def update_student_data(payload):
        """
            updating specific student data
        """
        return DynamodbService().update_data(payload)

    @staticmethod
    def delete_student_data(payload):
        """
            deleting specific student data
        """
        student_id = payload.get('student_id')
        student_data = DynamodbService().get_data(payload.get('student_id'))
        body = {
            "message": f"student_id = {student_id} is deleted"
        }
        if student_data is None or student_data == "null":
            body = {
                "message": f"student_id = {student_id} is not existed"
            }
            return {"statusCode": 404, "body": json.dumps(body)}
        DynamodbService().delete_data(student_id)
        return {'statusCode': 200, "body": json.dumps(body)}
