from distutils.core import setup

setup(
    name='Learner',
    version='1.0.0',
    packages=['weka', 'weka.features', 'weka.issuesExtract', 'weka.FeatureExtract', 'Agent', 'Sanity', 'tomcat',
              'diffAnalyze', 'wekaMethods', 'wekaMethods.features', 'wekaMethods.issuesExtract',
              'wekaMethods.FeatureExtract', 'wekaMethods.featuresMethods'],
    install_requires = ['LIAC-ARFF',"networkx","numpy","jira","gitpython","python-igraph","scipy","bugzillatools"],
    url='',
    license='',
    author='amir',
    author_email='',
    description=''
)


#python setup.py sdist
