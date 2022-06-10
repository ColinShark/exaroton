""" Exaroton Class to interface with the API """

import requests

from . import types


class Exaroton:
    """ Exaroton Class for the API """
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
        return req.json()

    def get_account(self) -> types.Account:
        """Get information about the authenticated Account

        Returns:
            ``types.Account``: Your Account
        """
        _data = self._make_request("account")["data"]
        return types.Account(**_data)

    def get_servers(self) -> types.List:
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
        _data = self._make_request(f"servers/{id}/start")  # ["data"]
        return _data

    def stop(self, id: str) -> str:
        """Stop the Server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``str``: "Hello, world!"
        """
        _data = self._make_request(f"servers/{id}/stop")  # ["data"]
        return _data

    def restart(self, id: str) -> str:
        """Restart the Server

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``str``: "Hello, world!"
        """
        _data = self._make_request(f"servers/{id}/restart")  # ["data"]
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

    def get_player_lists(self, id: str) -> list:
        """Get a list of available playerlists

        Args:
            ``id`` (``str``): The ID of the server

        Returns:
            ``list``: The List of available playerlists (whitelist, ops, etc.)
        """
        _data = self._make_request(f"servers/{id}/playerlists")["data"]
        return _data

    def get_player_list(self, id: str, player_list: str) -> list:
        """Get a specific playerlist

        Args:
            ``id`` (``str``): The ID of the server
            ``player_list`` (``str``): The playerlist to retrieve

        Returns:
            ``list``: List of players on that list
        """
        _data = self._make_request(f"servers/{id}/playerlists/{player_list}")["data"]
        return _data

    def add_player_to_list(self, id: str, player_list: str, usernames: list) -> list:
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

    def remove_player_from_list(self, id: str, player_list: str, usernames: list):
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
