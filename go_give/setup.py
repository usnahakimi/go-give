from setuptools import find_packages, setup

setup(
    name="go_give",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
<<<<<<< HEAD
    install_requires=["flask", "seleniumbase", "faker", "flask_sqlalchemy", "flask_login", "boto3", "flask_migrate", "flask_bootstrap"],
=======
    install_requires=["flask", "seleniumbase", "faker", "flask_sqlalchemy", "flask_login", "boto3", "flask_migrate", "flask_bootstrap", "flask_babel", "flask_admin", "flask_wtf"],
>>>>>>> d22074b021958340d26a4dc2e87c1bd7548e2c4f
)