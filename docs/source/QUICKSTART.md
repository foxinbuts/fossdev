# Quick Start Guide

This guide will help you install the `sales` project and run your first report.

## 1. Installation

### From Source (Editable Mode)

```bash
git clone git@github.com:foxinbuts/fossdev.git
cd fossdev
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Basic Verification

Verify installation by checking the CLI version:

```bash
sales --version
```

## 3. Running Sample Data

A sample CSV dataset is provided in `data/sample_sales.csv`:

```text
tea,drinks,7.0,5
coffee,drinks,12.5,3
croissant,bakery,15.2,2
baguette,bakery,25.2,1
apple,fruit,4.0,6
```

Generate a summary report:

```bash
sales -i data/sample_sales.csv
```

Expected output:

```text
Report
------
drinks: 72.5
bakery: 55.6
fruit: 24.0
------
Total: 152.1
```

## 4. Running Automated Tests

Run the full test suite with coverage report:

```bash
pytest --cov=sales --cov-report=term-missing
```
