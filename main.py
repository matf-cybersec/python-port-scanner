#!/usr/bin/env python3
"""Entry point for the Python TCP port scanner."""

import argparse
import logging
import sys
from pathlib import Path

try:
    from colorama import init as colorama_init
except ImportError:  # pragma: no cover
    def colorama_init(*args, **kwargs):
        return None

from scanner.output import OutputManager
from scanner.scanner import PortScanner
from scanner.utils import parse_port_list, setup_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner for cybersecurity learning.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--host", required=True, help="Hostname or IP address to scan")
    parser.add_argument(
        "--ports",
        default="1-1024",
        help="Ports to scan as a comma-separated list and ranges (for example: 22,80,443,8000-8100)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Socket timeout for TCP connection attempts in seconds",
    )
    parser.add_argument(
        "--banner",
        action="store_true",
        help="Attempt optional banner grabbing on open ports",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use thread-based concurrency for faster scanning",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=20,
        help="Number of threads to use in fast scan mode",
    )
    parser.add_argument(
        "--export",
        choices=["json", "txt"],
        help="Export scan results to JSON or TXT file",
    )
    parser.add_argument(
        "--output",
        help="Output file path when exporting results",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    colorama_init(strip=args.no_color)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logger(log_level)

    try:
        ports = parse_port_list(args.ports)
    except ValueError as exc:
        logging.error("Invalid port range: %s", exc)
        return 1

    if args.export and not args.output:
        logging.error("Export mode requires --output file path")
        return 1

    if not args.fast and args.threads > 1:
        logging.debug("Thread count is ignored when fast scan mode is disabled")

    output_manager = OutputManager()
    scanner = PortScanner(
        host=args.host,
        ports=ports,
        timeout=args.timeout,
        banner_grab=args.banner,
        use_threads=args.fast,
        thread_count=args.threads,
        verbose=args.verbose,
    )

    try:
        results = scanner.run()
        output_manager.print_summary(results)

        if args.export:
            output_path = Path(args.output)
            output_manager.export(results, args.export, output_path)
            logging.info("Results saved to %s", output_path)

        return 0
    except KeyboardInterrupt:
        logging.warning("Scan interrupted by user (Ctrl+C)")
        return 1
    except ValueError as exc:
        logging.error(str(exc))
        return 1
    except Exception as exc:
        logging.exception("Unexpected error during scan: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
