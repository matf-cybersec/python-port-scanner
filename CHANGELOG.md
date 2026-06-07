# Changelog

All notable changes to this project are tracked in this file.

## [Unreleased]

### Added

- `--no-color` CLI flag to disable ANSI color output.
- Fast scan mode via `--fast` and configurable worker threads using `--threads`.
- Export support for `json` and `txt` formats using `--export` and `--output`.
- Detailed scan summary counts for open, closed, filtered, and error results.
- Improved CLI validation and error handling for invalid port input and missing output paths.

### Changed

- Timeout results now report `filtered` status when the port does not respond.
- File exports now include banner and error details for open and filtered ports.
- README updated with current CLI usage examples, export behavior, and screenshots.
- Logging improved with `--verbose` debug output and clearer host resolution messages.

### Fixed

- Thread count is only applied when `--fast` mode is enabled.
- Network errors are mapped to readable statuses such as connection refused, host unreachable, and timeout.
- Output formatting now shows error details when available.
