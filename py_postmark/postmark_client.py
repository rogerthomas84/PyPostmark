from .postmark_client_base import PostmarkClientBase


class PostmarkClient(PostmarkClientBase):

    def __init__(self, server_token, timeout=30):
        self._setup(server_token, 'X-Postmark-Server-Token', timeout)

    def send_email(self, from_email, to_email, subject, html_body=None, text_body=None, tag=None, track_opens=True, reply_to=None, cc=None, bcc=None, headers=None, attachments=None, track_links=None):
        """
        Send an email.

        :param str from_email: The sender of the email. (Your account must have an associated Sender Signature for
                the address used).
        :param str to_email: The recipient of the email.
        :param str subject: The subject of the email.
        :param str html_body: The HTML content of the message, optional if Text Body is specified.
        :param str text_body: The text content of the message, optional if HTML Body is specified.
        :param str tag: A tag associated with this message, useful for classifying sent messages.
        :param bool track_opens: True if you want Postmark to track opens of HTML emails.
        :param str reply_to: Reply to email address.
        :param str cc: Carbon Copy recipients, comma-separated.
        :param str bcc: Blind Carbon Copy recipients, comma-separated.
        :param dict headers: Headers to be included with the sent email message.
        :param list[py_postmark.models.postmark_attachment.PostmarkAttachment] attachments: A list of PostmarkAttachment
                objects.
        :param str track_links: Can be any of "None", "HtmlAndText", "HtmlOnly", "TextOnly" to enable link tracking.

        :rtype: dict
        :return: The JSON decoded response from the Postmark API.
        """
        body = {
            'From': from_email,
            'To': to_email,
            'Cc': cc,
            'Bcc': bcc,
            'Subject': subject,
            'HtmlBody': html_body,
            'TextBody': text_body,
            'Tag': tag,
            'ReplyTo': reply_to,

            'Headers': self.__fix_headers(headers),

            'TrackOpens': track_opens,
            'Attachments': self.__fix_attachments(attachments)
        }

        if track_links is not None:
            body['TrackLinks'] = track_links

        return self._process_rest_request('POST', '/email', body)

    def send_email_with_template(self, from_email, to_email, template_id, template_model=None, inline_css=True, tag=None, track_opens=True, reply_to=None, cc=None, bcc=None, headers=None, attachments=None, track_links=None):
        """
        Send an email using a template.

        :param str from_email: The sender of the email. (Your account must have an associated
                Sender Signature for the address used).
        :param str to_email: The recipient of the email.
        :param int template_id: The ID of the template to use to generate the content of this message.
        :param dict template_model: The values to combine with the Templated content.
        :param bool inline_css: If the template contains an HTMLBody, CSS is automatically inlined, you may opt-out
                of this by passing 'false' for this parameter.
        :param str tag: A tag associated with this message, useful for classifying sent messages.
        :param bool track_opens: True if you want Postmark to track opens of HTML emails.
        :param str reply_to: Reply to email address.
        :param str cc: Carbon Copy recipients, comma-separated.
        :param str bcc: Blind Carbon Copy recipients, comma-separated.
        :param dict headers: Headers to be included with the sent email message.
        :param list[py_postmark.models.postmark_attachment.PostmarkAttachment] attachments: A list of PostmarkAttachment
                objects.
        :param str track_links: Can be any of "None", "HtmlAndText", "HtmlOnly", "TextOnly" to enable link tracking.

        :rtype: dict
        :return: The JSON decoded response from the Postmark API
        """
        body = {
            'From': from_email,
            'To': to_email,
            'Cc': cc,
            'Bcc': bcc,
            'Tag': tag,
            'ReplyTo': reply_to,
            'Headers': self.__fix_headers(headers),
            'TrackOpens': track_opens,
            'Attachments': self.__fix_attachments(attachments),
            'TemplateModel': template_model,
            'TemplateId': template_id,
            'InlineCss': inline_css
        }

        if track_links is not None:
            body['TrackLinks'] = track_links

        return self._process_rest_request('POST', '/email/withTemplate', body)

    def __fix_headers(self, headers):
        """
        The Postmark API wants an Array of Key-Value pairs, not a dictionary object,
        therefore, we need to wrap the elements in an array.

        :param dict headers:
        :return:
        """
        if headers is None:
            return None

        ret_val = []
        for k,v in headers.iteritems():
            ret_val.append({'Name': k, 'Value': v})
        return ret_val

    def __fix_attachments(self, attachments):
        """
        Treat any attachment models by calling the `json_serialize` method.

        :param list[py_postmark.models.postmark_attachment.PostmarkAttachment] attachments: A list of PostmarkAttachment
                objects.
        :return: list
        """
        attach = None
        if attachments is not None:
            attach = []
            for a in attachments:
                attach.append(a.json_serialize())
        return attach
