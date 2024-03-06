# dials-py

The Python api client interface to DIALS service.

## Installation

To install dials-py, simply

```bash
$ pip install cmsdials
```

## Usage

Before interfacing with any route you need to generate valid credentials, it is possible to authenticate trough the `device authorization flow` or using the `client secret key` of any application registered in DIALS. Note that, the device flow is an interactively authentication procedure that is possible to distinguish users in DIALS backend and the client secret flow is not interactive and is not possible to distinguish users so it should only be used for automation scripts.

### Generating credentials with client secret

```python
from cmsdials.auth.secret_key import Credentials

creds = Credentials(token=".....")
```

### Generating credentials with device

#### Loading from AuthClient

```python
from cmsdials.auth.client import AuthClient
from cmsdials.auth.bearer import Credentials

auth = AuthClient()
token = auth.device_auth_flow()
creds = Credentials.from_authclient_token(token)
```

#### Loading from cached credentials file

Credentials are always cached once you authenticate at least on time, calling this method without having a cached credential file will automatically trigger the AuthClient device flow.

```python
from cmsdials.auth.bearer import Credentials

creds = Credentials.from_creds_file()
```

### Baisc Example

```python
from cmsdials.auth.bearer import Credentials
from cmsdials import Dials
from cmsdials.filters import LumisectionHistogram1DFilters

creds = Credentials.from_creds_file()
dials = Dials(creds, nthreads=2)

# Getting h1d data
data = dials.h1d.list_all(LumisectionHistogram1DFilters(title="PixelPhase1/Tracks/PXBarrel/charge_PXLayer_2"))
```
