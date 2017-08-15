from setuptools import setup, find_packages

setup(
    name='eclipse',
    version='1.0.0',
    packages=['NLP', 'Agent', 'Sanity', 'Planner', 'Planner.mcts', 'Planner.lrtdp', 'Planner.pomcp',
              'Planner.pomcp_old.pomcp', 'Planner.lrtdp_checker', 'Diagnoser', 'diffAnalyze', 'wekaMethods',
              'wekaMethods.features', 'wekaMethods.issuesExtract', 'wekaMethods.featuresMethods', 'result_parsing'],
    url='https://github.com/amir9979/Debugger',
    license='',
    author='Amir Elmishali',
    author_email='amir9979@gmail.com',
    description=''
)
