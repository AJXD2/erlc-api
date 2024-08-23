from pydantic import BaseModel
from typing import Literal
from erlc.client import ErlcServerClient
from enum import Enum
from datetime import datetime


class Permission(Enum):
    """
    Permission enum
    """

    REMOTE = "Remote Server"
    OWNER = "Server Owner"
    ADMIN = "Server Administrator"
    MODERATOR = "Server Moderator"
    PLAYER = "Normal"


class Player(BaseModel):
    name: str
    id: int
    permissions: Permission
    callsign: str | None
    team: str | None

    @classmethod
    def from_dict(cls, data: dict):
        name, id = data["Player"].split(":")
        return cls(
            name=name,
            id=int(id),
            permissions=Permission(data["Permission"]),
            callsign=data.get("Callsign"),
            team=data.get("Team"),
        )


class RemoteManagment(Player):
    name: Literal["Remote Server"] = "Remote Server"
    id: Literal[0] = 0
    permissions: Literal[Permission.REMOTE] = Permission.REMOTE
    callsign: Literal[None] = None
    team: Literal[None] = None


class BannedPlayer(BaseModel):
    id: int
    name: str


class JoinLog(BaseModel):
    join: bool
    timestamp: datetime
    player: Player | int

    @classmethod
    def from_dict(cls, data: dict, client: ErlcServerClient):
        plr_id = data.get("Player", "0:0").split(":")[1]
        return cls(
            join=data["Join"],
            timestamp=datetime.fromtimestamp(data["Timestamp"]),
            player=client.server.get_player(plr_id) or plr_id,
        )


class CommandLog(BaseModel):
    player: Player | int
    time: datetime
    command: str

    @classmethod
    def from_dict(cls, data: dict, client: ErlcServerClient):
        if data["Player"] == "Remote Server":
            player = RemoteManagment()
        else:
            plr_id = data["Player"].split(":")[1]
            player = client.server.get_player(plr_id) or plr_id
        return cls(
            player=player,
            time=datetime.fromtimestamp(data["Timestamp"]),
            command=data["Command"],
        )


class KillLog(BaseModel):
    killer: Player | int
    victim: Player | int
    time: datetime

    @classmethod
    def from_dict(cls, data: dict, client: ErlcServerClient):
        killer = data["Killer"].split(":")[1]
        victim = data["Killed"].split(":")[1]
        return cls(
            killer=client.server.get_player(killer) or killer,
            victim=client.server.get_player(victim) or victim,
            time=datetime.fromtimestamp(data["Timestamp"]),
        )


class ModCall(BaseModel):
    caller: Player | int
    moderator: Player | None
    time: datetime

    @classmethod
    def from_dict(cls, data: dict, client: ErlcServerClient):
        clr_id = data["Caller"].split(":")[1]
        return cls(
            caller=client.server.get_player(clr_id) or clr_id,
            moderator=client.server.get_player(
                data.get("Moderator", "0:0").split(":")[1]
            ),
            time=datetime.fromtimestamp(data["Timestamp"]),
        )


class Vehicle(BaseModel):
    texture: str | None
    name: str
    owner: Player

    @classmethod
    def from_dict(cls, data: dict, client: ErlcServerClient):
        return cls(
            texture=data.get("Texture"),
            name=data["Name"],
            owner=client.server.get_player_by_name(data["Owner"]),
        )


class Server(BaseModel):
    client: ErlcServerClient
    name: str
    owner_id: int
    co_owner_ids: list[int]
    current_players: int
    max_players: int
    join_key: str
    acc_verified_req: Literal["Disabled", "Email", "Phone/ID"]
    team_balance: bool

    @property
    def joinlogs(self) -> list[JoinLog]:
        return self.client.server.get_server_joinlogs()

    @property
    def queue(self) -> list[int]:
        return self.client.server.get_server_queue()

    @property
    def killlogs(self) -> list[KillLog]:
        return self.client.server.get_server_killlogs()

    @property
    def commandlogs(self) -> list[CommandLog]:
        return self.client.server.get_server_commandlogs()

    @property
    def modcalls(self) -> list[ModCall]:
        return self.client.server.get_server_modcalls()

    @property
    def bans(self) -> list[int]:
        return self.client.server.get_server_bans()

    @property
    def players(self) -> list[Player]:
        return self.client.server.get_server_players()

    @property
    def vehicles(self) -> list[Vehicle]:
        return self.client.server.get_server_vehicles()

    def run_command(self, command: str) -> str:
        return self.client.server.run_server_command(command)

    def refresh(self) -> "Server":
        """
        Refresh the server data.
        """
        new_data = self.client.get_server()
        self.name = new_data.name
        self.owner_id = new_data.owner_id
        self.co_owner_ids = new_data.co_owner_ids
        self.current_players = new_data.current_players
        self.max_players = new_data.max_players
        self.join_key = new_data.join_key
        self.acc_verified_req = new_data.acc_verified_req
        self.team_balance = new_data.team_balance
        return self

    @classmethod
    def from_dict(cls, data: dict, client: ErlcServerClient) -> "Server":
        return cls(
            client=client,
            name=data["Name"],
            owner_id=data["OwnerId"],
            co_owner_ids=data["CoOwnerIds"],
            current_players=data["CurrentPlayers"],
            max_players=data["MaxPlayers"],
            join_key=data["JoinKey"],
            acc_verified_req=data["AccVerifiedReq"],
            team_balance=data["TeamBalance"],
        )

    model_config = {"arbitrary_types_allowed": True}
