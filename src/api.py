import os
from http import HTTPStatus
from flask import request, redirect
from flask_restful import Resource

from src.db import add_url, get_document_by_id, get_document_by_url, decrement_document_by_id
from src.check_regex import check_url_valid

BASE_URL = os.environ.get("BASE_URL")


class URLShortener(Resource):
    def post(self):
        try:
            data = request.get_json()
            url = data.get("url", None)
            num_uses = data.get("num_uses", 1)
            # check validity of url
            if url is None or url == "":
                return {"message": "URL not given."}, HTTPStatus.BAD_REQUEST
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            if not check_url_valid(url):
                return {"message": "URL is not valid."}, HTTPStatus.BAD_REQUEST

            # check if url exists in db
            # is_retrieved, data = get_document_by_url(url)
            # if not is_retrieved:
            #     return data, HTTPStatus.INTERNAL_SERVER_ERROR
            # if data:
            #     return {"url": BASE_URL + data["_id"]}, HTTPStatus.CREATED

            # add url if not exists
            is_retrieved, data = add_url(url, num_uses)
            if not is_retrieved:
                return data, HTTPStatus.INTERNAL_SERVER_ERROR
            return {"url": BASE_URL + data["_id"]}, HTTPStatus.CREATED
        except Exception as e:
            return {"message": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


class URLRedirect(Resource):
    def get(self, id):
        try:
            # check if num uses is > 0
            is_retrieved, data = get_document_by_id(id)
            if not is_retrieved:
                return data, HTTPStatus.INTERNAL_SERVER_ERROR
            if not data:
                return {"message": "URL not found."}, HTTPStatus.BAD_REQUEST
            num_uses = data["num_uses"]
            if num_uses == 0:
                return {"message": "There are no remaining uses for this URL."}, HTTPStatus.BAD_REQUEST

            # update num uses and redirect
            is_retrieved, data2 = decrement_document_by_id(id)
            if not is_retrieved:
                return data2, HTTPStatus.INTERNAL_SERVER_ERROR
            url = data["url"]
            return redirect(url, code=HTTPStatus.PERMANENT_REDIRECT)

        except Exception as e:
            return {"message": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
