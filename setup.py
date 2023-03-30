from setuptools import find_packages, setup
setup(
    name='streamsketchlib',
    packages=find_packages(include=['streamsketchlib']),
    version='0.1.0',
    description='Python library consisting of various streaming algorithms',
    author='Hoa Vu and Daniel Barnas',
    license='MIT',
    install_requires=['numpy', 'mmh3'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.2.2'],
    test_suite='tests',
)
