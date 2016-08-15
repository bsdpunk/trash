#from distutils.core import setup
from setuptools import setup, find_packages

#dependecy_links = ["git+https://github.com/pexpect/pexpect.git#egg=pexpect-0.1"]
install_requires = ['pyvmomi','pyvim','docker-py']

setup(
    name='trash',
    version='0.42',
    packages=['trash',],
    install_requires=install_requires,
    entry_points = { 'console_scripts': [
        'trash = trash.trash:cli', ],
        "trash.commands": [
            "get-groups = trash.adnet:get_groups",
        ],
     },
    author = "Dusty C",
    author_email = "bsdpunk@gmail.com.com",
    description = "A shell for linode, ESXi, And RedHat Satelite Server",
    license = "BSD",
    keywords = "Shell cli command virtualization management",
    url = 'bsdpunk.blogspot.com'   
    )
