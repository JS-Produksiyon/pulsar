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
|   1. | Redesign icons for system tray               |     ✓      |
|   2. | Design various interfaces 3-6                |            |
|   3. | Implement **main GUI** interface             |            |
|   4. | Implement **settings** interface             |            |
|   5. | Implement **profiles** interface             |            |
|   6. | Implement **first run** interface            |            |
|   7. | Implement system tray icon                   |            |
|   8. | Implement Nebula back-end check              |            |
|   9. | Create check for valid Nebula `.yaml` files  |            |
|  10. | Create backend for each interface            |            |


## Descriptions

### Base requirements

* pybabel for multilingual capabilities
* pywebview.api for backend connectivity
* JQuery for object manipulation
* Bootstrap for design and layout
* FontAwesome SVG+JavaScript for icons -> though this needs to be tested for speed
* jinja2 + pybabel for base page rendering
* ui/js/gui.js for interactions 


### Nebula settings in Profile management interface

* pki
    - pki.ca -> file or filled-in field
    - pki.cert -> file
    - pki.key -> file
    - pki.blocklist -> table of individual fields that can be added 
    - pki.disconnect_invalid -> checkbox

* static_host_map -> table of field pairs that can be added to

* static_map -> on same screen as static_host_map
    - network -> dropdown with *ip4*, *ip6*, or *ip4 and ip6*
    - cadence -> number input
    - lookup_timeout -> number input

* lighthouse
    - Do not expose: am_lighthouse, serve_dns, dns and subkeys, calculated_remotes
    - interval -> number input
    - hosts -> table of fields that can be added to
    - remote_allow_list, local_allow_list, advertised_addrs -> go under advanced and are textarea boxes that are filled in.

* ~~listen~~ -> not needed for clients

* punchy
    - punch -> checkbox
    - delay -> number input
    - respond -> checkbox
    - respond_delay number input

* cipher -> on advanced page; dropdown with `default`, `aes`, or `chachapoly`

* preferred_ranges -> on general page; table of individual fields that can be added

* relay -> on lighthouse page
    - relays -> table where rows can be added with dropdown of lighthouse IPs
    - ~~am_relay~~ -> cannot be set; must be false
    - use_relays -> checkbox

* ~~tun~~ -> managed by Pulsar

* ~~sshd~~ -> not needed by Pulsar

* logging -> on general page
    - level -> dropdown with levels
    - format -> Pulsar defaults to json

* firewall
    - outbound -> table where rows can be added with these fields via modal:
        + port -> text field that is either numerical or range
        + proto -> dropdown = `any`, `tcp`, `udp`, `icmp`
        + host -> text field with button that makes it `any`
        + group/groups -> table with text fields where groups can be added and a button to set to `any`
        + Under Advanced:
            + cidr -> text field
            + local_cidr -> text field
            + ca_name -> text field
            + ca_sha -> text field
        
    - inbound -> same as above

    - ~~default_local_cidr_any~~ -> not necessary

    - conntrack
        + tcp_timeout -> number input
        + udp_timeout -> number input
        + default_timeout -> number input
    
    - ~~outbound_action~~, ~~inbound_action~~ -> not needed

* ~~routines~~ -> not needed by Pulsar

* ~~stats~~ -> not needed by Pulsar

* handshakes -> under lighthouse page
    - try_intervals -> number input
    - retries -> number input
    - trigger_buffer -> number input

* local_range/preferred_ranges -> under advanced page -> table with rows that can be added with text input

| Tab         | Items |
| ----------- | ----- |
| General     | Enable/disable profile, import profile from file, auto connect, keep alive, logging
| Credentials | pki
| Networking  | static_host_map, static_map, lighthouse, punchy, handshakes
| Firewall    | firewall
| Advanced    | cipher, preferred_range, local_range/preferred_ranges, 


---
Last Updated: 2025-05-23
