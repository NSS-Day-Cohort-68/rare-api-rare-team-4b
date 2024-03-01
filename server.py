import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from json.decoder import JSONDecodeError
from views import login_user, create_user, get_user, get_all_users, create_category, list_categories, retrieve_categories, specific_post, get_all_posts

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
                [
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password",
                    "created_on",
                ],
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
                    return self.response(
                        "{}", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )

            # user id was not specified
            fetched_users = get_all_users()
            if fetched_users:
                return self.response(fetched_users, status.HTTP_200_SUCCESS.value)
            else:
                return self.response(
                    "[]", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                )

        # posts:
        elif url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = specific_post(url["pk"])
                if response_body:
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response(
                        "{}", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )
            response_body = get_all_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        # comments:
        elif url["requested_resource"] == "comments":
            # TODO: handle GET comments
            return self.response(
                "Feature is not yet implemented.", status.HTTP_501_NOT_IMPLEMENTED.value
            )  #!
        # categories:
        elif url["requested_resource"] == "categories":
            if url["pk"] != 0:
                response_body = retrieve_categories(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_categories(url)
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
                    required_fields = [
                        "first_name",
                        "last_name",
                        "username",
                        "email",
                        "password",
                        "bio",
                    ]
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
            

            elif url["requested_resource"] == "categories":
                content_len = int(self.headers.get("content-length", 0))
                request_body = self.rfile.read(content_len)
                category_data = json.loads(request_body)

                # Call the create_hauler function to add a new hauler
                new_category_id = create_category(category_data)

                if new_category_id:
                    # Respond with the newly created hauler's ID and a success status
                    response_body = json.dumps({"id": new_category_id})
                    return self.response(
                        response_body, status.HTTP_201_SUCCESS_CREATED.value
                    )
                else:
                    # Respond with an error status if hauler creation fails
                    return self.response(
                        "Failed to create hauler", status.HTTP_500_SERVER_ERROR.value
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

        # TODO: handle DELETE requests
        return self.response(
            "Feature is not yet implemented.", status.HTTP_501_NOT_IMPLEMENTED.value
        )  #!


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()