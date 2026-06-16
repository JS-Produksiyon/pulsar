# Notes for Pulsar v.2.0

## List of settings

### General Settings

* Interface
  *  Display mode → light, dark, system
  * Interface Language
* Startup behavior
  * Start in tray
  * Start at login
* Connection Behavior
  * Single profile or multiple profile
  * Keep-alive ping interval
* Locations
  * Log file location
  * Nebula location → find in system PATH or point to a 
    binary location

***-- DONE --***

### Profile settings

* Profile name
* Auto-connect
* List of remote hosts
* Resolve hosts (boolean to write to hosts file on connection)
* Use ping to keep up
* Log level
* Nebula information → we will embed all information directly
  into the config file, including the ca content. See the Nebula
  documentation wiki at https://nebula.defined.net
  * Allow for a to select a config.yaml file which is then parsed and turned into a full configuration.
  * Follow a sample client config.yaml file for all of the sections
  * From a display perspective, when editing the fields, they'll 
    mostly be text boxes, except for the static_host_map and the 
    outbound/inbound ports on the firewall, which will use a 
    table-based layout.

***-- DONE --***

### Examples

This is how the produced config.yaml files need to have the ca, cert, and key set up under `pki`. That way we can keep everything in a single file for easier storage and access.

```yaml
    pki:
        ca: |
            -----BEGIN NEBULA CERTIFICATE-----
            [base64-encoded CA cert here – paste the full multi-line content]
            -----END NEBULA CERTIFICATE-----

        cert: |
            -----BEGIN NEBULA CERTIFICATE-----
            [base64-encoded host/node cert here]
            -----END NEBULA CERTIFICATE-----

        key: |
            -----BEGIN NEBULA ED25519 PRIVATE KEY-----
            [base64-encoded private key here]
            -----END NEBULA ED25519 PRIVATE KEY-----
```

The ca and cert need to also be available as separate files to be able to check the validity of the ca and the cert using `nebula-cert`.

## Program modules and functionality

The program is in the `src` directory.

### Main Module (pulsar.py)

The main module is the application. It loads all the submodules and starts the application, loading the global `SETTINGS` object and starting the system tray icon and instantiating the windows. It contains the commands to trigger the shutdown of the application either from the system tray icon or from the window being closed, depending on what is in the `exit_on_window_close` key in `settings.json` and the global `SETTINGS` object.

* Holds the core commands needed to run Pulsar:
  * Connect
  * Disconnect
  * Exit

### General utilities (system/utils.py)

* timestamp utility → creates a timestamp of right now in YYYY-mm-ddThh:mm:ssZ±hh:00 format

* touch utility → creates a file in a location passed to the utility

* zip/unzip utility → needed in case the yaml is uploaded as a ZIP file

### System tray icon manager (system/trayIcon.py)

This module handles passes the PulsarTray class to the main module and does the following:

* Creates the tray module.

* Localizes the tray module.

* Manages the menu in the tray icon.

* Sends the menu commands from the tray icon to the base pulsar commands.

* Manages the change in icon if Pulsar is connected or disconnected.

### Nebula Connection manager (system/nebulaConnection.py)

This module provides the NebulaConnection Class that allows for the connection of each connection to the Nebula network using a separate thread.

* Handles the privilege elevation per connection.

* Adds / removes the DNS resolution lines from the hosts file.

* Checks to make sure the connection is active.

* Keeps the connection alive using ping (if so configured).

* Writes the output of the current connection to the selected log file.

### Nebula configuration file manager (system/nebulaConfig.py)

This module tracks and manages the various Nebula configuration files, which are stored in the `instance` directory.

* It reads from and writes to the various `.yaml` files.

* It validates the `.yaml` files.

* It parses the content from the `.yaml` file for display in the GUI and passes it to the HTML frontend in JSON.

* Handles importing the configuration from a `.zip` or a `.yaml` file.

* Individual nebula configuration files are stored in `instance` as `A-config.yaml` through `E-config.yaml`.

* When reading in the connection data, the IP address and expiration date of the connection cert can only be ascertained if nebula_cert is present. If not, these are left empty.

### System settings management (system/settings.py)

The system settings management module handles all functions and features concerning the settings by providing the PulsarSettings class to the system. It can do the follows:

* Exposes the active settings to the application globally as a single entity.

* Tracks any changes made to the settings by the GUI.

* Reads from and writes to the `instance/settings.json` file for persistence.

### Log file display (system/log.py)

