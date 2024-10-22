from rest_framework import status
from rest_framework.response import Response


class SuccessResponse(Response):
    """
    Standard success response format.
    """

    def __init__(self, data=None, msg="success", code=0, status_code=status.HTTP_200_OK):
        """
        Initialize the SuccessResponse.

        Args:
            data (dict, optional): The data to be returned in the response.
            msg (str, optional): The success message.
            code (int, optional): The response code.
            status_code (int, optional): The HTTP status code.
        """
        super().__init__(
            data={
                "msg": msg,
                "data": data or {},
                "success": True,
                "code": code
            },
            status=status_code
        )
