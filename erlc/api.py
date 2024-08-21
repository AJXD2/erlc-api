from typing import TYPE_CHECKING
import erlc.models as models
import erlc.execptions as execptions

if TYPE_CHECKING:
    from erlc.client import ErlcServerClient


class ServerAPI:
    def __init__(self, client: "ErlcServerClient") -> None:
        self.client = client
        self.cache = {}
        self.get_server_players()

    def get_server(self) -> models.Server:
        """
        Get server from the API.
        """
        response = self.client._get("/server")
        if isinstance(response, dict):
            server = models.Server.from_dict(response, self.client)
            return server
        else:
            raise execptions.APIError(
                f"Unexpected response: {response.status_code}", client=self
            )

    def get_server_players(self) -> list[models.Player]:
        response = self.client._get("/server/players")
        if isinstance(response, list):
            players = [models.Player.from_dict(player) for player in response]
            self.cache["players"] = {player.id: player for player in players}
            return players
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_joinlogs(self) -> list[models.JoinLog]:
        response = self.client._get("/server/joinlogs")
        if isinstance(response, list):
            joinlogs = [
                models.JoinLog.from_dict(joinlog, self.client) for joinlog in response
            ]

            return joinlogs
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_queue(self) -> list[int]:
        response = self.client._get("/server/queue")
        if isinstance(response, list):
            return response
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_killlogs(self) -> list[models.KillLog]:
        response = self.client._get("/server/killlogs")
        if isinstance(response, list):
            killlogs = [
                models.KillLog.from_dict(killlog, self.client) for killlog in response
            ]

            return killlogs
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_commandlogs(self) -> list[models.CommandLog]:
        response = self.client._get("/server/commandlogs")
        if isinstance(response, list):
            commandlogs = [
                models.CommandLog.from_dict(commandlog, self.client)
                for commandlog in response
            ]
            return commandlogs
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_modcalls(self) -> list[models.ModCall]:
        response = self.client._get("/server/modcalls")
        if isinstance(response, list):
            modcalls = [
                models.ModCall.from_dict(modcall, self.client) for modcall in response
            ]
            return modcalls
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_bans(self) -> list[models.BannedPlayer]:
        response = self.client._get("/server/bans")
        if isinstance(response, list):
            return []
        if isinstance(response, dict):
            return [
                models.BannedPlayer(id=id, name=name) for id, name in response.items()
            ]
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_server_vehicles(self) -> list[models.Vehicle]:
        response = self.client._get("/server/vehicles")
        if isinstance(response, list):
            vehicles = [
                models.Vehicle.from_dict(vehicle, self.client) for vehicle in response
            ]
            return vehicles
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )

    def get_player(self, player_id: int) -> models.Player:
        player_id = int(player_id)
        if player_id in self.cache["players"]:
            return self.cache["players"][player_id]
        else:
            players = self.get_server_players()
            for player in players:
                if player.id == player_id:
                    return player
        return None

    def get_player_by_name(self, player_name: str) -> models.Player:
        player_name = str(player_name)
        for player in self.cache["players"].values():
            if player.name == player_name:
                return player
        return None

    def run_server_command(self, command: str):
        response = self.client._post("/server/command", data={"command": command})
        if response.get("message") == "Success":
            return True
        else:
            raise execptions.ErlcExecption(
                f"Unexpected response: {response.status.code}", client=self
            )
