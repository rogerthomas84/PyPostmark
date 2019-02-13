try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'PyPostmark',
    'description': 'PyPostmark is an easy to use Python library built for use in the Google App Engine Python 2.7 environment',
    'author': 'Roger Thomas',
    'author_email': 'rogere84@gmail.com',
    'url': 'ssh://git@bitbucket.org:rogerthomas84/PyPostmark.git',
    'download_url': 'ssh://git@bitbucket.org:rogerthomas84/PyPostmark.git',
    'version': '1.0.0',
    'packages': [
        'py_postmark',
        'py_postmark.models'
    ],
    'scripts': []
}

setup(**config)
