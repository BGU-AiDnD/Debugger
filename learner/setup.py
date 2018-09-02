from setuptools import setup, find_packages

install_requires = ['liac-arff', 'python-bugzilla', 'distance', 'GitPython', 'github3.py', 'jira', 'networkx',
                    'numpy', 'pyswarm', 'requests', 'scipy', 'junitparser']

setup(
    name='eclipse',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/amir9979/Debugger',
    license='',
    author='Amir Elmishali',
    author_email='amir9979@gmail.com',
    install_requires=install_requires,
    description=''
)