* Reads in the various log files stored in the `/instance` folder. 

* Reverses the order and passes `n` (defaults to 30 lines) to the querying item.

### GUI management (gui/gui.py)

* Contains the code to draw the two windows:
  1. The main connection window (fixed size; depending on setting can close application).
  2. The settings and logs window (resizable; cannot close application).

* Exposes the functions necessary for the frontend and back end functions to talk to each other.

### GUI source files (gui/web/*)

Contains all the files necessary for displaying the front end. Basically is a clone of the `design-web` directory.

Under the `gui/web/js` folder, front-end only commands will be located at `frontend.js`. The `design-web/js/settingsMenu.js` and `design-web/js/connectionAnimation.js` files need to be pulled into `frontend.js`. Any command that connects to the back end will be located in `backend.js`. 

### Localization management (gui/localize.py)

* Localization is done by the use of [language-code].json files located under `gui/web/js/i18n/`

* This module exposes these localized strings to the Python side for localized responses as a `PulsarLocalize` class.

* The class checks to see which language code files are available in the i18n subdirectory and updates the dropdown in the title

Localization JSON structure:

```json
{
  "language": {
    "code": "en", // language code
    "foreignNames": {
      "ar": "Arabic",
      "bg": "Bulgarian",
      "cs": "Czech",
      "da": "Danish",
      "de": "German",
      "el": "Greek",
      "en": "English",
      "es": "Spanish",
      "fi": "Finnish",
      "fr": "French",
      "he": "Hebrew",
      "hi": "Hindi",
      "hr": "Croatian",
      "hu": "Hungarian",
      "id": "Indonesian",
      "it": "Italian",
      "ja": "Japanese",
      "ko": "Korean",
      "ms": "Malay",
      "nb": "Norwegian Bokmål",
      "nl": "Dutch",
      "pl": "Polish",
      "pt": "Portuguese",
      "ro": "Romanian",
      "ru": "Russian",
      "sk": "Slovak",
      "sl": "Slovenian",
      "sv": "Swedish",
      "th": "Thai",
      "tr": "Turkish",
      "uk": "Ukranian",
      "vi": "Vietnamese",
      "zh-tw": "Chinese Traditional",
      "zh": "Chinese Simplified"      
    },
    "nativeName": "English",
  },
  "strings":{
    "frontEnd": {
      "placeholders": {
        "key": "string"
      },
      "strings": {},
      "titles": {},
    },
    "backEnd": {
      "key": "string"
      }
  },
  "translator": "",
  "updated": "" // ISO 8601 Date or timestamp 
}
```

## Description of how the application is to work and be put together

When the application starts up it does the following:

1. It checks for instance/settings.json and reads the data into the system. If settings.json does not exist, it creates an empty version of it like so:

    ```python
    {
      'settings_version': __version__,
      'language': locale.languageToCode(locale.language()),
      'display_mode': 'system',
      'exit_on_window_close': False,
      'tray_start': True, 
      'multiple_connections': False,
      'ping_interval': 300, 
      'timestamp': '', 
      'nebula_path': 'system path',
      'connections': {
        'A': {
          'enabled': True,
          'auto_connect': False,
          'keep_alive': True,
          'disable_ping': False,
          'nebula_config': 'instance/connectionA.yaml',
          'private_ip': '',
          'cert_expiration': '',
          'resolve_hosts': True,
          'hosts_list': [
            {'host_name': '', 'host_ip': ''}
          ],
          'log_level': 'info', 
          'nebula_log': 'instance/connectionA.log'
        },
      }
    }
    ```

2. It checks for the nebula binary, depending on `nebula_path`. 

    If the nebula binary does not exist, the main window is displayed with the Connect button(s) disabled (regardless of the status of `tray_start`), the General Settings window is opened and a system native error dialog is displayed with the message, "Nebula binary could not be found. Please either add it to the system path, or else define its location using the settings window."

3. If the nebula binary is found, application starts according to the connection information in `settings.json`.
    
    1. If `tray_start` is set to true, only start in the tray, otherwise open the connection window.

    2. For each connection check for the `auto_connect` boolean. If `True`, start the connection; however, make sure that there is at least 0.5 seconds between triggering each connection separately.

## Moving forward

1. Build `pulsar.py`, `trayIcon.py`, `settings.py`, and `gui`, along with any utility functions necessary in `utils.py`. Make sure the application starts up.

2. Build NebulaConnect.py and NebulaConfig.py and connect them to the frontend.

---
Updated: 2026-06-09
