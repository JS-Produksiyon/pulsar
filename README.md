# Pulsar
A Python-based GUI frontend for the [Nebula mesh network](https://github.com/slackhq/nebula) CLI client for Windows and MacOS.


Read the Documentation in the Wiki

Pulsar is developed and maintained by JS Prodüksiyon Ltd. Şti. and is presented under the GNU GPL v3.0.

~~This document is also available in [German (Deutsch)](README_de.md) and [Turkish (Türkçe)](README_tr.md)~~ _Not yet_

This document was last updated on 2024-05-08.


## Nebula Version
Nebula client binary version 1.8.2

## Rationale for Pulsar
As nice as the Nebula mesh network is, it takes some technical know-how to implement. Many users are not technically savvy enough to handle the CLI commands necessary to run Nebula properly. As we have several such users in our organization, it behooved us to write a fairly simple GUI to allow the user to connect to the Nebula network. Setup takes a tiny bit of help by the IT department, but once it's running, it should be fairly easy to use. 


## Operating System Compatibility

| OS         | Source   | Binary    |
| ---------- | -------- | --------- |
| Windows 11 | Works    | Works     |
| Windows 10 | Untested | Testing   |
| MacOS 13.6 | Testing  | Not ready |

Technically speaking Pulsar should run on any OS that can handle Python 3.11 and the Nebula client. While we don't have the ability to test all platforms, looking at Python's and Nebula's system requirements, this application should run on the following operating systems:

* **Windows:** 11, 10, 8.1, 8, 7
* **macOS:** Sonoma 14, Ventura 13, Monterey 12, Big Sur 11, Catalina 10.14, HighSierra 10.13, Sierra 10.12, El Capitan 10.11

Since we don't need this application to run on Linux, we did not add that functionality. However, if you want to fork it and make it work there, be our Guest

## Installation
### Binary Releases
~~You can find binary releases for Pulsar that work on Windows and MacOS by visiting the [Releases](releases/) page.~~ _Not yet; still testing._

Download the latest release, unzip the file in a location of your choosing and run the enclosed executable. Pulsar does not need to be installed to be used.

You can manually add a shortcut link to Pulsar to the Start menu in Windows or the Launcher in MacOS

### Source
Pulsar requires Python 3.11 to run.

You can clone the source code of Pulsar to your machine by opening a CLI (PowerShell in Windows or Terminal on MacOS) using the `git clone https://github.com/JS-Produksiyon/pulsar.git` command. 

Once cloned, create a virtual environment: `python3.11 -m venv venv`

Activate the virtual environment in Windows with `venv\Scripts\Activate.ps1` or use `source venv/bin/activate` on MacOS.

Install the required packages using `pip install -r requirements.txt`

Once the requirements are installed, run the program with the command `python src/pulsar.py`




## Usage
Due to the fact that the Nebula CLI client requires superuser access, Pulsar will automatically attempt to elevate its privileges, either with an UAC prompt on Windows or requesting your password on MacOS.

On first run, Pulsar will require you to select the necessary Nebula `.yaml` config file. Once you have selected this, click Save Settings and you should be able to immediately connect to the Nebula network by clicking the big green button.

> The IT department will need to supply the Nebula CA file, and the user private key and certificate files along with the `.yaml` configuration file.

Closing the Pulsar window will not end the program. You must do this by either clicking the _Quit Pulsar_ button or by right-clicking the Pulsar icon System Tray (Windows) or by clicking on the Pulsar icon in the Menu Bar (MacOS) and selecting Quit. 

Additionally, Pulsar provides the option of adding entries to the local `hosts` file to allow for easy domain name based access to the various resources the user needs to access.

> These IP Address / Hostname pairs in `hosts` file format needs to be provided by the IT department.


## Why Is the App Called “Pulsar”?
The Nebula mesh network tool is named after the heavenly luminous gases that contain many stars. A mesh network is rather amorphous and contains many nodes as well. This application makes it possible for one node to connect to the network, much like one star exists in the nebula. And because it puts out a pulse to connect, the image of the pulsar, a magnetized neutron star that pulses at a certain frequency, seemed an apt image. Thus you use Pulsar to connect to the Nebula. Enjoy!



