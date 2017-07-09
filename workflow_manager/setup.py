from setuptools import setup

setup(name='workflow_manager',
      version='0.1',
      description='Workflow manager for tasks',
      url='http://github.com/dimtruck/workflow-manager-py',
      author='Dimitry Ushakov',
      author_email='me@dimitryushakov.com',
      license='MIT',
      packages=['workflow_manager'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'coverage','pytest-cov'],
      zip_safe=False)
