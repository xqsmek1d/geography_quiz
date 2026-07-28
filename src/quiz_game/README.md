# Quiz Game

The `quiz_game` package contains the core logic of the geography quiz application. It is responsible for generating questions, managing quiz sessions, validating answers, handling game modes, and providing the command-line interface (as well as future interfaces)

The package is designed around modular components so that new question types, answer strategies, data sources, and user interfaces can be added without significantly changing the existing architecture.

---

## Overview

The application separates:

- **Data access** → repositories
- **Question creation** → builders and generators
- **Game logic** → services and core
- **Configuration** → config module
- **Data models** → models
- **User interaction** → CLI (and future additions)

---

# Package Structure

```
quiz_game/
├── algorithms/
├── builders/
├── cli/
├── config/
├── core/
├── generators/
├── models/
├── pools/
├── repositories/
├── services/
└── __init__.py
```

---

# `algorithms`

Contains miscellaneous algorithms used to support quiz generation.

## `country_difficulty.py`

Calculates country difficulty scores used for question selection.

Difficulty is based on factors derived from known information on countries:

- country size
- population
- recognisability
- geographical properties

---

# `builders`

Contains question builders for constructing questions of specific categories.

## Components

| File | Description |
| --- | --- |
| `builder_context.py` | Shared context passed to builders |
| `country_capital_builder.py` | Builds country-capital questions |
| `question_builder_registry.py` | Registers available builders |

This builder structure allows new question categories to be added independently.

---

# `cli`

Contains the interface for interacting with the quiz via the command-line by:

- displaying questions
- receiving user input
- displaying results *(WIP)*
- starting quiz sessions *(WIP)*

## Files

| File | Description |
| --- | --- |
| `main.py` | CLI entry point |
| `display.py` | Terminal output formatting |
| `input.py` | User input handling |

---

# `config`

Contains application configuration including:

- default settings
- enums
- configuration loading
- resolving user choices

## Files

| File | Description |
| --- | --- |
| `enums.py` | Quiz categories, modes, answer types |
| `constants.py` | Shared constants |
| `loader.py` | Loads configuration |
| `resolver.py` | Resolves configuration choices |
| `modes.py` | Quiz mode definitions |
| `cli_defaults.py` | CLI default quiz settings |

---

# `core`

Contains the central quiz runtime.

## `quiz_session.py`

Controls a single quiz session by:

- starting a quiz
- requesting questions
- processing answers *(WIP)*
- updating game state *(WIP)*
- tracking progress *(WIP)*

---

# `generators`

Responsible for generating questions and answer options.

## Question generation

### `question_generator.py`

Creates questions by combining:

- question builders
- repositories
- question pools
- user settings

## Answer generation

### `answer_generator.py`

Creates possible answers for questions.

Supports:

- open answers
- multiple-choice answers
- a mix of the above

## Distractors

### `distractor_generator.py`

Creates incorrect answers for multiple-choice questions.

Distractor strategies can include:

- random
- same region
- same subregion
*- same country (specific for some categories, to be implemented)*
*- similar difficulty (to be implemented)*

---

# `models`

Contains the data models used throughout the application.

Examples:

| Model | Description |
| --- | --- |
| `Country` | Country information |
| `City` | City information |
| `QuestionData` | Internal question blueprint |
| `Question` | Generated quiz question |
| `AnswerKey` | Hidden correct answer information |
| `Settings` | Quiz configuration |
| `GameState` | Current game progress |

---

# `pools`

Controls question availability.

A pool represents a collection of possible questions that can be selected during a quiz by:

- preventing repeated questions
- tracking remaining questions
- providing questions to generators
- recycling/resetting questions if needed *(WIP)*

## Files

| File | Description |
| --- | --- |
| `country_pool_factory.py` | Creates country-related pools |
| `pool_factory_registry.py` | Registers pool factories |

---

# `repositories`

Provides access to stored data and abstracts away where data comes from because:

- they do not depend on file formats
- easier testing with mock repositories
- future database support

Current repositories:

| Repository | Data |
| --- | --- |
| `country_repository.py` | Countries *(WIP)* |
| `city_repository.py` | Cities *(WIP)* |
| `landmark_repository.py` | Landmarks *(to be implemented)* | 

---

# `services`

Contains supporting logic.

## `answer_checker.py`

Checks whether submitted answers are correct:

- exact matching  *(WIP)* 
- answer normalisation  *(WIP)* 
- alternative answers  *(WIP)* 

## `question_pool.py`

Manages available questions during a quiz.

## `state_manager.py`

Handles changes to the current game state such as: *(to be implemented)*

- lives remaining
- score
- question count
- timers

---

# Data

The quiz package uses generated data stored outside the package:

```
data/
├── countries.json
└── cities.json
```

These files are created by utilities in:

```
src/utils/build_data/
```

The generated assets used for some categories of questions are stored in:

```
assets/
├── country_flags/
├── country_shapes/
├── country_highlights/
└── flat_country_highlights/
```

---

# Supported Quiz Features

## Question categories

Currently supported question categories include:

- Country → Capital
- Capital → Country
- Flag → Country
- Flag → Capital *(WIP)* 
- Map outline → Country *(WIP)* 
- Map highlight → Country *(WIP)* 
- City → Country *(WIP)* 
- Landmark → City *(WIP)* 
- Landmark → Country *(WIP)* 

## Answer types

Supported answer formats:

- Open answer
- Multiple choice
- Closed (true/false) *(to be implemented)*
- Information comparison (which of the two?) *(to be implemented)*
- A mix of the above

## Quiz modes

Supported quiz modes include:

- Practice *(WIP)* 
- Survival *(WIP)* 
- Time attack *(WIP)* 
- Hardcore *(WIP)* 
- Speedrun *(WIP)* 
- Marathon *(WIP)* 
- Custom *(WIP)* 

---

# Extending the Quiz

## Adding a new question type

To add a new question category:

1. Add a new enum value in:

```
config/enums.py
```

2. Create a new builder:

```
builders/<new_question_builder>.py
```

3. Register the builder in main using:

```
builders/question_builder_registry.py
```

4. Add required repositories or pools if needed.

---

## Adding a new data source

1. Create a repository:

```
repositories/new_repository.py
```

2. Add corresponding models:

```
models/
```

3. Add generation logic:

```
generators/
```

---

# Testing

Tests are located in:

```
tests/
```

Current tests cover:

- country repository loading
- question generation

Run tests with:

```bash
./run_tests.sh
```

---

# Design Goals

## Separation of concerns

Game logic, data access, and user interaction are separated.

## Extensibility

New question types can be added without modifying existing logic.

## Testability

Components can be tested independently.

## Data-driven design

Quiz content is dynamically generated from external datasets rather than hardcoded values, which would allow for endless combinations and all sorts of specific geography quizes imagineable to create your own geography quiz. Whether you want to learn something specific, extend your general knowledge, or explore the world, this geography quiz engine should have you covered!