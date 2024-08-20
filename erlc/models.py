from pydantic import BaseModel
from typing import Literal


class Server(BaseModel):
    name: str
    owner_id: int
    co_owner_ids: list[int]
    current_players: int
    max_players: int
    join_key: str
    acc_verified_req: Literal["Disabled", "Email", "Phone/ID"]
    team_balance: bool

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
    def from_dict(cls, data: dict) -> "Server":
        return cls(
            name=data["Name"],
            owner_id=data["OwnerId"],
            co_owner_ids=data["CoOwnerIds"],
            current_players=data["CurrentPlayers"],
            max_players=data["MaxPlayers"],
            join_key=data["JoinKey"],
            acc_verified_req=data["AccVerifiedReq"],
            team_balance=data["TeamBalance"],
        )
