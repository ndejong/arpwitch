# arpwitch

## Development
The following development tools are used to help create and manage this project.

### shut
[shut](https://pypi.org/project/shut) is a Python package management and release 
tool - [documentation link](https://github.com/NiklasRosenstein/shut/blob/develop/docs/docs/index.md)
```shell script
# Update package files
$ shut pkg update

# Test the package
$ shut pkg test

# Create a staged changelog entry for a fix/feature
$ shut changelog --add fix --stage --message "Fixes bug"
$ shut changelog --add feature --stage --message "Initial version"

# Release bumps at patch/minor/major levels with --dry runs
$ shut pkg bump --patch --tag --push --dry
$ shut pkg bump --minor --tag --push --dry
$ shut pkg bump --major --tag --push --dry

# Build a package
$ shut pkg build -vvv setuptools:wheel
$ shut pkg build -vvv setuptools:*

# Publish a package
$ shut pkg publish --test warehouse:pypi
$ shut pkg publish warehouse:pypi
```

### pydoc-markdown
[pydoc-markdown](https://pypi.org/project/pydoc-markdown) is a documentation generation 
tool that works well with Python modules - [documentation link](https://pydoc-markdown.readthedocs.io/en/latest/)
```shell script
# Render documentation
$ pydoc-markdown docs/pydoc-markdown.yml 

# Provide a local live review server 
$ pydoc-markdown --server docs/pydoc-markdown.yml
```
