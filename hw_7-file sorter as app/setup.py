from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.2',
    description='My first deployment',
    url='https://github.com/DmytroSDV/my_HWs.git',
    author='Dmytro Smashmy',
    author_email='sdmytrov11@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['unidecode'],
    entry_points={'console_scripts': ['clean_folder = clean_folder.clean:main']}
)