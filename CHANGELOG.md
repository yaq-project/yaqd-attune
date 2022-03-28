# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2022.3.0]

### Changed
- No longer reset to destination when zero position is set, instead update current state to reflect change without changing underlying motor position.

### Fixed
- Avoid writing tuple `hw_limits` to state, which prevents state file from writing

## [2022.1.0]

### Added
- Methods to standardize access to dependent hardware

## [2021.12.0]

### Added
- Actual yaqc-qtpy entry point guis for opa and delay

## [2021.10.0]

### Added
- support for yaqc-qtpy entry point (currently placeholder)
- yaqd-attune-delay daemon for spectral delay correction

### Changed
- Convert YEP-111 fields into properties, including additional getters

### Fixed
- Allow for `null` to be passed as the control tune, disables offset from that control.

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

[Unreleased]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2022.3.0...master
[2022.3.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2022.1.0...v2022.3.0
[2022.1.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.12.0...v2022.1.0
[2021.12.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.10.0...v2021.12.0
[2021.10.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.9.0...v2021.10.0
[2021.9.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.3.0...v2021.9.0
[2021.3.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.2.0...v2021.3.0
[2021.2.0]: https://gitlab.com/yaq/yaqd-attune/-/compare/v2021.1.0...v2021.2.0
[2021.1.0]: https://gitlab.com/yaq/yaqd-attune/-/tags/v2021.1.0
