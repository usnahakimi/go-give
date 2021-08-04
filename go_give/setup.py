from setuptools import find_packages, setup

setup(
    name="go_give",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "seleniumbase", "faker", "flask_sqlalchemy", "flask_login", "boto3", "flask_migrate", "flask_bootstrap", "flask_babel", "flask_admin", "flask_wtf"],
)