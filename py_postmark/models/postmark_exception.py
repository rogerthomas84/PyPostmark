class PostmarkException(Exception):

    message = None
    http_status_code = None
    postmark_api_error_code = None

    def __init__(self, message, http_status_code, postmark_api_error_code=None):
        """
        :param str message:
        :param int http_status_code:
        :param int postmark_api_error_code:
        """
        self.message = message
        self.http_status_code = http_status_code
        self.postmark_api_error_code = postmark_api_error_code
