# Home Assistant Add-on: Radicale

_Radicale is a lightweight CalDAV (calendars, todo-lists) and CardDAV (contacts) server._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

This add-on provides a fully functional Radicale CalDAV and CardDAV server running within the Home Assistant OS / Supervised Docker environment. It is built on top of the official Home Assistant base Alpine image and follows modern add-on conventions including S6-overlay process supervision and Bashio logging.

## Features

- **CalDAV Server**: Sync calendars and to-do / task lists across devices.
- **CardDAV Server**: Sync address books and contacts across devices.
- **Web Interface**: Built-in web UI to create and manage collections and view CalDAV/CardDAV URLs.
- **Secure Authentication**: Built-in `htpasswd` authentication supporting bcrypt-hashed credentials.
- **Access Control & Rights**: Fine-grained access control with support for private, shared, and read-only calendars.
- **Flexible Storage**: Store collections in `addon_config` (`/config/collections`), `share` (`/share/radicale/collections`), or local internal storage.
- **Wide Client Compatibility**: Seamless integration with iOS, macOS, Android (DAVx5), Mozilla Thunderbird, Windows / Outlook, and Home Assistant's native CalDAV integration.

## Quick Start

1. Install the add-on from your Home Assistant Add-on Store.
2. In the add-on **Configuration** tab:
   - Configure your initial username and password under `users`.
   - Select your preferred `storage_location` (default: `addon_config`).
3. Start the add-on.
4. Access the web interface at `http://<HOME_ASSISTANT_IP>:5232/` to log in and create your first calendar or address book.

See the full installation, client setup, and configuration guide in [DOCS.md](./DOCS.md).
