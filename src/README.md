# Source Code

This directory contains shared utility functions and modules used across analyses.

## Structure
```
src/
├── python/           # Python modules
└── r/               # R functions
```

## Guidelines
- Move code from notebooks here if it is reusable
- Write reusable, well-documented functions
- Include docstrings/roxygen documentation
- Add unit tests (pytest for python) for critical functions
- Keep functions focused and modular
- Document dependencies clearly

## Using Shared Code
### Python
```python
from src.python.preprocessing import function_name
```

### R
```r
source("src/r/preprocessing/function_name.R")
``` 