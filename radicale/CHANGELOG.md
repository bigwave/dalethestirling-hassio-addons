<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.0.0

- Initial release of the Radicale CalDAV & CardDAV server add-on
- Built on top of official Home Assistant Alpine base image (`hassio-addons/base:20.0.1`)
- S6-overlay v3 process supervision and lifecycle management
- CalDAV (calendars, tasks) and CardDAV (contacts) server support using Radicale 3.x
- Built-in web management interface enabled on port 5232
- User authentication with secure bcrypt password hashing
- Support for multiple storage locations (`addon_config`, `share`, `internal`)
- Automatic configuration and rights generation on first boot
- Access control list / rights configuration support for multi-user setups
- Multi-architecture support for `aarch64` and `amd64`
