from src.report import AdocReport, MarkdownReport, Report


def test_report_initialization():
    report = Report()
    assert report.statistics == []
    assert report.board == ""
    assert report.report_format == "markdown"


def test_add_statistic():
    report = Report()
    report.add_statistic("Test statistic")
    assert report.statistics == ["Test statistic"]


def test_report_str_empty():
    report = Report()
    assert str(report) == ""


def test_markdown_report_initialization():
    report = MarkdownReport()
    assert report.report_format == "markdown"
    assert report.statistics == []
    assert report.board == ""


def test_markdown_generate_report():
    report = MarkdownReport()
    report.add_statistic("First stat")
    report.add_statistic("Second stat")
    report.generate_report()
    expected_output = (
        "##############   markdown   ##############\n"
        "### First stat\n"
        "### Second stat\n"
    )
    assert report.board == expected_output
    assert str(report) == expected_output


def test_adoc_report_initialization():
    report = AdocReport()
    assert report.report_format == "adoc"
    assert report.statistics == []
    assert report.board == ""


def test_adoc_generate_report():
    report = AdocReport()
    report.add_statistic("First stat")
    report.add_statistic("Second stat")
    report.generate_report()
    expected_output = (
        "**************   adoc   **************\n"
        "*** First stat\n"
        "*** Second stat\n"
    )
    assert report.board == expected_output
    assert str(report) == expected_output
