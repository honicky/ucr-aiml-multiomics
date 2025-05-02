# Machine Learning & AI for Multi-Omic Data Journal Club

This repository hosts code, documentation, and resources for the Machine Learning & AI for Multi-Omic Data Journal Club. Use it to share and collaborate on analyses using both Python and R.

## Repository Structure

```
ucr-aiml-multiomics/
├── notebooks/          # Jupyter notebooks for analysis and presentations
├── r_scripts/          # R analysis scripts and RMarkdown files
├── src/                # Shared Python/R utility functions
└── data/               # Small datasets and links to large ones (in the README)
```

## Setup Instructions

### Python Environment Setup

We use `uv` for Python dependency management. It's a fast, reliable Python package installer and resolver.

1. Install `uv`:
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Initialize the project:
   ```bash
   # Create virtual environment
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   
   # Initialize project dependencies
   uv sync
   ```

3. Managing dependencies:
   ```bash
   # Add new packages
   uv add numpy pandas scikit-learn
   
   # Add development dependencies
   uv add --dev pytest black
   
   # Remove packages
   uv remove package_name
   
   # View dependency tree
   uv tree
   
   # Update all dependencies
   uv sync
   ```

### R Environment Setup

We use `renv` for R dependency management:

1. Install `renv`:
   ```R
   install.packages("renv")
   ```

2. Initialize the project:
   ```R
   renv::init()
   ```

3. Install dependencies:
   ```R
   renv::restore()
   ```

## Contributing

1. Create a new branch for your work
2. Add your notebooks/scripts in the appropriate directory
3. Update dependencies if you add new ones:
   - For Python: Use `uv add package_name` and then `uv sync`
   - For R: Use `renv::snapshot()` to update `renv.lock`
4. Submit a pull request

## Best Practices

### Notebooks
- Name notebooks with a prefix indicating the topic and your initials
- Include clear markdown documentation
- Remove unnecessary output before committing

### R Scripts
- Use RMarkdown for analysis documentation
- Follow tidyverse style guide
- Document dependencies clearly

