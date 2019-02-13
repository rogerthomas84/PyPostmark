# Postmark Python

## Getting Started

Getting started with this Python library for Postmark is easy. Here's what you'll need:

### Pre-requisites

1. A Postmark Account: [Sign up for a new account](https://postmarkapp.com/sign_up).
2. A "Server Token": [Set up a new 'server' in your account](https://postmarkapp.com/servers).
3. A "Sender Signature": [Create a sender signature](https://postmarkapp.com/signatures/new).


### Sending your first email:

Postmark is designed to make sending email super easy, the following snippet shows how easy it is to get started:

```python
try:
    client = PostmarkClient(
        server_token="<server token>"
    )
    send_result = client.send_email(
        from_email="<sender signature>",
        to_email="ben@example.com",
        subject="Hello from Postmark!",
        html_body="This is just a friendly 'hello' from your friends at Postmark."
    )
    logging.info(send_result)

except PostmarkException, e:
    logging.error(e.http_status_code)
    logging.error(e.message)
    logging.error(e.postmark_api_error_code)

except Exception, ee:
    # A general exception is thrown if the API was unreachable or times out.
    logging.exception("Error")
```


### Sending using a template

Postmark provides a very powerful templating system that allows you to define an email's content ahead of time, and then pass just the values that change when you want to send it. This is a particularly useful when you are sending transactional emails (like password resets emails, for example), as the content is largely the same, except for the a user's name, and the reset link.

Templates also automatically inline stylesheets, which makes maintaining them and keeping them looking great in many email clients, a breeze. You can get more detailed information about the templating language (Mustachio), and how the templating system works, here: http://support.postmarkapp.com/article/1077-template-syntax

To use a template, first create it inside of one of your [Postmark Servers](https://account.postmarkapp.com/servers). After you create the template, take a note of the Template's ID, you will use that in the example code below:

```python
try:
    client = PostmarkClient(
        server_token="<server token>"
    )
    send_result = client.send_email_with_template(
        from_email="<sender signature>",
        to_email="ben@example.com",
        template_id=<template id>,
        template_model={
            "name": "Joe"
        }
    )
    logging.info(send_result)

except PostmarkException, e:
    logging.error(e.http_status_code)
    logging.error(e.message)
    logging.error(e.postmark_api_error_code)

except Exception, ee:
    # A general exception is thrown if the API was unreachable or times out.
    logging.exception("Error")
```


### Using attachments

You may add file attachments to any outgoing email provided they comply with the current [white-list](http://developer.postmarkapp.com/developer-send-api.html#attachments) of accepted email attachments. You may add as many attachments as you like as long as you don't go past the total size limit of 10MB per message.

#### Including an attachment with a message

```python
client = PostmarkClient(
    server_token="<server token>"
)

attachment = PostmarkAttachment.from_raw_data(
    data='Hello from a file!',
    attachment_name='example.txt',
    mime_type='text/plain',  # optional, default None
    content_id=None  # optional, default None
)

send_result = client.send_email(
    from_email="<sender signature>",
    to_email="ben@example.com",
    subject="Hello from Postmark!",
    html_body="This is just a friendly 'hello' from your friends at Postmark.",
    attachments=[attachment]
)
```

#### Including an "inline" attachment

The following example works similarly to the example above, except it loads the file content directly from the filesystem.

In order to maximize compatibility with the most email clients, you should also specify the `content_id` (the last parameter of the `PostmarkAttachment.from_file` method. `cid:logo.png` -- notice that this matches the `src=` attribute in the HTML part of the content. Including the `cid:` prefix instructs the Postmark API to treat this attachment as an "inline" attachment, instead of a file attachment, as was shown above. The above example can also accept the `content_id` parameter.

```python
client = PostmarkClient(
    server_token="<server token>"
)

attachment = PostmarkAttachment.from_file(
    file_path='cat-2669554_640.png',
    attachment_name='cat.png',
    mime_type='image/png',  # optional, default None
    content_id='cid:cat.png'  # optional, default None
)

send_result = client.send_email(
    from_email="<sender signature>",
    to_email="ben@example.com",
    subject="Hello from Postmark!",
    html_body="<b>Hi there! This is an inlined image attachment: <img src="cid:cat.png"/></b>",
    attachments=[attachment]
)
```
