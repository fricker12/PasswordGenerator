from setuptools import setup,find_packages

root_package = "PasswordGenerator"

setup(
    name='PasswordGenerator',
    version='1.0',
    description='Password Generation Utility',
    author='Evhen Korolov',
    author_email='fricker12@gmail.com',
    packages=[root_package] + [f"{root_package}.{item}" for item in find_packages(where=root_package)],
    url="https://github.com/fricker12/PasswordGenerator",
    install_requires=[
        'logging',
    ],
    python_requires='>=3.5',
)