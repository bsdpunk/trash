#from distutils.core import setup
from setuptools import setup, find_packages

#dependecy_links = ["git+https://github.com/pexpect/pexpect.git#egg=pexpect-0.1"]
install_requires = ['pyvmomi','pyvim','docker-py']

setup(
    name='trash-shell',
    version='0.45',
    packages=['trash',],
    install_requires=install_requires,
    entry_points = { 'console_scripts': [
        'trash = trash.trash:cli', ],
     },
    author = "Dusty C",
    author_email = "bsdpunk@gmail.com.com",
    description = "A shell for linode, docker, ESXi, And RedHat Satelite Server",
    license = "BSD",
    keywords = "Shell cli command virtualization management",
    url = 'http://github.com/trash' 
    )
