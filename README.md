# axl
Python package that generates web extensions for Firefox

## Install
`pip install axl`

## How to Use
Command line: `axl <path>`

Import:
```
import axl
axl.generate(path='<path>')
```

The .xpi file will be exported to the specified path, starting with `axl` followed by a mixture of 6 random numbers and characters, such as `axlOA2H5D`.

The file name is returned after successful completion.
