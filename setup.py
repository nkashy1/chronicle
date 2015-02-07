from setuptools import setup, find_packages

setup(name = 'chronicle',
      version = '0.1',
      author = 'Neeraj Kashyap',
      author_email = 'nkashy1@gmail.com',
      packages = find_packages(exclude=["test*"])
      )