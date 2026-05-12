"""Output management for printing and exporting scan results."""

import json
import logging
from pathlib import Path
from typing import Iterable, List

try:
    from colorama import Fore, Style
except ImportError:  # pragma: no cover
    class _ColorFallback:
        RESET_ALL = ""
        GREEN = ""
        RED = ""
        YELLOW = ""

    Fore = _ColorFallback()
    Style = _ColorFallback()

from scanner.scanner import ScanResult


class OutputManager:
    def print_summary(self, results: Iterable[ScanResult]) -> None:
        open_ports = 0
        for result in results:
            line = self._format_result(result)
            print(line)
            if result.status == "open":
                open_ports += 1

        total_ports = len(list(results))
        print()
        print(f"Scanned {total_ports} ports, {open_ports} open")

    def export(self, results: Iterable[ScanResult], export_format: str, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        if export_format == "json":
            self._export_json(results, path)
        elif export_format == "txt":
            self._export_txt(results, path)
        else:
            raise ValueError("Unsupported export format")

    def _format_result(self, result: ScanResult) -> str:
        if result.status == "open":
            status_text = f"{Fore.GREEN}[OPEN]{Style.RESET_ALL}"
        elif result.status == "closed":
            status_text = f"{Fore.RED}[CLOSED]{Style.RESET_ALL}"
        else:
            status_text = f"{Fore.YELLOW}[{result.status.upper()}]{Style.RESET_ALL}"

        banner_text = f" - {result.banner}" if result.banner else ""
        return f"{status_text} {result.port}/tcp - {result.service}{banner_text}"

    def _export_json(self, results: Iterable[ScanResult], path: Path) -> None:
        serialized = [
            {
                "port": result.port,
                "status": result.status,
                "service": result.service,
                "banner": result.banner,
                "error": result.error,
            }
            for result in results
        ]
        try:
            path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")
        except OSError as exc:
            logging.error("Failed to write JSON export: %s", exc)
            raise

    def _export_txt(self, results: Iterable[ScanResult], path: Path) -> None:
        lines: List[str] = []
        for result in results:
            banner_text = f" | banner: {result.banner}" if result.banner else ""
            error_text = f" | error: {result.error}" if result.error else ""
            lines.append(
                f"{result.port}/tcp {result.status} {result.service}{banner_text}{error_text}"
            )

        try:
            path.write_text("\n".join(lines), encoding="utf-8")
        except OSError as exc:
            logging.error("Failed to write TXT export: %s", exc)
            raise
