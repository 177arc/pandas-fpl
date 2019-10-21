from fpl import FPL
import aiohttp
import pandas as pd
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fpl.utils import fetch, logged_in
from fpl.constants import API_URLS

class FPLPandas:
    """
    This class is a wrapper for the FPL library: https://github.com/amosbastian/fpl It converts the JSON output to pandas data frames.
    It also provides a synchronous layer over the asynchronous library in order to reduce the requirements for Jupyter kernel. Otherwise iPython >= 7.0
    (see https://stackoverflow.com/questions/47518874/how-do-i-run-python-asyncio-code-in-a-jupyter-notebook)
    and ipykernel >= 5.0.1  (see https://github.com/ipython/ipykernel/issues/356) are required.
    """
    __aio_pool: ThreadPoolExecutor
    __aio_loop: object
    __user_id: int
    __email: str
    __password: str
    __fpl: FPL

    def __init__(self, user_id: int = None, email: str = None, password: str = None, fpl: FPL = None):
        """
        Create a new instance of this class and initiates a thread for async execution.

        Args:
            user_id: The FPL user id. Only required for protected info such as user team. You can get the user id by
            selecting the Points tab on the FPL website and then extracting it from the browser URL like this:
            https://fantasy.premierleague.com/entry/{user_id}/event/6
            email: The email address used to log in to the FPL web site. Only required for protected info such as user team.
            password: The password used to log in to the FPL web site. Only required for protected info such as user team.
            fpl: The FPL instance to use. This particular useful for injecting a mock instance for automated testing.
            If not set, an FPL instance will be created.
        """

        self.set_cred(user_id, email, password)
        self.__fpl = fpl

        self.__aio_pool = ThreadPoolExecutor(1)
        self.__aio_loop = asyncio.new_event_loop()
        self.__aio_pool.submit(asyncio.set_event_loop, self.__aio_loop).result()

    def __del__(self):
        if not self.__aio_loop is None:
            self.__aio_loop.close()

    async def __call_api_async(self, func, requires_login: bool = False) -> dict:
        """ Calls the given FPL API function asynchronously.

        Args:
            func: The API function to execute.
            requires_login: Whether the call requires authentication.

        Returns:
            The Future of the passed function.
        """
        if requires_login and self.__email is None:
            raise ValueError("Email not provided. For functions that require login, the email address is mandatory. Please set the email address in the constructor. ")

        if requires_login and self.__password is None:
            raise ValueError("Password not provided. For functions that require login, the password is mandatory. Please set the password in the constructor.")

        async with aiohttp.ClientSession() as session:
            fpl = FPL(session) if self.__fpl is None else self.__fpl

            if requires_login:
                await fpl.login(self.__email, self.__password)

            return await func(fpl)


    def __call_api(self, func, requires_login: bool = False) -> dict:
        """ Calls the given FPL API function synchronously.

        Args:
            func: The API function to execute.

        Returns:
            The result of the passed function.
        """
        return self.__aio_pool.submit(self.__aio_loop.run_until_complete, self.__call_api_async(func, requires_login)).result()


    def set_cred(self, user_id: int, email: str, password: str) -> None:
        """ Sets the credentials to use when accessing user specific data. This method does not trigger a login call.
        Args:
            user_id: The FPL user id. Only required for protected info such as user team. You can get the user id by
            selecting the Points tab on the FPL website and then extracting it from the browser URL like this:
            https://fantasy.premierleague.com/entry/{user_id}/event/6
            email: The email address used to log in to the FPL web site. Only required for protected info such as user team.
            password: The password used to log in to the FPL web site. Only required for protected info such as user team.
        """
        self.__user_id = user_id
        self.__email = email
        self.__password = password


    def get_teams(self, team_ids: List[int] = None) -> pd.DataFrame:
        """Returns either a list of *all* teams, or a list of teams with IDs in
        the optional ``team_ids`` list.

        Information is taken from:
            https://fantasy.premierleague.com/api/bootstrap-static/

        Args:
            team_ids: (optional) List containing the IDs of teams. If not set a list of *all* teams will be returned.
        Returns:
            The teams as a pandas data frame.
        """
        json_data = self.__call_api(lambda fpl: fpl.get_teams(team_ids, return_json=True))
        return pd.DataFrame.from_records(json_data, index=['id'])


    def get_player(self, player_id: int) -> List[pd.DataFrame]:
        """Returns the player with the given ``player_id`` as a data frame and his associated data.

        Information is taken from:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/element-summary/1/ (optional)

        Args:
            player_id: A player's ID.
        Returns:
            1: The player data as a pandas data frame with one row indexed by ``player_id``.
            2: The summary stats for the past seasons s a pandas data frame indexed by ``player_id``, ``season_name``.
            3: The stats for the completed games as a pandas data frame indexed by ``player_id``, ``fixture``
            4: The data for the upcoming fixtures as a pandas data frame indexed by ``player_id``, ``event``
        Raises:
            ValueError: Player with ``player_id`` not found
        """
        def convert_player_df(json_data: dict, player_id: int, element: str, index: str) -> pd.DataFrame:
            player_df = pd.DataFrame.from_records(json_data[element])
            player_df['player_id'] = player_id

            return player_df.set_index(['player_id', index])

        json_data = self.__call_api(lambda fpl: fpl.get_player(player_id, players=None, include_summary=True, return_json=True))
        return [pd.DataFrame.from_records([json_data], index=['id']).rename(index={'id': 'player_id'}),
            convert_player_df(json_data, player_id, 'history_past', 'season_name'),
            convert_player_df(json_data, player_id, 'history', 'fixture'),
            convert_player_df(json_data, player_id, 'fixtures', 'event')]


    def get_players(self, player_ids: List[int] = None) -> List[pd.DataFrame]:
        """Returns either a list of *all' players, or a list of players whose
        IDs are in the given ``player_ids`` list as a data frame indexed by  indexed by ``player_id`` and their associated data.

        Information is taken from:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/element-summary/{player_id}/

        Args:
            player_ids: (optional) A list of player IDs
            if ``True``.
        Returns:
            1: The team players as a pandas data frame indexed by ``player_id``.
            2: The summary stats for the past seasons s a pandas data frame indexed by ``player_id``, ``season_name``.
            3: The stats for the completed games as a pandas data frame indexed by ``player_id``, ``fixture``
            4: The data for the upcoming fixtures as a pandas data frame indexed by ``player_id``, ``event``
        """
        def convert_players_df(json_data: List[dict], element: str, index: str) -> pd.DataFrame:
            players_df = pd.DataFrame()
            for player in json_data:
                player_df = pd.DataFrame.from_records(player[element])
                player_df['player_id'] = player['id']
                players_df = pd.concat([players_df, player_df], sort=False)

            return players_df.set_index(['player_id', index])

        json_data = self.__call_api(lambda fpl: fpl.get_players(player_ids, include_summary=True, return_json=True))
        return [pd.DataFrame.from_records(json_data, index=['id'], exclude=['history_past', 'history', 'fixtures']).rename(index={'id': 'player_id'}),
            convert_players_df(json_data, 'history_past', 'season_name'),
            convert_players_df(json_data, 'history', 'fixture'),
            convert_players_df(json_data, 'fixtures', 'event')]


    def get_fixtures(self) -> pd.DataFrame:
        """Returns a list of *all* fixtures as data frame.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/fixtures/
            https://fantasy.premierleague.com/api/fixtures/?event=1

        Returns:
            All fixtures of the season as a pandas data frame.
        """

        json_data = self.__call_api(lambda fpl: fpl.get_fixtures(return_json=True));
        return pd.DataFrame.from_records(json_data, index=['id'])


    def get_user_team(self, user_id: int = None):
        """ Returns information about the players in the current team, the chips and transfer info of the user with
        the given user ID. This method requires that a valid email and password are set using the constructor.

        Args:
            user_id: The user ID for which to get the team information. If not provided, it defaults to the user ID that
            was set in the constructor.

        Returns:
            The team, chips, transfer info as a pandas data frame.
        """
        async def get_user_team_async(fpl: FPL, user_id: int = None):
            if user_id is None:
                user_id = self.__user_id

            if user_id is None:
                raise ValueError('No user ID was specified. Please provide a user ID.')

            return await fpl.get_user_team(user_id)

        json_data = self.__call_api(lambda fpl: get_user_team_async(fpl, user_id), requires_login=True);
        return [pd.DataFrame.from_records(json_data['picks'], index=['element']),
                pd.DataFrame.from_records(json_data['chips']),
                pd.DataFrame.from_records([json_data['transfers']])]


# Extension methods for FPL. These are necessary because FPL does not expose all available data.
async def fpl_get_user_team(self, user_id: str) -> List[pd.DataFrame]:
    """Gets current team, the chips and the transfer info of the logged in user. Requires the user to have
    logged in using ``fpl.login()``.

    Information is taken from:
        https://fantasy.premierleague.com/api/my-team/91928/

    Args:
        user_id: The user ID for which to get the team information. If not provided, it defaults to the user ID that
        was set in the constructor.

    Returns:
        Current team, the chips and the transfer info as data frames.
    """
    if not logged_in(self.session):
        raise Exception("User must be logged in.")

    response = await fetch(
        self.session, API_URLS["user_team"].format(user_id))

    if response == {"details": "You cannot view this entry"}:
        raise ValueError("User ID does not match provided email address!")

    return response

FPL.get_user_team = fpl_get_user_team
