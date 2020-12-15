# Env Alias

## Development
The following tools are used to create and manage this package.

### https://pypi.org/project/shut
Package release and management tools - [documentation](https://github.com/NiklasRosenstein/shut/blob/develop/docs/docs/index.md)
```shell script
# Update package files
$ shut pkg update

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

### https://pypi.org/project/pydoc-markdown
Documentation generation tools - [documentation](https://pydoc-markdown.readthedocs.io/en/latest/)
```shell script
# Render documentation
$ pydoc-markdown docs/pydoc-markdown.yml 

# Provide a local live review server 
$ pydoc-markdown --server docs/pydoc-markdown.yml
```
