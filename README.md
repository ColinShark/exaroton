# exaroton

A Python Wrapper for the [exaroton API](https://developers.exaroton.com/)

Simply get an API Token from [your Account](https://exaroton.com/account/) and you're good to go.

[![Python: 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-red)](https://gitlab.com/ColinShark/exaroton/-/blob/master/LICENSE)
<!-- [![Gitmoji: 💻🔥](https://img.shields.io/badge/Gitmoji-%F0%9F%92%BB%F0%9F%94%A5-yellow)](https://github.com/carloscuesta/gitmoji#readme) -->

## Installation

exaroton requires Python 3.7 or newer.

```sh
python3 -m pip install -U exaroton
```

A Virtual Environment is recommended to not mess with system installs.
This module has minimal requirements (`requests`), but you can never be safe enough.

```sh
python3 -m venv venv
source ./venv/bin/activate
pip install exaroton
```

## Example Usage

Currently all methods are (in my opinion) well documented and properly typehinted.
If you see something wrong, don't hestitate to [create an Issue](https://github.com/ColinShark/exaroton/issues/new).

I may create a full list of all available methods, or even utilize readthedocs.org

```python
# Import exaroton and set our token
>>> from exaroton import Exaroton
>>> exa = Exaroton("API_TOKEN")

# Get information about the authenticated account
>>> exa.get_account()
{
    "_": "Account",
    "name": "Username",
    "email": "email@example.org",
    "verified": true,
    "credits": 420.69
}

# Get a list of our servers
>>> exa.get_servers()
[
    {
        "_": "Server",
        "id": "7ZxuNK5RX879BFaH",  # Thanks, random.org!
        ...
    },
    {
        "_": "Server",
        "id": "Kf48Td5iVlr8Xu24",  # Thanks, random.org!
        ...
    }
]

# Upload logs to https://mclo.gs
>>> exa.upload_logs("7ZxuNK5RX879BFaH")
{
    "_": "Logs",
    "id": "N5FR4K2",  # Thanks, random.org!
    "url": "https://mclo.gs/N5FR4K2",
    "raw": "https://api.mclo.gs/1/raw/N5FR4K2"
}

# Print logs (this'll most likely spam your output lol)
>>> exa.get_server_logs("7ZxuNK5RX879BFaH")
'one extremely long string with lines seperated by the newline escape character \n'
# It'll print each line seperately when used with `print()`!
```

All you need to make calls to the API is the Authentication Token you can get
from your account page. If you make server-specific calls, you'll need that
servers ID, too.


## The boring stuff

Licensed under [MIT](https://github.com/ColinShark/exaroton/blob/master/LICENSE)