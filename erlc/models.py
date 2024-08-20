from pydantic import BaseModel
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from erlc.client import ErlcServerClient


class Server(BaseModel):
    client: "ErlcServerClient"
    name: str
    owner_id: int
    co_owner_ids: list[int]
    current_players: int
    max_players: int
    join_key: str
    acc_verified_req: Literal["Disabled", "Email", "Phone/ID"]
    team_balance: bool

    def refresh(self):
        """
        Refresh the server data.
        """
        self = self.client.get_server()
        return self

    @classmethod
    def from_dict(cls, data: dict, client: "ErlcServerClient") -> "Server":
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
