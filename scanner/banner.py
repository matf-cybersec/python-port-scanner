"""Banner grabbing support for open TCP services."""

import logging
import socket
from typing import Optional


def grab_banner(sock: socket.socket, timeout: float = 1.0) -> Optional[str]:
    """Read a small banner from a connected socket if available."""
    try:
        sock.settimeout(timeout)
        data = sock.recv(1024)
        if not data:
            return None

        try:
            return data.decode("utf-8", errors="replace").strip()
        except (UnicodeDecodeError, OSError) as exc:
            logging.debug("Banner decode error: %s", exc)
            return None
    except socket.timeout:
        logging.debug("No banner received within timeout")
        return None
    except OSError as exc:
        logging.debug("Socket error during banner grab: %s", exc)
        return None
