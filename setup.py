#from distutils.core import setup
from setuptools import setup, find_packages

#dependecy_links = ["git+https://github.com/pexpect/pexpect.git#egg=pexpect-0.1"]
install_requires = ['pyvmomi']

setup(
    name='trash',
    version='0.30',
    packages=['trash',],
    install_requires=install_requires,
    entry_points = { 'console_scripts': [
        'trash = trash.trash:cli', ],
        "trash.commands": [
            "get-groups = trash.adnet:get_groups",
        ],
     },
    author = "dusty c",
    author_email = "bsdpunk@gmail.com.com",
    description = "A shell for ESXi And RedHat Satelite Server",
    license = "BSD",
    keywords = "Shell cli command",
    url = 'bsdpunk.blogspot.com'   
    )
