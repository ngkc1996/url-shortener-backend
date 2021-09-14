import os
from http import HTTPStatus
from flask import request, redirect
from flask_restful import Resource

from src.db import add_url, get_document_by_id, get_document_by_url
from src.check_regex import check_url_valid

BASE_URL = os.environ.get("BASE_URL")


class URLShortener(Resource):
    def post(self):
        try:
            data = request.get_json()
            url = data.get("url", None)
            # check validity of url
            if url is None or url == "":
                return {"message": "URL not given."}, HTTPStatus.BAD_REQUEST
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            if not check_url_valid(url):
                return {"message": "URL is not valid."}, HTTPStatus.BAD_REQUEST

            # check if url exists in db
            is_retrieved, data = get_document_by_url(url)
            if not is_retrieved:
                return data, HTTPStatus.INTERNAL_SERVER_ERROR
            if data:
                return {"url": BASE_URL + data["_id"]}, HTTPStatus.CREATED

            # add url if not exists
            is_retrieved, data = add_url(url)
            if not is_retrieved:
                return data, HTTPStatus.INTERNAL_SERVER_ERROR
            return {"url": BASE_URL + data["_id"]}, HTTPStatus.CREATED
        except Exception as e:
            return {"message": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


class URLRedirect(Resource):
    def get(self, id):
        try:
            is_retrieved, data = get_document_by_id(id)
            if not is_retrieved:
                return data, HTTPStatus.INTERNAL_SERVER_ERROR
            if data:
                url = data["url"]
                return redirect(url, code=HTTPStatus.PERMANENT_REDIRECT)
            else:
                return {"message": "URL not found."}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {"message": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
