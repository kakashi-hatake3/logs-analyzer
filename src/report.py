class Report:
    """Создание отчета."""

    def __init__(self):
        self.statistics = []

    def add_statistic(self, stat):
        """Добавляет статистику в список для отчета"""
        self.statistics.append(stat)

    def generate_report(self, report_format='markdown'):
        """Генерирует отчет в формате markdown или adoc"""

        if report_format is None:
            report_format = 'markdown'

        report_lines = []

        # Генерация отчета для каждого элемента статистики
        for stat in self.statistics:
            stat_data = stat.get()
            for title, value in stat_data.items():
                if report_format == 'markdown':
                    report_lines.append(f"### {title}\n")
                    report_lines.append(f"- **Value:** {value}\n\n")
                elif report_format == 'adoc':
                    report_lines.append(f"== {title}\n")
                    report_lines.append(f"* Value: {value}\n\n")

        return ''.join(report_lines)
