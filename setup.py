#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


with open(path.join(path.dirname(path.abspath(__file__)), "requirements.txt")) as requirement_file:
    requirements = requirement_file.read().split("/n")

setup_requirements = ["pytest-runner"]

with open(path.join(path.dirname(path.abspath(__file__)), "requirements-dev.txt")) as dev_requirement_file:
    test_requirements = dev_requirement_file.read().split("/n")

setup(
    author="foryourselfand",
    author_email='foryourselfand@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="gazprom_test_task_jokes",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords="gazprom_test_task_jokes",
    name="gazprom_test_task_jokes",
    packages=find_packages(include=['gazprom_test_task_jokes']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/foryourselfand/gazprom_test_task_jokes',
    version='0.1.0',
    zip_safe=True
)
