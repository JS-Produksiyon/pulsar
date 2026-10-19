# Pulsar v.2.0 Project Definition File

Pulsar is a cross-platform Python-based GUI wrapper for Slack's Nebula mesh network client. It has the following features:

- It runs in the notification area with an icon that denotes connectivity and provides a quick-access menu for connecting/disconnecting.
- It provides a GUI window to manage connectivity.
- The GUI will display in both light mode and dark mode.
- It provides a second GUI window to manage settings and about information.
- It uses the existing Nebula installation, which it loads using an elevated command prompt.
- It can start up to five separate Nebula instances at one time, but defaults to a single instance for simplicity.
- It manages all of the Nebula configuration files through the user interface.
- It can import existing Nebula configurations both in zipped and in individual file format.
- If more than one Nebula connection exists, it allows the connection to be turned on or off through the GUI.
- Each connection can be edited through the GUI interface.
- The GUI interface is multilingual and easily translatable.
- The project is to be open source, preferably under GPL 3.0 or whatever version is current

Each of these features and how they are to work are described individually below.

## 1. System Tray Interface

- The system tray will be provided using the `pysystray` module.
- The icons are found in the `src/gui/img` folder relative to the project root. `pulsar-icon-black-64.png` and `pulsar-icon-white-64.png` will be preferred for the offline states and `pulsar-icon-64.png` will be preferred for the connected state.
- The icon needs to change to `pulsar-icon-64.png` when the connection is established. 
- During establishment and when the connection is not established, use the the black icon for light mode and the white icon for dark mode display. These icons need to follow the system interface style rather than the light/dark mode defined in 3. Light and Dark Mode.
- Right-clicking pops up a menu with the following options:
  - Connect to Nebula network → If multiple connections are set, this becomes a flyout menu with each active connection as an individual item and a *Connect to All* option  at the bottom.
  - Disconnect from Nebula netowrk → Follows the same logic as Connect to Nebula network above, just disconnecting.
  - Show Pulsar Window → Opens the main GUI window
  - Settings... → Opens the settings window
  - About... → Opens the about window
  - Quit Pulsar → Disconnects all connections and closes Pulsar; A native confirmation dialog is popped up if any connections are still active asking for confirmation of closing the application.

## 2. The GUI

- The GUI will be provided using `pywebview`, allowing for HTML/CSS/JS coding with animations etc.
- The GUI will be rendered using the built-in rendering engine of `pywebview`. No Flask or third-party packages will be used.
- The icons for the GUI are found in `src/gui/img` and are available as .png (cross-platform), .icns (Mac), and .ico (Windows).

### 2.1 Light and Dark Mode

