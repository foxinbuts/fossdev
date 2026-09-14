Using Project Sales
===================

The ``sales`` package provides both a Python API and an executable command-line interface.

Python Library Usage
--------------------

.. code-block:: python

    from sales import read_data, filter_by_threshold, generate_report

    # 1. Read and validate CSV sales logs
    records = read_data("data/sample_sales.csv")

    # 2. Optionally filter records by minimum position total (e.g., >= 30.0)
    high_value_sales = filter_by_threshold(records, threshold=30.0)

    # 3. Generate formatted summary report with optional discount percentage
    report_text = generate_report(records, discount=10.0)
    print(report_text)


Command Line Interface (CLI) Usage
----------------------------------

Running via the installed console command:

.. code-block:: bash

    # Print summary report to standard output
    sales -i data/sample_sales.csv

    # Apply 10% discount and save report to a file
    sales -i data/sample_sales.csv --discount 10.0 -o output_report.txt

    # Filter items with total amount not less than 30.0
    sales -i data/sample_sales.csv --threshold 30.0

Running directly via Python:

.. code-block:: bash

    python -m app.main -i data/sample_sales.csv
