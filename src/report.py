class Report:
    """Создание отчета."""

    def __init__(self, report_format="markdown"):
        self.statistics = []
        self.board = ''
        self.report_format = report_format

    def add_statistic(self, stat):
        """Добавляет статистику в список для отчета"""
        self.statistics.append(stat)

    def generate_report(self):
        """Генерирует отчет в формате markdown или adoc"""
        pass

    def __str__(self):
        return self.board


class MarkdownReport(Report):

    def __init__(self):
        super().__init__()

    def generate_report(self):
        self.board += f'##############   {self.report_format}   ##############\n'
        for line in self.statistics:
            self.board += f'### {line}\n'


class AdocReport(Report):

    def __init__(self):
        super().__init__()
        self.report_format = "adoc"

    def generate_report(self):
        self.board += f'**************   {self.report_format}   **************\n'
        for line in self.statistics:
            self.board += f'*** {line}\n'
