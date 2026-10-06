# Codebase Doctor

An intelligent Python codebase analysis and repair system designed to inspect, understand, and safely improve software projects.

> **Status:** Early Development

---

## Overview

Codebase Doctor is a modular software-engineering tool for analyzing Python codebases.

The project is designed to inspect an existing codebase, understand its structure, detect software-engineering problems, explain detected issues, and eventually provide controlled and reversible repairs.

The long-term vision is to combine traditional static analysis with AI-assisted reasoning and safe automated code modification.

A fundamental design principle is:

> **Codebase Doctor must never silently modify a user's codebase.**

---

## Current Capabilities

The current implementation focuses on the initial analysis pipeline:

```text
Project
   |
   v
Scanner
   |
   v
AST Parser
   |
   v
Code Analyzer
   |
   v
Issue Detection

Project Scanner

The scanner analyzes the project filesystem and identifies:

Files
Directories
Python files
Test files
Configuration files
Dependency files
Readable files
Unreadable files
Scan errors
Python AST Parser

Python source files are parsed using the built-in ast module.

The parser can:

Parse Python source code
Build Abstract Syntax Trees
Detect syntax errors
Track successfully parsed files
Track failed files
Code Analyzer

The analyzer currently checks for several code-quality problems, including:

Excessive function parameters
Large function bodies
Bare except blocks
Python syntax errors

Detected problems are represented as structured issues containing information such as:

Issue ID
File path
Line number
Title
Description
Category
Severity
Suggested solution
Evidence
Metadata

Example

The repository contains a deliberately problematic sample project:

examples/sample_project/
├── broken.py
├── main.py
└── users.py
broken.py

Contains an intentional Python syntax error.

users.py

Contains a function with an excessive number of parameters.

These examples allow the current scanner, parser, and analyzer pipeline to be demonstrated.

Example detected issues:

Python syntax error
Severity: HIGH
Too many function parameters
Severity: MEDIUM


Architecture

Codebase Doctor follows a modular architecture based on separation of responsibilities.

                    Codebase
                       |
                       v
                  +---------+
                  | Scanner |
                  +----+----+
                       |
                       v
                  +---------+
                  | Parser  |
                  |   AST   |
                  +----+----+
                       |
          +------------+------------+
          |            |            |
          v            v            v
     +---------+  +----------+  +----------+
     | Analyzer|  |Dependency|  | Security |
     +----+----+  +----------+  +----------+
          |            |            |
          +------------+------------+
                       |
                       v
                 +-----------+
                 |   Issues  |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 | Reasoning |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 |  Reporter |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 |  Repair   |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 | Approval  |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 | Modifier  |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 | Validator|
                 +-----+-----+
                       |
                  +----+----+
                  |         |
                  v         v
               Success   Failure
                  |         |
                  v         v
                 Save    Rollback

The architecture is intentionally divided into independent components so that each subsystem has a clear responsibility.

Project Structure
Codebase-Doctor/
|
├── examples/
│   └── sample_project/
│       ├── broken.py
│       ├── main.py
│       └── users.py
|
├── logs/
|
├── src/
│   └── codebase_doctor/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── architecture.py
│       ├── dependency.py
│       ├── issues.py
│       ├── models.py
│       ├── modifier.py
│       ├── parser.py
│       ├── reasoning.py
│       ├── repair.py
│       ├── reporter.py
│       ├── rollback.py
│       ├── scanner.py
│       ├── security.py
│       └── validator.py
|
├── tests/
│   ├── test_analyzer.py
│   ├── test_parser.py
│   └── test_scanner.py
|
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt

Core Modules
Module	Responsibility
scanner.py	Filesystem and project scanning
parser.py	Python AST parsing
analyzer.py	Code-quality analysis
dependency.py	Dependency and import analysis
architecture.py	Architecture analysis
security.py	Security analysis
issues.py	Issue creation and management
models.py	Shared data models and enums
reasoning.py	AI-assisted reasoning
repair.py	Repair planning
modifier.py	Source-code modification
validator.py	Post-repair validation
rollback.py	State restoration
reporter.py	Reporting and issue presentation

Planned Architecture

The long-term analysis and repair pipeline is planned as:

Project
   |
   v
Scanner
   |
   v
AST Parser
   |
   v
Static Analysis
   |
   +--> Dependency Analysis
   |
   +--> Architecture Analysis
   |
   +--> Security Analysis
   |
   v
Issue Detection
   |
   v
AI Reasoning
   |
   v
Issue Report
   |
   v
Repair Planning
   |
   v
Diff Preview
   |
   v
User Approval
   |
   v
Code Modification
   |
   v
Validation
   |
   +--> Success --> Save
   |
   +--> Failure --> Rollback

The modules for these future stages already exist in the project structure so the system can evolve toward a larger integrated architecture.

Safety Model

Automated source-code modification can introduce significant risk.

Codebase Doctor is therefore designed around an explicit approval and validation workflow.

Before modifying source code:

Issue
   |
   v
Analysis
   |
   v
Repair Plan
   |
   v
Diff Preview
   |
   v
User Approval

After approval:

Modification
      |
      v
Validation
   /     \
  /       \
Success   Failure
  |         |
  v         v
Save     Rollback

The goal is to make automated repairs:

Explicit
Reviewable
Validated
Reversible
Auditable

Development Status
Implemented
 Project architecture
 Filesystem scanner
 Python AST parser
 Basic code-quality analyzer
 Structured issue models
 Issue management
 Example project
 Initial unit tests
 Git repository
 GitHub repository
Under Development
 Advanced dependency analysis
 Advanced architecture analysis
 Advanced security analysis
 Advanced reporting
 AI-powered reasoning
 Repair planning
 Diff generation and preview
 Safe automated modification
 Post-repair validation
 Automatic rollback integration
 End-to-end analysis pipeline
 Dependency graph visualization
 Graphical interface
 Test generation
 AI-assisted debugging
 Automated refactoring

 Roadmap

The long-term goal is to evolve Codebase Doctor from a basic static-analysis system into an intelligent software-engineering platform.

Static Analysis
      |
      v
Code Understanding
      |
      v
Architecture Analysis
      |
      v
Dependency Graph
      |
      v
Security Analysis
      |
      v
AI Reasoning
      |
      v
Repair Planning
      |
      v
Diff Generation
      |
      v
User Approval
      |
      v
Code Modification
      |
      v
Testing
      |
      v
Validation
      |
      +----> Rollback
      |
      +----> Save

      Installation
Requirements
Python 3.10+
Git
Clone the repository
git clone https://github.com/fazllolahiamirmmohmad-netizen/Codebase-Doctor.git
Enter the project
cd Codebase-Doctor
Install dependencies
python -m pip install -r requirements.txt

Running the Tests

The project uses pytest for testing.

Run:

pytest

Technologies
Current Core
Python
pathlib
ast
dataclasses
typing
logging
Testing
pytest
Planned Analysis and Engineering Tools
Ruff
MyPy
Radon
NetworkX
Packaging
GitPython
Planned AI Integration
Pydantic
Ollama
Planned GUI
PySide6

Engineering Principles

Codebase Doctor is being developed around the following principles:

Modular architecture
Separation of responsibilities
Clean Code
Type hints
Structured data models
AST-based analysis
Explicit user approval
Safe source-code modification
Validation before saving changes
Rollback after failed validation
Extensible AI integration
Testable components
Git-aware development

Project Goals

The main goals of Codebase Doctor are:

Understand existing Python codebases.
Detect meaningful software-engineering problems.
Explain why detected problems matter.
Provide actionable repair strategies.
Use AI reasoning where traditional static analysis is insufficient.
Make automated modifications controllable and reversible.
Help developers maintain and improve complex software systems

Author

Amirmmohmad Fazllolahi

Python Developer | AI Engineering

GitHub:

https://github.com/fazllolahiamirmmohmad-netizen

License

This project is currently under development.

License information will be added in a future release.