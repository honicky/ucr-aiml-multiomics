# R Scripts and RMarkdown Files

This directory contains R scripts and RMarkdown files for analysis and presentations.

## Naming Convention
Use the following format:
```
YYYY-MM-DD_topic_initials.Rmd
```

Example: `2024-03-15_differential_expression_RJ.Rmd`

## Guidelines
- Use RMarkdown for reproducible analysis
- Document package dependencies at the top of each file
- Follow tidyverse style guide
- Include session information using `sessionInfo()`
- Keep data preprocessing steps explicit and documented

## Beginner-friendly instruction for pushing a .rmd file to GitHub while also properly setting up the environment with renv. I

This repository contains an R Markdown (`.Rmd`) project. We use [`renv`](https://rstudio.github.io/renv/) for dependency management to ensure that anyone can reproduce the results with the same package versions.

## Project Structure

- `YYYY-MM-DD_topic_initials.Rmd` — Main analysis file  
- `renv.lock` — Snapshot of R package dependencies  
- `renv/` — Local library managed by `renv`  
- `your_project.Rproj` — RStudio project file

## R Environment Setup

We use `renv` to manage dependencies. Follow the steps below to recreate the project environment:

### 1. Clone or download the repository

Click the green **"Code"** button above and select **Download ZIP**, or clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### 2. Open the project in RStudio

Open the `.Rproj` file in RStudio.

### 3. Install `renv` (only once)

```r
install.packages("renv")
```

### 4. Restore the project environment

This will install all packages listed in `renv.lock`:

```r
renv::restore()
```

### 5. Knit the R Markdown file

Once the environment is ready, open and knit the `.Rmd` file:

```r
rmarkdown::render("YYYY-MM-DD_topic_initials.Rmd")
```


## Notes

- Do **not** run `renv::init()` if the `renv.lock` file already exists.
- You may need to install `rmarkdown` separately if it's not already installed:
  ```r
  install.packages("rmarkdown")
  ```

