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

Credentials are always cached once you authenticate at least one time, calling this method without having a cached credential file will automatically trigger the AuthClient device flow.

```python
from cmsdials.auth.bearer import Credentials

creds = Credentials.from_creds_file()
```

### Basic Example

```python
from cmsdials.auth.bearer import Credentials
from cmsdials import Dials
from cmsdials.filters import LumisectionHistogram1DFilters

creds = Credentials.from_creds_file()
dials = Dials(creds, nthreads=2)

# Getting h1d data
data = dials.h1d.list_all(LumisectionHistogram1DFilters(title="PixelPhase1/Tracks/PXBarrel/charge_PXLayer_2"))
```

## Available endpoints

This package interacts with DIALS api endpoints using underlying classes in `Dials` object.

### Retrieving a specific object using `get`

```python
dials.bad_file_index.get(id=1)
dials.file_index.get(id=1)
dials.h1d.get(id=1)
dials.h2d.get(id=1)
dials.lumi.get(id=1)
dials.run.get(id=1)
```

### Retrieving a list of objects per page using `list`

It is possible to get a list of entries from those endpoint using the `list` and `list_all` methods, the `list` method will fetch only one page and the `list_all` will fetch all available pages:

```python
dials.bad_file_index.list()
dials.file_index.list()
dials.h1d.list()
dials.h2d.list()
dials.lumi.list()
dials.run.list()
```

### Retrieving all available pages of a list of objects using `list_all`

```python
dials.bad_file_index.list_all()
dials.file_index.list_all()
dials.h1d.list_all()
dials.h2d.list_all()
dials.lumi.list_all()
dials.run.list_all()
```

If you don't need all available pages but just a subset of then, it is possible to specify a `max_pages` integer parameter:

```python
dials.run.list_all(..., max_pages=5)
```

### Using filters

Keep in mind that calling those methods without any filter can take a lot of time, because the underlying query will try to load the entire database table through multiple requests, then it is recommended to apply filters according to DIALS [live documentation](https://cmsdials-api.web.cern.ch/api/v1/swagger#/) using filter classes for each table:

```python
from cmsdials.filters import (
    BadFileIndexFilters,
    FileIndexFilters,
    LumisectionHistogram1DFilters,
    LumisectionHistogram2DFilters,
    LumisectionFilters,
    RunFilters
)

dials.bad_file_index.list(BadFileIndexFilters(path_contains="ZeroBias"))

dials.file_index.list(FileIndexFilters(page="10"))

dials.h1d.list(LumisectionHistogram1DFilters(title="PixelPhase1/Tracks/PXBarrel/charge_PXLayer_2", page="15"))

dials.h2d.list_all(LumisectionHistogram2DFilters(title_contains="EEOT digi occupancy EE +", min_entries=100, min_run_number=360392, max_run_number=365000))

dials.lumi.list_all(LumisectionFilters(run_number=360392))

dials.run.list_all(RunFilters(min_run_number=360392, max_run_number=365000))
```

### Dials MEs

It is possible to inspect the list of selected MEs considered in DIALS during ETL requesting the endpoint `configured-mes` trough the method:

```python
dials.lumi.configured_mes()
```

## Usage with local DIALS

All classes that interface the DIALS service inherits the class `BaseAPIClient` which propagate the `base_url`, `route` and `version` attributes with production values. In order to use dials-py with a local version of DIALS it is possible to overwrite those attributes when instantiating the `AuthClient` and the `Dials` client, for example:

```python
from cmsdials.auth.client import AuthClient
from cmsdials.auth.bearer import Credentials
from cmsdials import Dials
from cmsdials.filters import LumisectionHistogram2DFilters

DEV_URL = "http://localhost:8000/"
DEV_CACHE_DIR = ".cache-dev

auth = AuthClient(base_url=DEV_URL)
creds = Credentials.from_creds_file(cache_dir=DEV_CACHE_DIR, client=auth)  # Make sure to specify the auth client with overwritten values, using another cache_dir is recommended
dials = Dials(creds, nthreads=2, base_url=DEV_URL)

dials.h2d.list_all(LumisectionHistogram2DFilters(title_contains="EEOT digi occupancy EE +", min_entries=100, min_run_number=360392, max_run_number=365000))
```
