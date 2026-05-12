"""Utility helpers for port parsing, service identification, and logging setup."""

import logging
import re
import socket
from typing import Dict, List

COMMON_SERVICES: Dict[int, str] = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    161: "snmp",
    389: "ldap",
    443: "https",
    587: "smtp-submission",
    631: "ipp",
    3306: "mysql",
    3389: "rdp",
    5900: "vnc",
    8080: "http-alt",
}

_PORT_RANGE_RE = re.compile(r"^\s*(\d{1,5})(\s*-\s*(\d{1,5}))?\s*$")


def setup_logger(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
    )


def parse_port_list(port_string: str) -> List[int]:
    """Parse a comma-separated list of ports and ranges into individual ports."""
    if not port_string:
        raise ValueError("Port string is empty")

    ports: List[int] = []
    parts = port_string.split(",")

    for part in parts:
        match = _PORT_RANGE_RE.match(part)
        if not match:
            raise ValueError(f"Invalid port token: {part}")

        start = int(match.group(1))
        end = int(match.group(3)) if match.group(3) else start

        if start < 1 or end > 65535 or start > end:
            raise ValueError(f"Invalid port range: {part}")

        ports.extend(range(start, end + 1))

    unique_ports = sorted(set(ports))
    if len(unique_ports) > 1024:
        logging.warning("Scanning more than 1024 ports may take a while")

    return unique_ports


def get_service_name(port: int) -> str:
    """Return a human-readable service name for a given port."""
    return COMMON_SERVICES.get(port, "unknown")


def resolve_host(host: str) -> str:
    """Resolve hostname to IPv4 address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc
