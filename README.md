# Pulsar
A Python-based GUI frontend for the [Nebula mesh network](https://github.com/slackhq/nebula) CLI client for Windows and MacOS.

Pulsar is developed and maintained by JS Prodüksiyon Ltd. Şti. and is presented under the GNU GPL v3.0.

This document is also available in [German (Deutsch)](README_de.md) and [Turkish (Türkçe)](README_tr.md)

This document was last updated on 2024-05-08.


## Nebula Version
Nebula client binary version 1.8.2

## Installation
### Binary Releases
~~You can find binary releases for Pulsar that work on Windows and MacOS by visiting the [Releases](releases/) page.~~ _Not yet; still testing._

Download the latest release, unzip the file in a location of your choosing and run the enclosed executable. Pulsar does not need to be installed to be used.

You can manually add a shortcut link to Pulsar to the Start menu in Windows or the Launcher in MacOS

### Source
Pulsar requires Python 3.11 to run.

You can clone the source code of Pulsar to your machine by opening a CLI (PowerShell in Windows or Terminal on MacOS) using the `git clone https://github.com/JS-Produksiyon/pulsar.git` command. Once cloned, create a virtual environment: `python3.11 -m venv venv`

Activate the virtual environment in Windows with `venv\Scripts\Activate.ps1` or use `source venv/bin/activate` on MacOS.

Install the required packages using `pip install -r requirements.txt`

Once the requirements are installed, run the program with the command `python src/pulsar.py`


## Usage
Due to the fact that the Nebula CLI client requires superuser access, Pulsar will automatically attempt to elevate its privileges, either with an UAC prompt on Windows or requesting your password on MacOS.

On first run, Pulsar will require you to select the necessary Nebula `.yaml` config file. Once you have selected this, click Save Settings and you should be able to immediately connect to the Nebula network by clicking the big green button.

Closing the Pulsar window will not end the program. You must do this by either clicking the _Quit Pulsar_ button or by right-clicking the Pulsar icon System Tray (Windows) or by clicking on the Pulsar icon in the Menu Bar (MacOS) and selecting Quit. 


## Why “Pulsar”?
The Nebula mesh network tool is named after the heavenly luminous gases that contain many stars. A mesh network is rather amorphous and contains many nodes as well. 
This application makes it possible for one node to connect to the network, much like one star exists in the nebula. And because it puts out a pulse to connect,
the image of the pulsar, a magnetized neutron star that pulses at a certain frequency, seemed an apt image. Thus you use Pulsar to connect to the Nebula. Enjoy!



