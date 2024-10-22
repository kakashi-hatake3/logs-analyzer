from enum import StrEnum


class Formats(StrEnum):
    adoc = "adoc"
    markdown = "markdown"


class PathTypes(StrEnum):
    url = "url"
    local = "local"


class InputParameters(StrEnum):
    path = "path"
    from_date = "from"
    to_date = "to"
    file_format = "format"
    filter_field = "filter-field"
    filter_value = "filter-value"


class LogFields(StrEnum):
    ip = "ip"
    client_id = "client_id"
    user_id = "user_id"
    time_local = "time_local"
    method = "method"
    path = "path"
    protocol = "protocol"
    status_code = "status_code"
    response_size = "response_size"
    referrer = "referrer"
    agent = "agent"
