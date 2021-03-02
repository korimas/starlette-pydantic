from setuptools import setup, find_packages

setup(
    # name=NAME,
    # version=VERSION,
    name='starlette_pydantic',
    version='0.1',
    author='zpzhou',
    author_email='himoker@163.com',
    url='https://github.com/zpdev/starlette-pydantic',
    description='pydantic for starlette',
    packages=find_packages(),
    install_requires=['starlette', 'pydantic'],
    include_package_data=True
)
