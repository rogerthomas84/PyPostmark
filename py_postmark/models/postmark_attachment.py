class PostmarkAttachment:

    name = None
    mime_type = None
    data = None
    content_id = None
    DEFAULT_MIME_TYPE = 'application/octet-stream'

    def __init__(self, base64_encoded_data, attachment_name, mime_type=DEFAULT_MIME_TYPE, content_id=None):
        """
        Initialise a new attachment

        :param str base64_encoded_data:
        :param str attachment_name:
        :param str mime_type: (optional), default 'application/octet-stream'
        :param str content_id: (optional), default None
        """
        self.name = attachment_name
        self.data = base64_encoded_data
        self.mime_type = mime_type
        self.content_id = content_id

    @staticmethod
    def from_raw_data(data, attachment_name, mime_type=None, content_id=None):
        """
        Construct an attachment from raw data.

        :param str data:
        :param str attachment_name:
        :param str mime_type: (optional), will default to 'application/octet-stream' at point of sending.
        :param str content_id: (optional), default None

        :rtype: PostmarkAttachment
        :return: An instance of PostmarkAttachment
        """
        base64_encoded_data = data.encode('base64')
        return PostmarkAttachment(
            base64_encoded_data=base64_encoded_data,
            attachment_name=attachment_name,
            mime_type=mime_type,
            content_id=content_id
        )

    @staticmethod
    def from_base64_encoded_data(base64_encoded_data, attachment_name, mime_type=None, content_id=None):
        """
        Construct an attachment from pre-base64 encoded data.

        :param str base64_encoded_data:
        :param str attachment_name:
        :param str mime_type: (optional), will default to 'application/octet-stream' at point of sending.
        :param str content_id: (optional), default None

        :rtype: PostmarkAttachment
        :return: An instance of PostmarkAttachment
        """
        return PostmarkAttachment(
            base64_encoded_data=base64_encoded_data,
            attachment_name=attachment_name,
            mime_type=mime_type,
            content_id=content_id
        )

    @staticmethod
    def from_file(file_path, attachment_name, mime_type=None, content_id=None):
        """
        Construct an attachment from a given file path.

        :param str file_path:
        :param str attachment_name:
        :param str mime_type: (optional), will default to 'application/octet-stream' at point of sending.
        :param str content_id: (optional), default None

        :rtype: PostmarkAttachment
        :return: An instance of PostmarkAttachment
        """
        raw_data = open(file_path, 'r').read()
        return PostmarkAttachment.from_raw_data(
            data=raw_data,
            attachment_name=attachment_name,
            mime_type=mime_type,
            content_id=content_id
        )

    def json_serialize(self):
        """
        Get a JSON serializable representation of this attachment.

        :rtype: dict
        """
        return {
            'Name': self.name,
            'Content': self.data,
            'ContentType': 'application/octet-stream' if self.mime_type is None else self.mime_type,
            'ContentId': self.content_id
        }
