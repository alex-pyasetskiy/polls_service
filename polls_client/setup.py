from setuptools import setup, find_packages

setup(
    name="polls_client",
    version="0.0.1",
    zip_safe=False,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    package_data={
        '': ['*.css', '*.js', '*.html'],
    },
    install_requires=['setuptools']
)
