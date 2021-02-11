# - coding: utf-8 --

import werkzeug
from flask_restx import Namespace, Resource, reqparse

from src import success_messages
from src.custom_fields import validate_image

ns = Namespace("Files", description="Files Operations")

image_upload_parser = reqparse.RequestParser()
image_upload_parser.add_argument('profile', type=werkzeug.datastructures.FileStorage, location='files', required=True,
                                 help='Profile Image')


@ns.route("")
class ImageFileResource(Resource):
    @ns.response(200, success_messages.PROFILE_IMAGE_UPDATED)
    @ns.expect(image_upload_parser, validate=True)
    def post(self):
        """Upload Image File"""
        try:
            args = image_upload_parser.parse_args()
            validate_image(args['profile'])
            response = {"code": 200, "message": success_messages.PROFILE_IMAGE_UPDATED}
            return response
        finally:
            pass
