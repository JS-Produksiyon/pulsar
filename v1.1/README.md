# Pulsar v.1.1

## Required New Features
1. Remove QT6 requirement for GUI; use pywebview for GUI and pysystray for for the notification icon

2. Do not include nebula executables; first search for nebula in path; if not there prompt user to point to the nebula executable

3. Allow for up to 5 separate nebula connections

4. Handle all nebula connections directly.
    
    - Allow for import of a nebula config.yaml file
    - Allow for import of a zipped nebula configuration
    - Create interface to make nebula config.yaml file interactively
    - Make it possible to have a separate hosts setup for each file

> These will be kept track of using the GitHub issues.


## Optional new features

* Privilege elevation should only be triggered when nebula attempts to connect *unless* autostart is enabled, then the application itself should auto-elevate.

* Hide the console window and integrate into the interface.


## Process

| Step | Description                                  | Complete   |
| ---: | -------------------------------------------- | :--------: |
|   1. | Redesign icons for system tray               |            |
|   2. | Design various interfaces 3-6                |            |
|   2. | Implement **main GUI** interface             |            |
|   3. | Implement **settings** interface             |            |
|   4. | Implement **profiles** interface             |            |
|   5. | Implement **first run** interface            |            |
|   6. | Implement system tray icon                   |            |
|   7. | Implement Nebula back-end check              |            |
|   8. | Create check for valid Nebula `.yaml` files  |            |
|   9. | Create backend for each interface            |            |


## Descriptions

### Base requirements

* pybabel for multilingual capabilities
* pywebview.api for backend connectivity
* JQuery for object manipulation
* Bootstrap for design and layout
* FontAwesome SVG+JavaScript for icons -> though this needs to be tested for speed
* jinja2 + pybabel for base page rendering
* ui/js/gui.js for interactions 


---
Last Updated: 2025-05-19
