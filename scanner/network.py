"""Network operations for TCP connect scan logic."""

import logging
import socket
from dataclasses import dataclass
from typing import Optional, Tuple

from scanner.banner import grab_banner


@dataclass
class PortCheckResult:
    port: int
    is_open: bool
    banner: Optional[str]
    error: Optional[str]


def create_tcp_socket(timeout: float) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    return sock


def scan_port(
    host: str,
    port: int,
    timeout: float,
    banner_grab: bool = False,
) -> PortCheckResult:
    """Try to connect to a TCP port and optionally perform banner grabbing."""
    logging.debug("Scanning port %d on %s", port, host)
    sock = create_tcp_socket(timeout)
    try:
        result = sock.connect_ex((host, port))
        if result != 0:
            return PortCheckResult(port=port, is_open=False, banner=None, error=None)

        banner_data = None
        if banner_grab:
            banner_data = grab_banner(sock, timeout)

        return PortCheckResult(port=port, is_open=True, banner=banner_data, error=None)
    except socket.timeout:
        logging.debug("Timeout while scanning port %d", port)
        return PortCheckResult(port=port, is_open=False, banner=None, error="timeout")
    except OSError as exc:
        logging.debug("Socket error on port %d: %s", port, exc)
        return PortCheckResult(port=port, is_open=False, banner=None, error=str(exc))
    finally:
        try:
            sock.close()
        except OSError:
            pass
