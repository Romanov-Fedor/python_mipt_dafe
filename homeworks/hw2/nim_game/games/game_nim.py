import json

from nim_game.common.enumerations import Players
from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config) as f:
            text = json.load(f)
            heaps_amount = int(text["heaps_amount"])
            opponent_level = str(text["opponent_level"])

            self._environment = EnvironmentNim(heaps_amount)
            self._agent = Agent(opponent_level)

    def make_steps(self, player_step: NimStateChange) -> GameState:
        Game_state = GameState()
        self._environment.change_state(player_step)
        Game_state.heaps_state = self._environment.get_state()
        Game_state.opponent_step = player_step
        if self.is_game_finished():
            Game_state.winner = Players.USER
            return Game_state

        agent_step = self._agent.make_step(self._environment.get_state())
        self._environment.change_state(agent_step)
        Game_state.heaps_state = self._environment.get_state()
        Game_state.opponent_step = agent_step
        if self.is_game_finished():
            Game_state.winner = Players.BOT
            return Game_state
        return Game_state

    def is_game_finished(self) -> bool:
        return True if sum(self._environment.get_state()) == 0 else False

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
