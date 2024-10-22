import pytest

from src.report import AdocReport, MarkdownReport, Report


# Тест для базового класса Report
def test_report_initialization():
    report = Report()
    assert report.statistics == []  # Проверка, что список статистики пустой
    assert report.board == ''  # Проверка, что изначально нет текста отчета
    assert report.report_format == "markdown"  # По умолчанию формат markdown

def test_add_statistic():
    report = Report()
    report.add_statistic("Test statistic")
    assert report.statistics == ["Test statistic"]  # Статистика была добавлена

def test_report_str_empty():
    report = Report()
    assert str(report) == ''  # Проверка пустого отчета (метод __str__)

# Тесты для MarkdownReport
def test_markdown_report_initialization():
    report = MarkdownReport()
    assert report.report_format == "markdown"  # Формат должен быть markdown
    assert report.statistics == []  # Пустая статистика
    assert report.board == ''  # Пустое поле для отчета

def test_markdown_generate_report():
    report = MarkdownReport()
    report.add_statistic("First stat")
    report.add_statistic("Second stat")
    report.generate_report()
    expected_output = (
        '##############   markdown   ##############\n'
        '### First stat\n'
        '### Second stat\n'
    )
    assert report.board == expected_output  # Проверка правильности генерации отчета
    assert str(report) == expected_output  # Проверка работы __str__


# Тесты для AdocReport
def test_adoc_report_initialization():
    report = AdocReport()
    assert report.report_format == "adoc"  # Формат должен быть adoc
    assert report.statistics == []  # Пустая статистика
    assert report.board == ''  # Пустое поле для отчета

def test_adoc_generate_report():
    report = AdocReport()
    report.add_statistic("First stat")
    report.add_statistic("Second stat")
    report.generate_report()
    expected_output = (
        '**************   adoc   **************\n'
        '*** First stat\n'
        '*** Second stat\n'
    )
    assert report.board == expected_output  # Проверка правильности генерации отчета
    assert str(report) == expected_output  # Проверка работы __str__

# Запуск тестов с помощью pytest.
