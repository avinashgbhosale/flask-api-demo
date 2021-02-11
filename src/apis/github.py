# - coding: utf-8 --
import requests
from flask_restx import Namespace, fields, Resource, reqparse, inputs

from src import success_messages, NotFoundError, error_messages
from src.costants import GITHUB_USER_SEARCH_URL, GITHUB_REPOS_BY_USER_URL


api = Namespace("Github", description='Github operations')


GithubUserInfo = api.model('GithubUserInfo', {
    'user_name': fields.String(required=True, attribute="login"),
    'avatar_url': fields.String(required=True, attribute="avatar_url"),
    'url': fields.String(required=True, attribute="url"),
    'profile_url': fields.String(required=True, attribute="html_url"),
    'repos_url': fields.String(required=True, attribute="repos_url")
})
GithubUserList = api.model('GithubUserList', {
    "status": fields.String(default="Success"),
    "code": fields.String(default="200"),
    "message": fields.String(default=success_messages.GITHUB_USERS_LIST_RETURNED),
    "data": fields.List(fields.Nested(GithubUserInfo))
})
GithubUserInfoResponse = api.model('GithubUserInfoResponse', {
    "status": fields.String(default="Success"),
    "code": fields.String(default="200"),
    "message": fields.String(default=success_messages.GITHUB_USERS_INFO_RETURNED),
    "data": fields.List(fields.Nested(GithubUserInfo))
})
GitReposInfo = api.model('GitReposInfo', {
    'name': fields.String(required=True, attribute="name"),
    'full_name': fields.String(required=True, attribute="full_name"),
    'private': fields.Boolean(required=True, attribute="private"),
    'owner': fields.Nested(GithubUserInfo, skip_none=True)
})
GitReposList = api.model('GitReposList', {
    "status": fields.String(default="Success"),
    "code": fields.String(default="200"),
    "message": fields.String(default=success_messages.GITHUB_REPOS_LIST_RETURNED),
    "data": fields.List(fields.Nested(GitReposInfo))
})
users_search_parser = reqparse.RequestParser()
users_search_parser.add_argument('q', required=True, trim=True, type=str, help="Search Users By Name, Email")


@api.route("/users")
class UsersResource(Resource):
    @api.response(200, success_messages.GITHUB_USERS_LIST_RETURNED)
    @api.response(404, error_messages.USER_NOT_FOUND)
    @api.expect(users_search_parser, validate=True)
    @api.marshal_with(GithubUserList)
    def get(self):
        """ Search Github Users By Name, Email"""
        try:
            args = users_search_parser.parse_args()
            r = requests.get(url=GITHUB_USER_SEARCH_URL, params=args)
            res_json = r.json()
            if r.status_code == 200 and res_json['total_count'] > 0:
                items = res_json["items"]
            else:
                raise NotFoundError(error_messages.USER_NOT_FOUND)
            response = {
                "status": "Success",
                "code": "200",
                "message": success_messages.GITHUB_USERS_LIST_RETURNED,
                "data": items
            }
            return response
        finally:
            pass


@api.route("/users/<user_name>/repos")
class GithubReposByUserResource(Resource):
    @api.response(200, success_messages.GITHUB_REPOS_LIST_RETURNED)
    @api.response(404, error_messages.GITHUB_REPOS_NOT_FOUND)
    @api.marshal_with(GitReposList)
    def get(self, user_name):
        """ Get Github repos by User"""
        try:
            url = GITHUB_REPOS_BY_USER_URL.format(user_name)
            r = requests.get(url)
            res_json = r.json()
            if r.status_code == 200 and len(res_json) > 0:
                items = res_json
            else:
                raise NotFoundError(error_messages.GITHUB_REPOS_NOT_FOUND)
            response = {
                "status": "Success",
                "code": "200",
                "message": success_messages.GITHUB_REPOS_LIST_RETURNED,
                "data": items
            }
            return response
        finally:
            pass
