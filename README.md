# 🌍 Geography Quiz

A configurable Python geography quiz featuring countries, capitals, cities, maps and more.

Currently, the project consists of two parts:

- **A quiz engine** for generating geography questions.
- **A data processing pipeline** that builds, validates and maintains high-quality geographical datasets and assets from publicly available sources.

Although it is still mainly focused on interaction with a command-line interface, the project has been designed to support future graphical interfaces and web APIs.

---

## Features

### Quiz

- Multiple question types
    - Country → Capital *(planned)*
    - Capital → Country *(planned)*
    - City → Country *(planned)*
    - Flag → Country *(planned)*
    - Country outline → Country *(planned)*
    - Highlighted map → Country *(planned)*
- Open questions
- Multiple choice questions
- Mixed questions mode (e.g. open and multiple choice)
- LOTS OF configurable quiz settings
- Difficulty calculated based on country properties (population, size, gdp, and region)

### Data

The repository comes with the assets collections of flags and coat of arms, the other assets are generated upon first time usage.
The repository contains scripts to automatically:

- Generate the country datasets from the sources
- Generate the city datasets from the sources
- Correct inconsistencies between different geographic data sources
- Generate map outline images
- Generate highlighted country maps
- Validate generated datasets
- Validate assets

---

# Repository structure

```text
assets/        Generated images (flags, outlines, highlighted maps, etc.)
data/          Generated JSON datasets used by the quiz
sources/       Original and corrected source datasets
src/
    quiz_game/ Main quiz package
    utils/     Data processing and validation utilities
tests/         Unit tests
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/xqsmek1d/geography_quiz.git
cd geography_quiz
```

Install dependencies using **uv**

```bash
uv sync
```

or with pip

```bash
pip install -e .
```

---

# Building datasets

Rebuild all generated datasets

```bash
./update_data.sh
```

---

# Generating map assets

Generate outline maps and highlighted maps

```bash
./update_assets.sh
```

---

# Validation

Validate generated data

```bash
./validate_data.sh
```

---

# Testing

Run all tests

```bash
./run_tests.sh
```

or

```bash
pytest
```

---

# Running the quiz

```bash
./run_cli_quiz.sh
```

---

# Data sources

The repository combines data from several public sources, including:

- ISO 3166 country information
- World Bank administrative boundaries
- World city datasets

Additional information, corrections and preprocessing steps are documented in:

```
sources/README.md
```

---

# Project layout

```
quiz_game
├── algorithms
├── cli
├── config
├── models
├── repositories
```

### algorithms

Contains algorithms such as country difficulty calculations.

### cli

Command-line interface.

### config

Configuration, enums, defaults and mode definitions.

### models

Pydantic models representing countries, cities, quiz settings etc.

### repositories

Repository classes responsible for loading and filtering geographical data.

---

# Future plans

- GUI application
- FastAPI backend
- Web frontend
- Additional question categories
- Landmark support
- Difficulty balancing
- Spaced repetition mode
- More image-based questions

---

# License

This project is released under the MIT License.

---

# Acknowledgements

This project builds upon several publicly available geographic datasets. Credit belongs to the original authors and maintainers of those datasets.