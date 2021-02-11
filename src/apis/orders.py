# - coding: utf-8 --
import uuid
from datetime import datetime

from boto3.dynamodb.conditions import Key
from flask_restx import Namespace, fields, Resource, reqparse, inputs
import boto3

from src import success_messages, NotFoundError, error_messages
from src.custom_fields import validate_dates, EmailField, validate_payload
from src.custom_inputs import date_input

api = Namespace("Orders", description='Orders operations')

products_di = {
    "prod_1": "Lenovo i3 8gbRAM 1TB HDD",
    "prod_2": "Macbook i5 16gb RAM 500SSD",
    "prod_3": "Iphone11"
}

order_info = api.model('OrdersInfo', {
    'id': fields.String(required=True, description='Order ID', attribute="pk"),
    'product_name': fields.String(required=True, description='Product Name', attribute="product_name"),
    "order_date": fields.Date(required=True, dt_format="iso8601", attribute="order_date"),
    "user_email": fields.String(required=True, attribute="email")
})
OrderPayload = api.model('OrderPayload', {
    'product_id': fields.String(required=True, description='Product ID (prod_1, pod_2, prod_3)', example="prod_3"),
    "user_email": EmailField(required=True, description="User Email")
})

OrderListResponse = api.model('OrderListResponse', {
    "status": fields.String(default="Success"),
    "code": fields.String(default="200"),
    "message": fields.String(default=success_messages.ORDERS_LIST_RETURNED),
    "data": fields.List(fields.Nested(order_info))
})
OrderInfoResponse = api.model('OrderInfoResponse', {
    "status": fields.String(default="Success"),
    "code": fields.String(default="200"),
    "message": fields.String(default=success_messages.ORDERS_INFO_RETURNED),
    "data": fields.List(fields.Nested(order_info))
})

order_by_date_parser = reqparse.RequestParser()
order_by_date_parser.add_argument('from_date', required=False, trim=True, type=date_input, help="2020-12-31")
order_by_date_parser.add_argument('to_date', required=False, trim=True, type=date_input, help="2021-12-31")

order_by_email_parser = reqparse.RequestParser()
order_by_email_parser.add_argument("email", required=True, trim=True, type=inputs.email())


@api.route("")
class OrdersResource(Resource):
    @api.response(200, success_messages.ORDERS_LIST_RETURNED)
    @api.response(404, error_messages.ORDER_NOT_FOUND)
    @api.expect(order_by_date_parser, validate=True)
    @api.marshal_with(OrderListResponse)
    def get(self):
        """ Get ALL Orders"""
        try:
            args = order_by_date_parser.parse_args()
            from_date = args["from_date"]
            to_date = args["to_date"]
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Orders')
            scan_kwargs = dict()
            if from_date and to_date:
                validate_dates(from_date, to_date)
                scan_kwargs = {
                    'FilterExpression': Key('order_date').between(from_date, to_date)
                }

            table_response = table.scan(
                **scan_kwargs
            )
            if not table_response["Items"]:
                raise NotFoundError(error_messages.ORDER_NOT_FOUND)

            response = {
                "status": "Success",
                "code": "200",
                "message": success_messages.ORDERS_LIST_RETURNED,
                "data": table_response["Items"]
            }
            return response
        finally:
            pass

    @api.response(200, success_messages.ORDER_CREATED)
    @api.response(404, error_messages.PRODUCT_NOT_FOUND)
    @api.expect(OrderPayload, validate=True)
    @api.marshal_with(OrderInfoResponse)
    def post(self):
        """ Create New Order"""
        payload = api.payload
        validate_payload(payload, OrderPayload)
        try:

            product = products_di.get(payload["product_id"])
            if not product:
                raise NotFoundError(error_messages.PRODUCT_NOT_FOUND, errors={"product_id": error_messages.PRODUCT_NOT_FOUND})
            item = {"pk": str(uuid.uuid4()), "product_id": payload["product_id"],
                    "order_date": datetime.utcnow().isoformat(),
                    "email": payload["user_email"], "product_name": product}

            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Orders')
            table.put_item(Item=item)
            response = {
                "status": "Success",
                "code": "200",
                "message": success_messages.ORDER_CREATED,
                "data": item
            }
            return response
        finally:
            pass


@api.route("/find/email")
class OrdersByEmail(Resource):
    @api.response(200, success_messages.ORDERS_LIST_RETURNED)
    @api.response(404, error_messages.ORDER_NOT_FOUND)
    @api.expect(order_by_email_parser, validate=True)
    @api.marshal_with(OrderListResponse)
    def get(self):
        """ Get ALL Orders by Email """
        try:
            args = order_by_email_parser.parse_args()
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Orders')
            table_response = table.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(args["email"])
            )
            if not table_response["Items"]:
                raise NotFoundError(error_messages.ORDER_NOT_FOUND)

            response = {
                "status": "Success",
                "code": "200",
                "message": success_messages.ORDERS_LIST_RETURNED,
                "data": table_response["Items"]
            }
            return response
        finally:
            pass
