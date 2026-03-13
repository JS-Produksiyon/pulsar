# Notes for Pulsar v.2.0

## List of settings

### General Settings

* Interface
  * Display mode → light, dark, system
  * Interface Language
* Startup behavionr
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

### Examples

This is how the produced config.yaml files need to have the ca, cert, and key set up under `pki`. That way we can keep everything in a single file for easier storage and access.

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

---
Updated: 2026-03-13
