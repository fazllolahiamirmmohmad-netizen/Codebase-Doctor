README.md
# Codebase Doctor

An intelligent Python codebase analysis and repair system designed to inspect, understand, and safely improve software projects.

Codebase Doctor combines static code analysis, AST parsing, dependency analysis, architecture inspection, security analysis, AI-assisted reasoning, repair planning, validation, and rollback into a modular software-engineering system.

> **Status:** Early Development

---

## Overview

Codebase Doctor is designed to act as an intelligent software-engineering assistant for Python codebases.

The system analyzes an existing project instead of only executing it. It attempts to understand the structure and relationships inside the codebase, identify problems, explain their impact, and eventually propose and safely apply repairs.

The core workflow is:

```text
Project
   ↓
Scanner
   ↓
AST Parser
   ↓
Code Analysis
   ├── Dependency Analysis
   ├── Architecture Analysis
   └── Security Analysis
   ↓
Issue Detection
   ↓
AI Reasoning
   ↓
Issue Report
   ↓
Repair Planning
   ↓
User Approval
   ↓
Code Modification
   ↓
Validation
   ├── Success → Save
   └── Failure → Rollback

A fundamental design principle is:

Codebase Doctor must never silently modify a user's codebase.

Features
Project Scanner

The scanner analyzes the project filesystem and collects information about:

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
Code Analysis

The analyzer inspects parsed Python code for code-quality problems.

Current checks include:

Excessive function parameters
Large functions
Bare except blocks
Syntax errors

Each detected problem is represented as a structured issue containing information such as:

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
Dependency Analysis

The dependency subsystem is designed to analyze:

Python imports
Module relationships
External dependencies
Internal project dependencies
Architecture Analysis

The architecture subsystem is designed to analyze relationships between modules and identify structural problems in a codebase.

Security Analysis

The security subsystem is designed to detect potentially dangerous or insecure coding patterns.

AI Reasoning

The reasoning layer is designed to provide AI-assisted interpretation of detected issues.

The architecture supports integration with local AI models through Ollama.

Repair System

The repair pipeline is designed around controlled modifications:

Issue
  ↓
Repair Plan
  ↓
Diff Preview
  ↓
User Approval
  ↓
Modification
  ↓
Validation
  ↓
Save / Rollback
Validation

The validator is responsible for checking whether a modification remains valid after repair.

Possible validation mechanisms include:

Python compilation
Automated tests
Static analysis
Type checking
Rollback

If a modification fails validation, the rollback system is designed to restore the previous state of the affected files.

Architecture

Codebase Doctor follows a modular architecture based on separation of responsibilities.

                         Codebase
                            │
                            ▼
                       ┌─────────┐
                       │ Scanner │
                       └────┬────┘
                            │
                            ▼
                       ┌─────────┐
                       │ Parser  │
                       │   AST   │
                       └────┬────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        ┌─────────┐   ┌────────────┐   ┌──────────┐
        │ Analyzer│   │ Dependency │   │ Security │
        └────┬────┘   └─────┬──────┘   └────┬─────┘
             │              │               │
             └──────────────┼───────────────┘
                            ▼
                     ┌────────────┐
                     │   Issues   │
                     └─────┬──────┘
                           │
                           ▼
                     ┌────────────┐
                     │  Reasoning │
                     └─────┬──────┘
                           │
                           ▼
                     ┌────────────┐
                     │  Reporter  │
                     └─────┬──────┘
                           │
                           ▼
                     ┌────────────┐
                     │   Repair   │
                     └─────┬──────┘
                           │
                           ▼
                     ┌────────────┐
                     │  Approval  │
                     └─────┬──────┘
                           │
                           ▼
                     ┌────────────┐
                     │  Modifier  │
                     └─────┬──────┘
                           │
                           ▼
                     ┌────────────┐
                     │ Validator  │
                     └─────┬──────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                 Success        Failure
                    │             │
                    ▼             ▼
                  Save         Rollback
Project Structure
Codebase-Doctor/
│
├── examples/
│   └── sample_project/
│       ├── broken.py
│       ├── main.py
│       └── users.py
│
├── logs/
│
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
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_parser.py
│   └── test_scanner.py
│
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
rollback.py	Safe state restoration
reporter.py	Issue and analysis reporting
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
Example

The repository includes a sample Python project:

examples/sample_project/

It contains:

main.py
users.py
broken.py

broken.py intentionally contains a syntax error.

users.py intentionally contains a function with excessive parameters.

These files are included to demonstrate the analysis capabilities of Codebase Doctor.

Example analysis results:

Python syntax error
Severity: HIGH

and:

Too many function parameters
Severity: MEDIUM
Current Pipeline

The currently implemented analysis path is:

Project
   ↓
Scanner
   ↓
Parser
   ↓
Analyzer
   ↓
Issue Detection

The scanner identifies the project files.

The parser converts valid Python source code into AST structures and detects syntax errors.

The analyzer inspects the parsed AST and creates structured issues.

Technologies
Core
Python
pathlib
ast
dataclasses
typing
logging
Analysis
Pytest
Ruff
MyPy
Radon
NetworkX
Packaging
GitPython
AI
Pydantic
Ollama
GUI
PySide6
Engineering Principles

Codebase Doctor is designed around the following principles:

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
Git-aware development
Development Status
Implemented
 Project architecture
 Filesystem scanner
 Python AST parser
 Basic code-quality analyzer
 Issue management
 Shared data models
 Example project
 Initial unit tests
 Git repository
 GitHub repository
Planned / Under Development
 Advanced dependency analysis
 Advanced architecture analysis
 Advanced security analysis
 Advanced reporting
 AI-powered reasoning
 Repair planning
 Diff preview
 Safe automated modification
 Post-repair validation
 Automatic rollback
 End-to-end analysis pipeline
 Graph visualization
 Graphical interface
 Test generation
 AI-assisted debugging
 Automated refactoring
Roadmap

The long-term goal is to develop Codebase Doctor into an intelligent software-engineering platform capable of understanding and safely improving real-world Python codebases.

Future development is planned around:

Static Analysis
      ↓
Code Understanding
      ↓
Architecture Analysis
      ↓
Dependency Graph
      ↓
Security Analysis
      ↓
AI Reasoning
      ↓
Repair Planning
      ↓
Diff Generation
      ↓
User Approval
      ↓
Code Modification
      ↓
Testing
      ↓
Validation
      ↓
Rollback / Save
Safety Model

Automated source-code modification introduces significant risk.

Codebase Doctor therefore follows a controlled repair workflow.

The system should never directly modify a project without user approval.

Before modification:

Issue
  ↓
Analysis
  ↓
Repair Plan
  ↓
Diff Preview
  ↓
User Approval

After approval:

Modification
      ↓
Validation
   ┌──┴──┐
   ↓     ↓
Success Failure
   ↓     ↓
 Save  Rollback

This approach is intended to minimize unintended changes and make automated repairs reversible.

Project Goals

The main goals of Codebase Doctor are:

Understand existing Python codebases.
Detect meaningful software-engineering problems.
Explain why those problems matter.
Provide actionable repair strategies.
Use AI reasoning where traditional static analysis is insufficient.
Make automated modifications controllable and reversible.
Help developers maintain and improve complex software systems.
Author

Amirmmohmad Fazllolahi

Python Developer | AI Engineering

GitHub:

https://github.com/fazllolahiamirmmohmad-netizen

License

This project is currently under development.

License information will be added in a future release.