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
        user_id = 6769616
        email = 'fpl@177arc.net'
        log.info(f'Downloading team data for user {user_id} using account {email}...')
        fpl = FPLPandas(user_id, email, 'TestMcTestFace')
        user_team, chips, transfers = fpl.get_user_team()
        log.info(f'Team data for user {user_id} downloaded.')
        self.assertTrue(user_team.shape[0] > 0)
        self.assertTrue(chips.shape[0] > 0)
        self.assertTrue(transfers.shape[0] > 0)

if __name__ == '__main__':
    unittest.main()
