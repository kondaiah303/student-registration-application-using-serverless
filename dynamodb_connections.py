import boto3
import json
from decimal import *

dynamoDB = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamoDB.Table('StudentInfo')


class DecimalEncoder(json.JSONEncoder):

    def default(self, obj):
        """
            changing decimal to integer
        """
        # if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            # if float(obj) % 1 == 0:
            #     return int(obj)
            return int(obj)
        # otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


class DynamodbService:
    @staticmethod
    def put_data(update_payload):
        """
            Insert the Items.
        """
        print('inserting the data')
        table.put_item(
            Item={
                'student_id': update_payload['student_id'],
                'name': update_payload['name'],
                'age': update_payload['age'],
                'gender': update_payload['gender'],
                'course': update_payload['course'],
                'course_year': update_payload['course_year'],
                'address': update_payload['address'],
                'phone': update_payload['phone']
            }
        )

    @staticmethod
    def get_data(student_id: str):
        """
            Read the Items.
        """
        print('Retrieving the data')
        try:
            res = table.get_item(
                Key={
                    "student_id": student_id
                }
            )
            return res['Item']
        except KeyError:
            print('key error')

    @staticmethod
    def update_data(payload):
        """
            update the Items.
        """
        student_id = payload.get('student_id')
        payload_keys_list = [key for key in payload.keys()]  # payload dictionary keys list
        payload_values_list = [value for value in payload.values()]  # payload dictionary values list
        student_data = DynamodbService().get_data(payload.get('student_id'))
        """
            initially using loop for comparing every item in table to student_id which is passed in payload 
            and retrieving the data.
        """
        if student_data:
            for count in range(len(payload)-1):
                query = 'SET #{} = :f'.format(payload_keys_list[count+1])
                print(query)
                table.update_item(
                    Key={
                        'student_id': payload.get('student_id')
                    },
                    UpdateExpression=query,
                    ExpressionAttributeValues={
                        ':f': payload_values_list[count+1]
                    },
                    ExpressionAttributeNames={
                        "#{}".format(payload_keys_list[count+1]): "{}".format(payload_keys_list[count+1])
                    }
                )
            student_data = DynamodbService().get_data(payload.get('student_id'))
            return {'statusCode': 200, 'body': json.dumps(student_data, cls=DecimalEncoder)}
        else:
            body = {
                "message": f"student_id = {student_id} is not existed"
            }
            return {"statusCode": 404, "body": json.dumps(body)}

    @staticmethod
    def scan_table_data():
        response = table.scan()
        table_data = response['Items']
        return table_data

    @staticmethod
    def delete_data(student_id):
        """
            Delete the Items.
        """
        print('deleting the data')
        table.delete_item(
            Key={
                'student_id': student_id
            }
        )
