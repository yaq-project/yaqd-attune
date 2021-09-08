# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2021.9.0]

### Fixed
- Errant type for `set_position_except` that allowed strings to be passed
- Provide units (currently statically "nm")

### Changed
- prefer double over float over the yaq interface
- config now accepts host:port (string) as well as port alone (int)

## [2021.3.0]

### Added
- Ability to use Discrete tunes/motors

### Fixed
- added forgotten config options to is-daemon: enable, log_level, and log_to_file

## [2021.2.0]

- fix stringified numbers if no arrangement is set

## [2021.1.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.9.0...master
[2021.9.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.3.0...v2021.9.0
[2021.3.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.2.0...v2021.3.0
[2021.2.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.1.0...v2021.2.0
[2021.1.0]: https://gitlab.com/yaq/yaqd-attune/-/tags/v2021.1.0
