# axl
Python package that generates web extensions for Firefox

## Install
`pip install axl`

## How to Use
Command line: `axl <path>`

Import:
```
import axl
axl.generate(<options>)
```

The .xpi file will be exported to the specified path, starting with `axl` followed by a mixture of 6 random numbers and characters, such as `axlOA2H5D`.

The path is returned after successful completion.

### Options

Axl includes multiple options to customize your web extensions.
```
path='/path/to/desired/export/location/': Allows you to specify the location to export packaged extension.
seed='customSeed':
