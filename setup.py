from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='workflow_manager',
      version='0.1',
      description='Wizard-link workflow manager',
      long_description=readme(),
      url='http://github.com/dimtruck/workflow-manager-py',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Workflow Manager :: Wizard',
      ],
      author='Dimitry Ushakov',
      author_email='me@dimitryushakov.com',
      license='MIT',
      packages=['workflow_manager'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'coverage','pytest-cov'],
      zip_safe=False)
