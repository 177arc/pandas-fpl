import unittest
from fplpandas import FPLPandas
import logging as log
import warnings

log.basicConfig(level=log.INFO, format='%(message)s')


class TestFplPandas(unittest.TestCase):
    def test_get_teams(self):
        log.info(f'Downloading teams ...')
        fpl = FPLPandas()
        teams = fpl.get_teams()
        log.info(f'Downloaded {teams.shape[0]} teams.')

        self.assertTrue(teams.shape[0] > 0)

    def test_get_game_weeks(self):
        log.info(f'Downloading game weeks ...')
        fpl = FPLPandas()
        game_weeks = fpl.get_game_weeks()
        log.info(f'Downloaded {game_weeks.shape[0]} game weeks.')

        self.assertTrue(game_weeks.shape[0] == 38)

    def test_get_game_weeks_by_ids(self):
        log.info(f'Downloading game weeks ...')
        fpl = FPLPandas()
        game_weeks = fpl.get_game_weeks([1,2])
        log.info(f'Downloaded {game_weeks.shape[0]} game weeks.')

        self.assertTrue(game_weeks.shape[0] == 2)

    def test_get_fixtures(self):
        log.info(f'Downloading fixtures ...')
        fpl = FPLPandas()
        fixtures = fpl.get_fixtures()
        log.info(f'Downloaded {fixtures.shape[0]} fixtures.')

        self.assertTrue(fixtures.shape[0] > 0)

    def test_get_players(self):
        log.info(f'Downloading data for all players ...')
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            fpl = FPLPandas()
            players, history_past, history, fixtures = fpl.get_players()
        log.info(f'Downloaded {players.shape[0]} players.')

        self.assertTrue(players.shape[0] > 0)
        self.assertTrue(history_past.shape[0] > 0)
        self.assertTrue(history.shape[0] >= 0)
        self.assertTrue(fixtures.shape[0] >= 0)

    def test_get_player(self):
        id = 1
        log.info(f'Downloading data for player {id} ...')
        fpl = FPLPandas()
        player, history_past, history, fixtures = fpl.get_player(id)
        log.info(f'Downloaded.')

        self.assertTrue(player.shape[0] == 1)
        self.assertTrue(history_past.shape[0] >= 0)
        self.assertTrue(history.shape[0] >= 0)
        self.assertTrue(fixtures.shape[0] >= 0)

    def test_get_user_team(self):
        email = 'fpl@177arc.net'
        log.info(f'Downloading team data for account {email}...')
        fpl = FPLPandas(email, 'TestMcTestFace')
        user_team, chips, transfers = fpl.get_user_team()
        log.info(f'Team data downloaded.')

        self.assertTrue(user_team.shape[0] > 0)

    def test_get_user_info(self):
        email = 'fpl@177arc.net'
        log.info(f'Downloading user info for account {email}...')
        fpl = FPLPandas(email, 'TestMcTestFace')
        user_info = fpl.get_user_info()
        log.info(f'User info downloaded.')

        self.assertTrue(user_info.shape[0] > 0)


if __name__ == '__main__':
    unittest.main()
