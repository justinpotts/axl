# axl
Python package that generates web extensions for Firefox

## Install
`pip install axl`

## How to Use
Command line: `axl option <option-value>`

Import:
```
from axl import generate
generate(option='<option-value>')
```
Note: Not all arguments are required. The extension will be generated with default values if left empty.

The .xpi file will be exported to the specified path, starting with `axl` followed by a custom seed, or the default: mixture of 6 random numbers and characters, such as `axlOA2H5D`.

The path is returned after successful completion.

### Options
To see all available options, type `axl --help`.