- The application will render in both a dark mode and a light mode interface.
- The program will provide a snippet of code that will determine the current setting of the OS to render the interface in the correct mode.
- If the OS color mode cannot be determined, the program will default to dark mode (e.g. for Linux).
- The interface will initially follow the system preference.
- The interface can be set to the user's preference for light mode or dark mode on the Settings page. This value is stored in the `instance/settings.yaml` file (see [2.3.1 Settings](#231-settings)).
- Light and dark mode are controlled in the interface by setting the `data-bs-theme` attribute in the `html` tag and the `class` attribute in the `body` tag to `light` or `dark` respectively. This needs to be able to be toggled  via JavaScript. (see [2.3.1 Settings](#231-settings)).

### 2.2 Primary GUI Window

- The design for the primary GUI Window is already completed using HTML/CSS/JS. All necessary files are located in `src/gui/web`.
- The primary GUI window size is to be 520px x 520px, 
- The primary GUI window is frameless (i.e. does not have the system-based title and border).
- The primary GUI window is not resizable. It needs to be able to handle the dynamic resolution-based resizing that Windows provides (e.g. 100% enlargement on FullHD and 200% enlargement on 4k).
- Upon opening, the window appears centered on the user's main monitor.
- Light and dark mode are managed
- Clicking and dragging the `#drag-bar` DIV will move the window around the screen. This needs to be handled with a combination of frontend JavaScript and backend `pywebview` functionality. The code for this is in `src/gui/web/js/windowDrag.js`.
- The buttons at the top of the GUI function as follows:

| Button ID    | Action                                                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| btnReconnect | Executes a disconnect, waits a second, executes connect.                                                                           |
| btnSettings  | Opens the secondary GUI window containing the Settings page. (Replaces the About page, if open)                                    |
| btnAbout     | Opens the secondary GUI window containing the About page. (Replaces the Settings page, if open)                                    |
| btnHelp      | Opens the help wiki on the public repository page in a separate web browser                                                        |
| btnClose     | Closes the connection window. If `#switchCloseOnWindow` is checked, it closes down all connections and the tray  application, too. |

- The button clicks are executed using pywebview's JavaScript bridge. These are to be exposed in `src/gui/web/js/mainWindowBackend.js`. 
- If there is only a single connection defined (multiple connections are disabled in settings.yaml), then the GUI shows the `#pulsar-single-connection` layer. On clicking the connect button the following animation starts. JavaScript for frontend portion of connection animation is found in `src/gui/web/js/connectAnimation.js`.
  - The bottom line animates across at which point the connection begins. The Connect button becomes the Cancel button. This is where the privilege elevation UI should be triggered.
  - Read the output to see if the connection is established and do a ping of the lighthouses.
  - If the ping comes back, color the Nebula icon and animate the top bar back over to the Pulsar icon. The Cancel Button becomes the Disconnect button.
- If there are multiple connections defined then the GUI shows the `#pulsar-multi-connection` layer. Only the connections that are set to active in `settings.yaml` will be displayed in the list (e.g. if there are three connections defined as active, only those three connections are displayed). On connection the animation works as following:
  - The associated `#connect-status-[id]` block's class is set from `disconnected` to `connecting`. The associated `#connect-connect-[id]` button is  replaced with the `#connect-cancel-[id]` button.
  - Once the connection has been checked to be established the associated `#connect-status-[id]` block's class is set from `connecting` to `connected`and the associated `#connect-cancel-[id]` button is  replaced with the `#connect-disconnect-[id]` button. 

  - When the disconnect command is given (either by clicking the Cancel button, Disconnect button or through the Reconnect button), the associated `#connect-status-[id]` block's class is set from whatever it is to `disconnected`and the button is replaced by the `#connect-connect-[id]` button.

- Upon startup the existence of a Nebula instance is checked for. If it cannot be found in the system path, then a native dialog explaining the missing Nebula instance pops up. Clicking OK on the dialog will open the Settings window (see [2.3 Secondary GUI Window](#23-secondary-gui-window)) and scrolls down to the Nebula Binaries (`settings.html#settingGeneralSettingsNebula`) on the Settings page (see [2.3.1 Settings](#231-settings)).
- Upon startup the existence of configured connections is checked (see 2.5 Startup Sequence). If there is no connection configured, then a native dialog is popped up, warning that the connection must be configured. Clicking OK on the dialog will open the Settings window (see [2.3 Secondary GUI Window](#23-secondary-gui-window)) and navigate to the Connections screen (see [2.3.3 Editing Connections](#233-editing-connections)). The Connect button(s) will be disabled until the connection is properly configured.
- If the Close button is clicked while the application is set to shut down when the main GUI window is closed and there are still connections active, a native system dialog is triggered through the pywebview backend warning the user of the connection status and whether they want to close the application, as it will disconnect all of the Nebula connections. The application will only close upon confirmation.
- **Add notes on how the main interface displays the auto-connect icons.**

### 2.3 Secondary GUI Window

- The design for the secondary GUI Window is already completed using HTML/CSS/JS. All necessary files are located in `src/gui/web`.
- The secondary GUI window size is to be 80% of the monitor it appears on. This needs to be calculated when the window is first created. It needs to be able to handle the dynamic resolution-based resizing that Windows provides (e.g. 100% enlargement on FullHD and 200% enlargement on 4k).
- The secondary GUI window is frameless (i.e. does not have the system-based title and border). 
- Upon opening, the window appears centered on the user's main monitor.
- The secondary GUI window is resizable, though this is handled by clicking and dragging the `#resize-handle` DIV. The resizing functionality needs to be handled with a combination of frontend JavaScript and backend `pywebview` functionality. The code for this is in `src/gui/web/js/windowResize.js`.
- Clicking and dragging the `#drag-bar` DIV will move the window around the screen. This needs to be handled with a combination of frontend JavaScript and backend `pywebview` functionality. The code for this is in `src/gui/web/js/windowDrag.js`.
- The buttons in the upper right corner function as follows:

| Button ID | Action |
| --------- | ------ |
| `btnWinMinimize` | Minimizes the secondary window to the taskbar. |
| `btnWinMaximize` | Maximizes the secondary window to fill the whole screen. Is replaced by btnWinRestore when clicked. |
| `btnWinRestore` | Restores the secondary window to its previous size. Is replaced by btnWinMaximize when clicked. |
| `btnWinClose` | Closes the secondary window, *but not the application!*. |

- The maximize, minimize and restore buttons need to use a combination of front-end JavaScript and backend `pywebview` functionality. The code for this is be in `src/gui/web/js/windowResize.js`.
- The secondary GUI window hosts two main pages, settings.html and info-logs.html. It will not navigate between these two. Each one will be loaded separately when needed. Only one instance of the window can be open with one of these pages at a time.
- When the secondary GUI window is open, the primary GUI window needs to be set as inaccessible.
- When the secondary GUI window is closed, the primary GUI window becomes accessible again.
- The settings and connection information are stored in a global SETTINGS class which contains the following functionality:
  - Creates the empty `instance/settings.yaml` file if it does not exist.
  - Loads the information from the `instance/settings.yaml` file.
  - Allows for the alteration of the various settings.
  - Writes the altered data to the `instance/settings.yaml` file for persistence.

#### 2.3.1 Settings

- Application wide settings are provided in `src/gui/web/settings.html` in the `#settings-general` DIV.
- When the `src/gui/web/settings.html` page is loaded, the following information must be populated using the `pywebview` bridge:

| Input ID | Population Method |
| -------- | ----------------- |
| `ifaceLangSelect` | populated by reading the language JSON files in `src/gui/web/js/i18n`. See [2.4 Multilingual Features and Localization](#24-multilingual-features-and-localization) for how localization works. |
| `ifaceDisplayModeSelect` | set according to the value of `display_mode` in global SETTINGS object |
| `switchCloseOnWindow` | set according to the value of `exit_on_window_close` in the SETTINGS object |
| `switchStartupTray` | set according to the value of `tray_start` in the SETTINGS object |
| `switchStartupLogin` | set according to the value of `start_on_login` in the SETTINGS object |
| `switchMultipleConnections` | set according to the value of `multiple_connections` in the SETTINGS object |
| `inputPingInterval` | populated according to the value of `ping_interval` in the SETTINGS object |
| `nebulaBinariesSysPath` | set as clicked if `nebula_path` in the SETTINGS object is equal to `system path` |
| `nebulaBinariesFilePath` | set as clicked if `nebula_path` in the SETTINGS object is *not* equal to `system path` |
| `nebulaBinariesFilePathBox` | set as the value of `nebula_path` in the SETTINGS object, if `nebula_path` is not equal to `system_path`; otherwise left empty |

- When the settings page is opened the presence of the nebula binaries is checked using the global NebulaControl class (see [3. Nebula Integration](#3-nebula-integration)). Depending on the content found there the following information is modified:
  - Depending on the presence of the `nebula` binary in the selected location:
    - If present `txtNebulaBinaryFound` is displayed, `txtNebulaBinaryNotFound` is hidden.
    - If not present `txtNebulaBinaryFound` is hidden, `txtNebulaBinaryNotFound` is displayed.
  - Depending on the presence of the `nebula-cert` binary in the selected location:
    - If present `txtNebulaCertBinaryFound` is displayed, `txtNebulaCertBinaryNotFound` is hidden.
    - If not present `txtNebulaCertBinaryFound` is hidden, `txtNebulaCertBinaryNotFound` is displayed.

- When a setting is changed, mark the page as dirty. Trigger the change transfer to the back end 500 ms after the change is made, allowing for multiple clicks and keeping the alteration down. 
  - When the write is finally triggered *all* general settings data are sent to the backend for processing.
  - If `btnWinClose` is clicked before the latest update to the settings has been completed, wait for the update to complete, *then* close the window.

- A setting is considered changed as follows:
  - When a switch (`<input type="checkbox">`) is flipped.
  - When a radio button is selected.
  - When a dropdown selection changes.
  - When an input box is blurred.

- If a different interface language is selected in the `#ifaceLangSelect` dropdown, then the interface immediately switches to that language (see [2.4 Multilingual Features and Localization](#24-multilingual-features-and-localization)).
- If a different display mode is selected in the `#ifaceDisplayModeSelect` dropdown, the interface needs to immediately switch the mode to the selected item. See [2.1 Light and Dark Mode](#21-light-and-dark-mode) for the code that needs to be modified.
- When the `#nebulaBinariesFilePathBrowse` button is clicked, then `pywebview` triggers a folder select dialog that allows the user to browse to the folder where the nebula and nebula-cert binaries are found. The result is pasted into `#nebulaBinariesFilePathBox` and the change is triggered to save it.
- Upon triggering the change of `nebulaBinariesFilePathBox`, the necessary modifications are made to the global NebulaControl class and the information about the nebula and nebula-cert executable files is displayed as listed above.

#### 2.3.2 Multiple Connections

- The `#switchMultipleConnections` is populated from SETTINGS.connections upon opening the settings page.
  - The rows are populated according to the letter assigned to the connection. E.g. A populates `#connectionA[title]`. 
  - If a given connection is not found in SETTINGS.connections, it is left in the default empty format.
  - connectionA is the primary connection that is always populated initially, as it contains the single connection.
  - The connection items are populated as follows where `[x]` is equal to the connection letter:
    - `#connection[x]SwitchEnable` is set to checked if `enabled` is true.
    - `#connection[x]Title` is set to the content of `name`.
    - If `enabled` is true, then the `.connection-autoconnect` and `.connection-keepalive` buttons with the related `data-connect-id` attribute are enabled; otherwise they are set to `disabled.
    - If `auto_connect` is true, the `.connection-autoconnect-true` span under the `.connection-autoconnect` button with the related `data-connect-id` is set to `display: inline-block` and the span `.connection-autoconnect-false` is set to `display: none`. This is inverted if `auto_connect` is false.    
    - If `keep_alive` is true, the `.connection-keepalive-true` span under the `.connection-keepalive` button with the related `data-connect-id` is set to `display: inline-block` and the span `.connection-keepalive-false` is set to `display: none`. This is inverted if `auto_connect` is false.

- If `#switchMultipleConnections` is set to true, the `#switchMultipleConnections` DIV will be displayed automatically.
- Clicking the `.connection-autoconnect` and `.connection-keepalive` buttons turns on and off the `auto_connect` and `keep_alive` features dynamically, immediately updating the SETTINGS global object and writing the changes to the `settings.yaml` file after a 500ms delay.
  - The writing of the data to the backend follows the same scheme as in [2.3.1 Settings](#231-settings).

- Clicking the `.connection-edit` button will load the given connection in to the connection editing DIV by calling the data from the backend using the `pywebview` bridge, first using the data from `SETTING.connections.[connection id]` and then from the Nebula configuration file defined in `SETTING.connections.[connection id].nebula_config`. For more information see [2.3.3 Editing Connections](#233-editing-connections). The related connection ID (A-E) is found in the `data-connection-id` attribute of the button. Then it will display the `#settings-connection-edit` DIV. The JS code to display this DIV properly is already found in `src/gui/web/js/settingsMenu.js`; only the backend connection is still necessary to load the content.

#### 2.3.3 Editing Connections

- If `multiple_connections` is false in the SETTING class, then this is when the application loads the data first from the `SETTINGS.connections.A` object, then from the connection file defined in `SETTINGS.connections.A.nebula_config`.
- If `multiple_connections` is true, then the data from the passed connection ID should be loaded when the connections `.connection-edit` button is clicked.
- If the configuration file is empty or non-existent, the application will load the empty version of the connection:
  - `#settingsProfileName` is set to `Nebula Mesh Network` (or localized equivalent).
  - `#switchProfileAutoconnect` and `#switchProfileNoPing` are set to not checked.
  - `#switchProfileKeepAlive` is set to checked.
  - All the `.settings-connection-[root/private]-[cert/key]-valid` spans are set to `display: none;`
  - All the ``.settings-connection-[root/private]-[cert/key]-invalid` are set to `display: inline-block;`.
  - `#settings-connection-node-ip` and `#settings-connection-node-expiration` text is set to `Undefined`.
  - `#nodeStaticHostsTable`, `#nodeOutboundConnectionAction`, `#nodeInboundConnectionAction`, and `#hostsTable` have their `<tbody>` emptied of any rows.
  - `#switchUseHosts` checked is removed.

- Configuration content is received from the backend as JSON containing two YAML strings as follows (where `x` is the connection ID as a captial letter from `A-E`) and stored in `window.settings_content`:

  ```json
  {
    'pulsar_settings': 'connections.X YAML string from settings.yaml',
    'nebula_settings': 'content of the connectionX.yaml file as a string'
  }
  ```

- The `pulsar_settings` YAML is parsed and displayed in the GUI as follows:
  - The `.yaml` file is parsed into JSON (prefer `eemeli/yaml`).
  - The content in `name` is written into `#settingsProfileName`.
  - `#switchProfileAutoconnect` is set to `checked` if `auto_connect` is true. `checked` is removed, if false.
  - `#switchProfileKeepAlive` is set to `checked` if `keep_alive` is true and `#switchProfileNoPing` is set to disabled. `checked` is removed, if false and `#switchProfileNoPing` is enabled.
  - `#switchProfileNoPing` is set to `checked` if `disable_ping` is true. `checked` is removed, if false.
  - `#switchUseHosts` is set to `checked` if `resolve_hosts` is true. `checked` is removed, if false.
  - If there are entries in `hosts_list` these are parsed and written into `#hostsTable` with the data in `host_name` in the first column and `host_ip` in the second. Each row is given a `data-row-id` attribute that is incremented from the previous one.

- Clicking `#btnImportConfigFile` will start the process to import a Nebula connection configuration file.
  - Valid configuration files are either a `.yaml` file that contains the configuration details, including paths to or fully embedded private key, certificate, and certificate authority, or a `.zip` file that contains all files necessary to enable the connection.
  - The files are selected using an OS native file selection dialog provided by the `pywebview` backend bridge.
  - Upon submission, the file names and the data regarding the profile name, `auto_connect`, `keep_alive`, and `no_ping` are passed to the back end.
  - The back end will open and check the files provided. If the files are invalid, an OS native error dialog box will be triggered by `pywebview` informing the user of what is invalid.
  - The valid information parsed from the files will be loaded into the page.

- The backend validation process is as follows:
  1. The `.yaml` file is parsed and checked against a sample Nebula `config.yaml` file to make sure that it contains the correct headings.
  2. The associated certificate authority, certificate, and private key are validated. These can either be separate files or they can be embedded in the `.yaml` file.
      - If the certificate authority, certificate, and private key are embedded in the `.yaml` file, then they are extracted and saved to separate temporary files in the `src/tmp` directory with the following naming convention below. The temporary files are deleted after verification and IP Address and expiration date extraction.
          - Certificate authority: `[connection ID]-ca.crt`
          - Certificate: `[connection ID].crt`
          - Private key: `[connection ID].key`
      - Certificate and certificate authority need to have `-----BEGIN NEBULA CERTIFICATE` at the top.
      - The private key file needs to have `-----BEGIN NEBULA X25519 PRIVATE KEY` at the top.
      - If the nebula-cert binary is available, then the certificate authority and certificate are verified against each other (`nebula-cert verify -ca ca.crt -crt certificate.crt`) from a hidden command shell. A result of `nil` means that the certificate is valid. Any other result should pop up an error.
  3. The node host name, IP address, and certificate expiration are extracted from the certificate using the nebula-cert binary (if present): `nebula-cert print -path certificate.crt`.
      - The output of the command is JSON.
      - The node hostname is found in `details.name`.
      - The node IP address is found in `details.network[0]`
      - The expiration date is found in `details.notAfter`
  4. If the certificate authority, certificate and private key are not already embedded in the `.yaml` data, then the content of each of these is used to replace the paths to the respective files under `pki` in `ca`, `crt`, and `key` for transfer to the front end.
  5. The `.yaml` file is loaded and sent to the frontend for parsing.
  
- If a `.yaml` file exists for the connection, then this is loaded and sent to the frontend for processing.
- The passed YAML content is processed on the front end as follows:
  1. Frontend JS writes the `.yaml` file into `#modalEditConfigFileText` in case the user wants to edit it manually.
  2. The `.yaml` file is parsed into JSON (prefer `eemeli/yaml`) and the content is populated into the GUI.
  3. Whenever content is altered, it is pulled into the JSON automatically and the YAML in the hidden textarea is updated.
  4. If the `.yaml` file in `#modalEditConfigFileText` is edited (through a bootstrap modal in the HTML), saving the modal will send the YAML content to the backend for a quick validity check, then, if no error is detected, re-parses the .yaml and work the changes into the various fields in the GUI.
  5. When saving the configuration, the YAML in `#modalEditConfigFileText` is passed to the backend, validated, and saved.

- Content from the YAML in `nebula_settings` is loaded into the GUI as follows:
  - `pki`
    - The embedded certificate authority under `ca` is checked for validity (does it start with `-----BEGIN NEBULA CERTIFICATE`?). If it is valid, `#settings-connection-root-cert-valid` is set to `display: inline-block` and `#settings-connection-root-cert-invalid` is set to `display: none`. If it is invalid, the two spans' `display` CSS attributes are reversed.
    - The same procedure is repeated for the private certificate in `cert` for the spans `#settings-connection-private-cert-valid` and `#settings-connection-private-cert-invalid`.
    - The privat key in `key` is checked for validity (does it start with `-----BEGIN NEBULA X25519 PRIVATE KEY`?). Upon determination of validity the spans `#settings-connection-private-key-valid` and `#settings-connection-private-key-invalid` have their CSS `display` attributes set accordingly (see above).
    - If the edit button beside a given certificate is clicked, it is loaded from the JSON object in memory into the `#certificateTextArea` of the `#editCertificateModal` before opening the modal. (See below for how the modal works.)

  - `static_host_map`
    - Each entry in the list is written to a row in `#nodeStaticHostsTable`.
    - Whether or not a static host is a lighthouse is determined whether it is found in the list at `lighthouse.hosts`

  - `firewall`
    - `outbound_action` and `inbound_action` are translated to the dropdowns `#nodeOutboundConnectionAction` and `#nodeInboundConnectionAction` respectively. Each row is given a `data-row-id` attribute that is incremented from the previous one. The row ids are specific to the table (i.e. each table can have a row 1 or 2, etc.).
    - Firewall rules under `outbound` are translated to `#nodeOutboundConnectionTable`. Each row is given a `data-row-id` attribute that is incremented from the previous one.

- Clicking the `#connectionEditConfigFile` button will pop up the modal that allows for the manual editing of the Nebula configuration file.
  - Once the `#modalConfigFileSave` button is clicked, then the content of the `#modalEditConfigFileText` textarea is sent to the backend for validation.
  - If the content is valid, the new YAML is parsed, worked into the global JSON and the GUI content is reworked accordingly (see above).

- The connection is not saved until the `#btnSaveConnection` button is clicked. Then the content is sent to the backend for processing via the `pywebview` JavaScript bridge (`src\gui\web\js\settingsBackend.js`) as follows:
  - The fields populated by `window.settings_content.pulsar_settings` are read (see above) and compiled into a new YAML string and placed in the `pulsar_settings` object of the `window.settings_content` JSON object.
  - The YAML in `#modalEditConfigFileText` textarea is placed in the `nebula_settings` object of the `window.settings_content` JSON object.
  - The `window.settings_content` JSON object is passed to the backend.
  - The JSON is  received from the frontend and the YAML is extracted. The YAML is checked using `yaml.safe_load`. If it does not pass, an error is sent to the front end.
  - If the content is valid, 
    - `nebula_settings` are written to `instance/connection[x].yaml` where the `x` is the letter associated with the connection. If there is only one connection `x` is equal to `A`.
    - `pulsar_settings` are parsed and written to the global `SETTINGS` object and from there saved to the permanent `settings.yaml` file.
  - A success message is passed back to the GUI.

#### 2.3.4 About and Logs

- The About and Logs page is provided in `src/gui/web/info-logs.html`.
- The JavaScript driving this page is located in `src/gui/web/js/aboutLogs.js`.
- Upon opening the page the Build Information section is updated as follows:
  - The `pywebview` bridge provides the data for the Build Information section from the back end.
    
    ```json
    {
      'pulsar_version': 'String from __version__ variable of the pulsar.py file',
      'pulsar_build': 'String from the __build__ variable of the pulsar.py file',
      'pulsar_devs': 'comma separated list of names made from the __credits__ list of the pulsar.py file',
      'python_version': 'sys.version_info output as str',
      'nebula_version': 'Nebula version pulled from NebulaControl.nebula.version'
    }
    ```

  - `pulsar_version` is written to `#aboutBuildVersion`.
  - `pulsar_build` is written to `#aboutBuildNumber`.
  - `pulsar_devs` is written to `#aboutBuildDevs`.
  - `python_version` is written to `#aboutBuildPythonVersion`.
  - `nebula_version` is written to `#aboutBuildNebula`.

- The Connection Log section is handled as follows:
  - The connection information is passed from the backend as a JSON that is converted from the YAML in the `SETTINGS` global object
  - Only the connections that are enabled are displayed using `display: inline-block`, whether they are connected or not. Those that are not enabled are hidden using `display: none`. The DIV containing the log display is identified by `#logConnectionX` where `X` is equal to the letter defining the connection (A-E).
  - The log contents are read from the log files written to disk, which are reversed, with the newest log entries at the top. The reordering of the log file is handled at the backend.
  - If the `#switchLogRefreshConnectionX` switch is `checked`, then the frontend queries the backend every 30 seconds to receive the updated log file for that connection. 
  - The timed query function needs to be smart enough to stagger the calls to the backend so that they are spaced at least a half-second apart, preventing bottlenecking.
  - Clicking the associated `.btn-log-refresh` will trigger the refresh immediately and reset the 30-second timer if the `#switchLogRefreshConnectionX` switch is `checked`. It *will not* set the `#switchLogRefreshConnectionX` switch to `checked` if it is not checked.
  - If the `#switchLogRefreshConnectionX` switch is not `checked`, then the log file is only loaded when the page is first loaded and is not updated unless either the `#switchLogRefreshConnectionX` switch is set to `checked` or the associated `.btn-log-refresh` is clicked.

### 2.4 Multilingual Features and Localization

### 2.5 Startup Sequence

### 2.6 Shutdown Sequence

## 3. Nebula Integration

NebulaControl class

### 3.1 Nebula Binaries

### 3.2 Starting and Stopping Nebula

### 3.3 Nebula Configuration Files

### 3.4 Editing Nebula Configurations through the GUI

## 4. Infrastructure

### 4.1 Required Python Packages

### 4.2 Directory Structure

### 4.3 Coding Conventions

### 4.4 Sample Files

#### 4.4.1 settings.yaml

```yaml
settings_version: 2.0         # from __version__ variable
language: en                  # from locale.languageToCode(locale.language())
display_mode: system
exit_on_window_close: false
tray_start: true
start_on_login: true
multiple_connections: false
ping_interval: 300            # in seconds
timestamp: ''                 # regenerated on each save of settings
nebula_path: system path      # or direct path to document
connections:
  A:
    enabled: true
    name: ''
    auto_connect: false
    keep_alive: true
    disable_ping: false
    nebula_config: instance/connectionA.yaml
    private_ip: ''
    cert_expiration: ''
    resolve_hosts: true
    hosts_list:              # this creates the host url-to-ip resolution to be inserted into the hosts file
      - host_name: ''
        host_ip: ''
    log_level: info
    nebula_log: instance/connectionA.log
  # continue with B, C, D, and E
```

#### 4.4.2 en.json
