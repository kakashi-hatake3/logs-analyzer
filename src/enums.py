from enum import StrEnum


class Formats(StrEnum):
    adoc = "adoc"
    markdown = "markdown"


class PathTypes(StrEnum):
    url = "url"
    local = "local"
