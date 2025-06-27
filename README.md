# Code Difficulty Analyzer

This tool classifies coding problems into Easy, Medium, or Hard using:
- Rule-based heuristics
- Optional LLM validation (Groq API)

## Features

- Simple HTML frontend for input
- Flask backend for processing
- Rule-based analyzer (`analyzer.py`)
- Optional Groq LLM-based analysis (`groq_interface.py`)

## Setup

### 1. Install Requirements

```bash
pip install flask requests
