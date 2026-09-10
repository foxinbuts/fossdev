"""Integration tests for the CLI interface."""

import pytest
from sales.cli import main


def test_cli_stdout(sample_csv_file, capsys):
    """Test standard CLI invocation printing report to stdout."""
    exit_code = main(["-i", sample_csv_file])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "drinks: 72.5" in captured.out
    assert "Total: 152.1" in captured.out


def test_cli_positional_arg(sample_csv_file, capsys):
    """Test passing input file as positional argument."""
    exit_code = main([sample_csv_file])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Total: 152.1" in captured.out


def test_cli_output_file(sample_csv_file, tmp_path):
    """Test writing report to an output file."""
    out_file = tmp_path / "output_report.txt"
    exit_code = main(["-i", sample_csv_file, "-o", str(out_file)])
    assert exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "Total: 152.1" in content


def test_cli_threshold(sample_csv_file, capsys):
    """Test CLI with minimum line item threshold."""
    exit_code = main(["-i", sample_csv_file, "-t", "30.0"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "drinks: 72.5" in captured.out
    assert "bakery: 30.4" in captured.out
    assert "fruit" not in captured.out


def test_cli_discount(sample_csv_file, capsys):
    """Test CLI with discount argument."""
    exit_code = main(["-i", sample_csv_file, "-d", "10.0"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Total: 136.89" in captured.out


def test_cli_missing_input(capsys):
    """Test CLI without arguments returns error code 1."""
    exit_code = main([])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error: input file must be specified" in captured.err


def test_cli_file_not_found(capsys):
    """Test CLI with missing file returns error code 1."""
    exit_code = main(["-i", "non_existent_file.csv"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Input sales file not found" in captured.err


def test_cli_invalid_discount(sample_csv_file, capsys):
    """Test CLI with invalid discount returns error code 1."""
    exit_code = main(["-i", sample_csv_file, "-d", "150.0"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Validation error:" in captured.err


def test_cli_version(capsys):
    """Test --version flag exits cleanly."""
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0


def test_cli_unexpected_error(sample_csv_file, monkeypatch, capsys):
    """Test handling of unexpected exceptions."""
    def broken_read(_):
        raise RuntimeError("Disk explosion")

    monkeypatch.setattr("sales.cli.read_data", broken_read)
    exit_code = main(["-i", sample_csv_file])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Unexpected error: Disk explosion" in captured.err

