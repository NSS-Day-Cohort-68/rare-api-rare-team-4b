import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from json.decoder import JSONDecodeError
from views import (
    login_user,
    create_user,
    get_user,
    get_all_users,
    create_category,
    list_categories,
    retrieve_categories,
    specific_post,
    get_all_posts,
    create_tag,
    get_user_by_email,
    get_comments,
    get_single_comment,
    get_tag,
    get_all_post_tags,
    add_comment,
    delete_category,
    delete_tag,
    delete_post,
)

from helper import has_unsupported_params, missing_fields


class JSONServer(HandleRequests):
    """server class to handle incoming HTTP requests"""

    def do_GET(self):
        """handle GET requests"""

        url = self.parse_url(self.path)

        # users:
        if url["requested_resource"] == "users":

            if has_unsupported_params(
                url,
                ["first_name", "last_name", "email", "username"],
            ):
                # request contains bad data
                return self.response(
                    "Unsupported parameter specifications.",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )

            if url["pk"] != 0:
                # user id was specified
                fetched_user = get_user(url["pk"])
                if fetched_user:
                    return self.response(fetched_user, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response("{}", status.HTTP_200_SUCCESS.value)

            # user email was specified
            if "email" in url["query_params"]:
                fetched_user = get_user_by_email(url["query_params"]["email"][0])
                if fetched_user:
                    return self.response(fetched_user, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response("{}", status.HTTP_200_SUCCESS.value)

            # user id and email were not specified
            fetched_users = get_all_users()
            if fetched_users:
                return self.response(fetched_users, status.HTTP_200_SUCCESS.value)
            else:
                return self.response("[]", status.HTTP_200_SUCCESS.value)

        # posts:
        elif url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = specific_post(url["pk"])
                if response_body:
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response("{}", status.HTTP_200_SUCCESS.value)
            response_body = get_all_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        # comments:
        elif url["requested_resource"] == "comments":
            if url["pk"] != 0:
                response_body = get_single_comment(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = get_comments()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        # categories:
        elif url["requested_resource"] == "categories":
            if url["pk"] != 0:
                response_body = retrieve_categories(url["pk"])
                if response_body:
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response("{}", status.HTTP_200_SUCCESS.value)

            response_body = list_categories(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        # tags:
        elif url["requested_resource"] == "tags":
            if url["pk"] != 0:
                fetched_tag = get_tag(url["pk"])
                if fetched_tag:
                    return self.response(fetched_tag, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response("{}", status.HTTP_200_SUCCESS.value)

            response_body = get_all_post_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "post-tags":
            response_body = get_all_post_tags()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            # invalid request
            return self.response(
                "[]", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        """handle POST requests"""

        url = self.parse_url(self.path)

        if url["pk"] == 0:
            # users:
            if url["requested_resource"] == "users":
                try:
                    content_len = int(self.headers.get("content-length", 0))
                    request_body = self.rfile.read(content_len)
                    request_body = json.loads(request_body)

                    # validate request body
                    required_fields = ["first_name", "last_name", "username", "email"]
                    missing_request_fields = missing_fields(
                        request_body, required_fields
                    )

                    if missing_request_fields:
                        return self.response(
                            f"Missing required fields: {', '.join(missing_request_fields)}",
                            status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                        )

                    new_user = create_user(request_body)
                except (JSONDecodeError, KeyError):
                    # invalid request
                    return self.response(
                        "Your request is invalid JSON.",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )

                if new_user:
                    # user creation was successful
                    return self.response(
                        new_user, status.HTTP_201_SUCCESS_CREATED.value
                    )
                else:
                    # user creation was unsuccessful
                    return self.response(
                        "Failed to create user.", status.HTTP_500_SERVER_ERROR.value
                    )

            # tags:
            elif url["requested_resource"] == "tags":
                try:
                    content_len = int(self.headers.get("content-length", 0))
                    request_body = self.rfile.read(content_len)
                    request_body = json.loads(request_body)

                    # create the new tag
                    new_tag = create_tag(request_body)
                    if new_tag:
                        return self.response(
                            "{}", status.HTTP_201_SUCCESS_CREATED.value
                        )
                    else:
                        return self.response(
                            "Failed to create tag.", status.HTTP_500_SERVER_ERROR.value
                        )

                except (JSONDecodeError, KeyError):
                    # invalid request
                    return self.response(
                        "Your request is invalid JSON.",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )

            elif url["requested_resource"] == "post-tags":
                content_len = int(self.headers.get("content-length", 0))
                request_body = self.rfile.read(content_len)
                request_body = json.loads(request_body)

                # create the new tag
                new_tag = create_tag(request_body)
                if new_tag:
                    return self.response("{}", status.HTTP_201_SUCCESS_CREATED.value)
                else:
                    return self.response(
                        "Failed to create tag.", status.HTTP_500_SERVER_ERROR.value
                    )

            elif url["requested_resource"] == "comments":
                content_len = int(self.headers.get("content-length", 0))
                request_body = self.rfile.read(content_len)
                request_body = json.loads(request_body)

                successfully_added = add_comment(request_body)
                if successfully_added:
                    return self.response("{}", status.HTTP_201_SUCCESS_CREATED.value)
                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

            elif url["requested_resource"] == "categories":
                content_len = int(self.headers.get("content-length", 0))
                request_body = self.rfile.read(content_len)
                category_data = json.loads(request_body)

                new_category_id = create_category(category_data)

                if new_category_id:
                    response_body = json.dumps({"id": new_category_id})
                    return self.response(
                        response_body, status.HTTP_201_SUCCESS_CREATED.value
                    )
                else:
                    return self.response(
                        "Failed to create category", status.HTTP_500_SERVER_ERROR.value
                    )
            # login:
            elif url["requested_resource"] == "login":
                if has_unsupported_params(url) or url["pk"] != 0:
                    # request contains bad data
                    return self.response(
                        "Unsupported parameter specifications.",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
                try:
                    content_len = int(self.headers.get("content-length", 0))
                    request_body = self.rfile.read(content_len)
                    request_body = json.loads(request_body)

                    # validate request body
                    missing_request_fields = missing_fields(
                        request_body, ["username", "email"]
                    )

                    if missing_request_fields:
                        return self.response(
                            f"Missing required fields: {', '.join(missing_request_fields)}",
                            status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                        )

                    existing_user = login_user(request_body)

                    return self.response(existing_user, status.HTTP_200_SUCCESS.value)

                except (JSONDecodeError, KeyError):
                    # invalid request
                    return self.response(
                        "Your request is invalid JSON.",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
            else:
                # invalid request
                return self.response(
                    "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                )

        else:
            # incorrectly specified a primary key
            return self.response(
                'Cannot POST to a specific row. Did you mean "PUT"?',
                status.HTTP_405_METHOD_NOT_ALLOWED.value,
            )

    def do_PUT(self):
        """handle PUT requests from a client"""

        # TODO: handle PUT requests
        return self.response(
            "Feature is not yet implemented.", status.HTTP_501_NOT_IMPLEMENTED.value
        )  #!

    def do_DELETE(self):
        """handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if pk != 0:
            if url["requested_resource"] == "categories":
                deleted = delete_category(pk)
                if deleted:
                    return self.response("{}", status.HTTP_200_SUCCESS.value)

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

            elif url["requested_resource"] == "posts":
                if pk != 0:
                    deleted = delete_post(pk)
                    if deleted:
                        return self.response("{}", status.HTTP_200_SUCCESS.value)

                    return self.response(
                        "Resource not found",
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )
            else:
                return self.response("", status.HTTP_403_FORBIDDEN.value)

        else:
            # invalid request
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
