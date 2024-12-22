""" Exaroton Class to interface with the API """

import requests
from typing import List

from . import types


class Exaroton:
    """Exaroton Class for the API"""

    def __init__(self, token: str, host: str = "https://api.exaroton.com/v1") -> None:
        """
        Exaroton Class to interface with the API

        Parameters:
            ``token`` (``str``):
                The Authentication Token from the [user page](https://exaroton.com/account/)

            ``host`` (``str``, optional):
                The API Host. Defaults to "https://api.exaroton.com/v1".
        """
        self._host = host
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {token}"})

    def _make_request(self, path: str, method: str = "get", **kwargs):
        """Make HTTP Requests against the API

        Parameters:
            ``path`` (``str``): The API calls' path for the request.
            ``method`` (``str``, optional): HTTP Method (GET, POST, PUT, etc). Defaults to GET.
            ``**kwargs``: Additional arguments passed to the API call.

        Returns:
            JSON serialized data
        """
        req = self._session.request(method, f"{self._host}/{path}", **kwargs)
        # TODO Error Handling
        content_type = req.headers["content-type"]

        if content_type == "application/json":
            return req.json()

        elif content_type == "text/plain;charset=UTF-8":
            return bytes.decode(req.content, "utf8")

        elif content_type == "application/octet-stream":
            return req.content

        elif content_type == "image/png":
            # In case returned data is an image (for example the server-icon.png)
            # This type isn't actually documentated by the API Docs :thumbsup:
            return req.content

    def get_account(self) -> types.Account:
        """Get information about the authenticated Account

        Returns:
            ``types.Account``: Your Account
        """
        _data = self._make_request("account")["data"]
        return types.Account(**_data)

    def get_servers(self) -> List[types.Server]:
        """Get a list of servers on your account

        Returns:
            ``types.List``: List of ``types.Server`` objects
        """
        _data = self._make_request("servers")["data"]
        return types.List(types.Server(**data) for data in _data)

    def get_server(self, id: str) -> types.Server:
        """Get a specific Server on your account

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``types.Server``: The Server
        """
        _data = self._make_request(f"servers/{id}")["data"]
        return types.Server(**_data)

    def get_server_logs(self, id: str) -> str:
        """Retrieve logs of the specified server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``str``: The current log file in its entirety.
        """
        _data = self._make_request(f"servers/{id}/logs")["data"]["content"]
        return _data

    def upload_logs(self, id: str) -> types.Logs:
        """Upload logs to https://mclo.gs

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``types.Logs``: Identifier and URLS to the uploaded log
        """
        _data = self._make_request(f"servers/{id}/logs/share")["data"]
        return types.Logs(**_data)

    def get_server_ram(self, id: str) -> int:
        """Get the RAM of a Server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``int``: Currently set RAM in Gigabytes
        """
        _data = self._make_request(f"servers/{id}/options/ram")["data"]["ram"]
        return _data

    def set_server_ram(self, id: str, ram: int) -> int:
        """Set a new amount of RAM to be used by the specified server

        Args:
            ``id`` (``str``): The ID of the server
            ``ram`` (``int``): RAM in Gigabyte

        Returns:
            ``int``: Newly set RAM in Gigabytes
        """
        _data = self._make_request(
            f"servers/{id}/options/ram", "post", json={"ram": ram}
        )["data"]["ram"]
        return _data

    def start(self, id: str) -> str:
        """Start the Server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``str``: "Hello, world!"
        """
        _data = self._make_request(f"servers/{id}/start", "post")
        return _data

    def stop(self, id: str) -> str:
        """Stop the Server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``str``: "Hello, world!"
        """
        _data = self._make_request(f"servers/{id}/stop",  "post")
        return _data

    def restart(self, id: str) -> str:
        """Restart the Server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``str``: "Hello, world!"
        """
        _data = self._make_request(f"servers/{id}/restart", "post")
        return _data

    def command(self, id: str, command: str) -> str:
        """Send a Command to the Server

        Args:
            ``id`` (``str``): The ID of the server
            ``command`` (``str``): The command (`say Hello World`)

        Returns:
            ``str``: "Hello, world!"
        """
        _data = self._make_request(
            f"servers/{id}/command", "post", json={"command": command}
        )["data"]
        return _data

    def get_player_lists(self, id: str) -> List[str]:
        """Get a list of available playerlists

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``list``: The List of available playerlists (whitelist, ops, etc.)
        """
        _data = self._make_request(f"servers/{id}/playerlists")["data"]
        return _data

    def get_player_list(self, id: str, player_list: str) -> List[str]:
        """Get a specific playerlist

        Args:
            ``id`` (``str``): The ID of the server
            ``player_list`` (``str``): The playerlist to retrieve

        Returns:
            ``list``: List of players on that list
        """
        _data = self._make_request(f"servers/{id}/playerlists/{player_list}")["data"]
        return _data

    def add_player_to_list(self, id: str, player_list: str, usernames: list) -> List[str]:
        """Add playernames to a playerlist

        Args:
            id (``str``): The ID of the server
            player_list (``str``): The name of the playerlist (eg "whitelist")
            usernames (``list`` | ``str``): The username or multiple thereof to add

        Returns:
            ``list``: The new list of players on that list
        """
        _data = self._make_request(
            f"servers/{id}/playerlists/{player_list}",
            "put",
            json={"entries": usernames},
        )["data"]
        return _data

    def remove_player_from_list(self, id: str, player_list: str, usernames: List[str]):
        """Remove players from a playerlist

        Args:
            ``id`` (``str``): The ID of the server
            ``player_list`` (``str``): The name of the playerlist (eg "whitelist")
            ``usernames`` (``list`` | ``str``): The username of multiple thereof to remove

        Returns:
            ``list``: The new list of players on that list
        """
        _data = self._make_request(
            f"servers/{id}/playerlists/{player_list}",
            "delete",
            json={"entries": usernames},
        )["data"]
        return _data

    def get_file_data(self, id: str, path: str):
        """Retrieve file data based on a given path.

        Args:
            ``id`` (``str``): The ID of the server
            ``path`` (``str``): The path to retrieve
        """
        _data = self._make_request(f"servers/{id}/files/data/{path}")
        return _data

    def write_file_data(self, id: str = None, path: str = None, data=None):
        """Write content to a file. If it doesn't exist yet, it'll be created."""
        # TODO implement
        raise NotImplementedError("This method hasn't been implemented yet")
        # _data = self._make_request(f"servers/{id}/files/data/{path}", "put")

    def delete_file_data(self, id: str, path: str):
        _data = self._make_request(f"servers/{id}/files/data/{path}", "delete")
        return _data

    def get_credit_pools(self) -> List[types.CreditPool]:
        """Get the list of credit pools that the account is a member of

        Returns:
            ``types.List``: List of ``types.CreditPool`` objects
        """
        _data = self._make_request("billing/pools")["data"]
        return types.List(types.CreditPool(**data) for data in _data)
    
    def get_credit_pool(self, id: str) -> types.CreditPool:
        """Get a specific credit pool

        Args:
            ``id`` (``str``): The ID of the credit pool

        Returns:
            ``types.CreditPool``: The credit pool
        """
        _data = self._make_request(f"billing/pools/{id}")["data"]
        return types.CreditPool(**_data)

    def get_credit_pool_members(self, id: str) -> List[types.CreditPoolMember]:
        """Get members of a specified credit pool

        Args:
            ``id`` (``str``): The ID of the credit pool

        Returns:
            ``types.List``: A list of CreditPoolMember
        """
        _data = self._make_request(f"billing/pools/{id}/members")["data"]
        return types.List(types.CreditPoolMember(**data) for data in _data)

    def get_credit_pool_servers(self, id: str) -> List[types.Server]:
        """Get servers of a specified credit pool

        Args:
            ``int``: (``str``): The ID of the credit pool

        Returns:
            ``types.list``: A list of types.Server
        """
        _data = self._make_request(f"billing/pools/{id}/servers")["data"]
        return types.List(types.Server(**data) for data in _data)
