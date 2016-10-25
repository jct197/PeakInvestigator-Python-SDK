# PeakInvestigator-Python-SDK
A Python library for interacting with the PeakInvestigator™ public API

## Using the library

The general use is to create an instance of PeakInvestigatorSaaS, as well as instances of various "Actions" 
corresponding to the desired API calls to PeakInvestigator (see https://peakinvestigator.veritomyx.com/api 
for complete list), and call ```execute()``` with the desired action. For example, making a call to the 
PI_VERSIONS API can be accomplished with the following code:

```
from peakinvestigator import PeakInvestigatorSaaS
from peakinvestigator.actions import *

service = PeakInvestigatorSaaS() # uses https://peakinvestigator.veritomyx.com by default
action = PiVersionsAction("4.2", "joe", "abc123")
response = service.execute(action)
action.process_response(response)

print("Current version:", action.current_version)
...
```

## Dependencies

The following dependencies are required, and should be available from PyPi.

* ```requests```   — for the actual POST calls to the API
* ```simplejson``` — for parsing the JSON response from server
* ```paramiko```   — for SFTP transfers

## Example script

There is also a basic command-line implementation (```scripts/peakinvestigator```) that can be used 
for simple job submission and retrieval. As of late October 2016, it can only be used for single scan
data in tab-delimited format. It requires the USERNAME, PASSWORD, and PROJECT to be specified via 
environmental variables.
