rmdir dist -y
py -m build
twine upload dist/*