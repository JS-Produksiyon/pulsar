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
- The icons are found in the `/src/gui/img` folder relative to the project root. `pulsar-icon-black-64.png` and `pulsar-icon-white-64.png` will be preferred for the offline states and `pulsar-icon-64.png` will be preferred for the connected state.
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
- The icons for the GUI are found in `/src/gui/img` and are available as .png (cross-platform), .icns (Mac), and .ico (Windows).

### 2.1 Light and Dark Mode

- The application will render in both a dark mode and a light mode interface.
- The program will provide a snippet of code that will determine the current setting of the OS to render the interface in the correct mode.
- If the OS color mode cannot be determined, the program will default to dark mode (e.g. for Linux).
- The interface will initially follow the system preference.
- The interface can be set to the user's preference for light mode or dark mode on the Settings page. This value is stored in the `instance/settings.yaml` file (see [2.3.1 Settings](#231-settings)).

### 2.2 Primary GUI Window

- The design for the primary GUI Window is already completed using HTML/CSS/JS. All necessary files are located in `/src/gui/web`.
- The primary GUI window size is to be 520px x 520px, is frameless (i.e. does not have the system-based title and border), and is not resizable. It needs to be able to handle the dynamic resolution-based resizing that Windows provides (e.g. 100% enlargement on FullHD and 200% enlargement on 4k).
- Upon opening, the window appears centered on the user's main monitor.
- Clicking and dragging the `#drag-bar` DIV will move the window around the screen. This needs to be handled with a combination of frontend JavaScript and backend `pywebview` functionality. The code for this is in `/src/gui/web/js/windowDrag.js`.
- The buttons at the top of the GUI function as follows:

| Button ID    | Action                                                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| btnReconnect | Executes a disconnect, waits a second, executes connect.                                                                           |
| btnSettings  | Opens the secondary GUI window containing the Settings page. (Replaces the About page, if open)                                    |
| btnAbout     | Opens the secondary GUI window containing the About page. (Replaces the Settings page, if open)                                    |
| btnHelp      | Opens the help wiki on the public repository page in a separate web browser                                                        |
| btnClose     | Closes the connection window. If `#switchCloseOnWindow` is checked, it closes down all connections and the tray  application, too. |

- The button clicks are executed using pywebview's JavaScript bridge. These are to be exposed in `/src/gui/web/js/mainWindowBackend.js`. 
- If there is only a single connection defined (multiple connections are disabled in settings.yaml), then the GUI shows the `#pulsar-single-connection` layer. On clicking the connect button the following animation starts. JavaScript for frontend portion of connection animation is found in `/src/gui/web/js/connectAnimation.js`.
  - The bottom line animates across at which point the connection begins. The Connect button becomes the Cancel button. This is where the privilege elevation UI should be triggered.
  - Read the output to see if the connection is established and do a ping of the lighthouses.
  - If the ping comes back, color the Nebula icon and animate the top bar back over to the Pulsar icon. The Cancel Button becomes the Disconnect button.
- If there are multiple connections defined then the GUI shows the `#pulsar-multi-connection` layer. Only the connections that are set to active in `settings.yaml` will be displayed in the list (e.g. if there are three connections defined as active, only those three connections are displayed). On connection the animation works as following:
  - The associated `#connect-status-[id]` block's class is set from `disconnected` to `connecting`. The associated `#connect-connect-[id]` button is  replaced with the `#connect-cancel-[id]` button.
  - Once the connection has been checked to be established the associated `#connect-status-[id]` block's class is set from `connecting` to `connected`and the associated `#connect-cancel-[id]` button is  replaced with the `#connect-disconnect-[id]` button. 

  - When the disconnect command is given (either by clicking the Cancel button, Disconnect button or through the Reconnect button), the associated `#connect-status-[id]` block's class is set from whatever it is to `disconnected`and the button is replaced by the `#connect-connect-[id]` button.

- Upon startup the existence of a Nebula instance is checked for. If it cannot be found in the system path, then a native dialog explaining the missing Nebula instance pops up. Clicking OK on the dialog will open the Settings window (see [2.3 Secondary GUI Window](#23-secondary-gui-window)) and scrolls down to the Nebula Binaries (`settings.html#settingGeneralSettingsNebula`) on the Settings page (see [2.3.1 Settings](#231-settings)).
- Upon startup the existence of configured connections is checked (see 2.5 Startup Sequence). If there is no connection configured, then a native dialog is popped up, warning that the connection must be configured. Clicking OK on the dialog will open the Settings window (see [2.3 Secondary GUI Window](#23-secondary-gui-window)) and navigate to the Connections screen (see [2.3.2 Connections](#232-connections)). The Connect button(s) will be disabled until the connection is properly configured.
- If the Close button is clicked while the application is set to shut down when the main GUI window is closed and there are still connections active, a native system dialog is triggered through the pywebview backend warning the user of the connection status and whether they want to close the application, as it will disconnect all of the Nebula connections. The application will only close upon confirmation.

### 2.3 Secondary GUI Window

- The design for the secondary GUI Window is already completed using HTML/CSS/JS. All necessary files are located in `/src/gui/web`.
- The secondary GUI window size is to be 80% of the monitor it appears on. This needs to be calculated when the window is first created. It needs to be able to handle the dynamic resolution-based resizing that Windows provides (e.g. 100% enlargement on FullHD and 200% enlargement on 4k).
- The secondary GUI window is frameless (i.e. does not have the system-based title and border). 
- Upon opening, the window appears centered on the user's main monitor.
- The secondary GUI window is resizable, though this is handled by clicking and dragging the `#resize-handle` DIV. The resizing functionality needs to be handled with a combination of frontend JavaScript and backend `pywebview` functionality. The code for this is in `/src/gui/web/js/windowResize.js`.
- Clicking and dragging the `#drag-bar` DIV will move the window around the screen. This needs to be handled with a combination of frontend JavaScript and backend `pywebview` functionality. The code for this is in `/src/gui/web/js/windowDrag.js`.
- The buttons in the upper right corner function as follows:

| Button ID      | Action                                                                                    |
| -------------- | ----------------------------------------------------------------------------------------- |
| btnWinMinimize | Minimizes the window to the taskbar.                                                      |
| btnWinMaximize | Maximizes the window to fill the whole screen. Is replaced by btnWinRestore when clicked. |
| btnWinRestore  | Restores the window to its previous size. Is replaced by btnWinMaximize when clicked.     |
| btnWinClose    | Closes the window.                                                                        |

- 

#### 2.3.1 Settings

#### 2.3.2 Connections

#### 2.3.3 About and Logs

### 2.4 Multilingual Features and Localization

### 2.5 Startup Sequence

### 2.6 Shutdown Sequence

## 3. Nebula Integration

### 3.1 Nebula Binaries

### 3.2 Starting and Stopping Nebula

### 3.3 Nebula Configuration Files

### 3.4 Editing Nebula Configurations through the GUI

## 4. Infrastructure

### 4.1 Required Python Packages

### 4.2 Directory Structure

### 4.3 Coding Conventions
