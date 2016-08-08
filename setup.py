from setuptools import setup
from setuptools import find_packages


packages = [
    'Flask-Restless==0.17.0',
    'Flask-SQLAlchemy==2.1',
    'logga==0.0.0',
    'pytest==2.9.2',
    'pytest-cov==2.3.0',
    'pylint==1.6.4',
    'sphinx_rtd_theme==0.1.10a0',
    'Sphinx==1.4.5',
]

setup_kwargs = {
    'name': 'python-slagiatt',
    'version': '0.0.0',
    'description': 'Micro Services Seemed Like a Good Idea at the Time',
    'author': 'iPACT Devs',
    'author_email': 'loumarkovski@nbnco.com.au',
    'url': '',
    'install_requires': packages,
    'packages': find_packages(),
    'package_data': {
        'slagiatt': [
        ],
    },
}

setup(**setup_kwargs)
