import unittest
import unittest.mock as mock
import asyncio
from fplpandas import FPLPandas
import logging as log
import pandas as pd
from pandas.util.testing import assert_frame_equal

log.basicConfig(level=log.INFO, format='%(message)s')


class TestFplPandas(unittest.TestCase):
    def test_get_teams(self):
        test_data = [{'id': 1, 'attr1': 'value11', 'attr2': 'value12'},
                     {'id': 2, 'attr1': 'value21', 'attr2': 'value22'}]

        fpl_mock = mock.MagicMock()

        async def mock_get_team(team_ids, return_json):
            self.assertEqual(team_ids, None)
            self.assertEqual(return_json, True)
            return test_data

        fpl_mock.get_teams = mock_get_team

        fpl = FPLPandas(fpl=fpl_mock)
        actual_df = fpl.get_teams()
        expected_df = pd.DataFrame.from_dict(test_data).set_index('id')
        self.assertTrue(expected_df.equals(actual_df))

    def test_get_teams_with_ids(self):
        test_data = [{'id': 1, 'attr1': 'value11', 'attr2': 'value12'},
                     {'id': 2, 'attr1': 'value21', 'attr2': 'value22'}]

        fpl_mock = mock.MagicMock()

        async def mock_get_team(team_ids, return_json):
            self.assertEqual(team_ids, [1, 2])
            self.assertEqual(return_json, True)
            return test_data

        fpl_mock.get_teams = mock_get_team

        fpl = FPLPandas(fpl=fpl_mock)
        actual_df = fpl.get_teams([1, 2])
        expected_df = pd.DataFrame.from_dict(test_data).set_index('id')
        self.assertTrue(expected_df.equals(actual_df))

    def test_get_fixtures(self):
        test_data = [{'id': 1, 'attr1': 'value11', 'attr2': 'value12'},
                     {'id': 2, 'attr1': 'value21', 'attr2': 'value22'}]

        fpl_mock = mock.MagicMock()

        @asyncio.coroutine
        def mock_get_fixtures(ids, return_json):
            self.assertTrue(set([1, 2]) <= set(ids))
            self.assertEqual(return_json, True)
            return test_data

        fpl_mock.get_fixtures_by_id = mock_get_fixtures

        fpl = FPLPandas(fpl=fpl_mock)
        actual_df = fpl.get_fixtures()
        expected_df = pd.DataFrame.from_dict(test_data).set_index('id')

        self.assertTrue(expected_df.equals(actual_df))

    def test_get_player(self):
        test_data = {'id': 1, 'attr1': 'value11', 'attr2': 'value12',
                          'history_past': [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12'},
                                            {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22'}],
                          'history': [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                      {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                          'fixtures': [{'event': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                       {'event': 2, 'attr1': 'value21', 'attr2': 'value22'}]
                      }
        expected_history_past = [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                                 {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1}]
        expected_history = [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                         {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1}]
        expected_fixtures = [{'event': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                            {'event': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1}]

        expected_player_df = pd.DataFrame.from_records([test_data], index=['id']).rename(index={'id': 'player_id'})
        expected_history_past_df = pd.DataFrame.from_dict(expected_history_past).set_index(['player_id', 'season_name'])
        expected_history_df = pd.DataFrame.from_dict(expected_history).set_index(['player_id', 'fixture'])
        expected_fixtures_df = pd.DataFrame.from_dict(expected_fixtures).set_index(['player_id', 'event'])

        fpl_mock = mock.MagicMock()

        async def mock_get_player(player_id, players, include_summary, return_json):
            self.assertEqual(player_id, 1)
            self.assertEqual(players, None)
            self.assertEqual(include_summary, True)
            self.assertEqual(return_json, True)
            return test_data

        fpl_mock.get_player = mock_get_player

        fpl = FPLPandas(fpl=fpl_mock)
        actual_player_df, actual_history_past_df, actual_history_df, actual_fixture_df = fpl.get_player(1)

        assert_frame_equal(expected_player_df, actual_player_df)
        assert_frame_equal(expected_history_past_df, actual_history_past_df)
        assert_frame_equal(expected_history_df, actual_history_df)
        assert_frame_equal(expected_fixtures_df, actual_fixture_df)


    def test_get_players_all(self):
        test_data = [{'id': 1, 'attr1': 'value11', 'attr2': 'value12',
                          'history_past': [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12'},
                                            {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22'}],
                          'history': [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                      {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                          'fixtures': [{'event': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                       {'event': 2, 'attr1': 'value21', 'attr2': 'value22'}]
                      },
                     {'id': 2, 'attr1': 'value21', 'attr2': 'value22',
                          'history_past': [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12'},
                                            {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22'}],
                          'history': [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                      {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                          'fixtures': [{'event': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                       {'event': 2, 'attr1': 'value21', 'attr2': 'value22'}]
                    }]

        expected_players= [{'id': 1, 'attr1': 'value11', 'attr2': 'value12'},
                           {'id': 2, 'attr1': 'value21', 'attr2': 'value22'}]
        expected_history_past = [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                                 {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1},
                                 {'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12', 'player_id': 2},
                                 {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22', 'player_id': 2}]
        expected_history = [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                         {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1},
                            {'fixture': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 2},
                            {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 2}]
        expected_fixtures= [{'event': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                            {'event': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1},
                            {'event': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 2},
                            {'event': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 2}]

        expected_players_df = pd.DataFrame.from_dict(expected_players).set_index('id').rename(index={'id': 'player_id'})
        expected_history_past_df = pd.DataFrame.from_dict(expected_history_past).set_index(['player_id', 'season_name'])
        expected_history_df = pd.DataFrame.from_dict(expected_history).set_index(['player_id', 'fixture'])
        expected_fixtures_df = pd.DataFrame.from_dict(expected_fixtures).set_index(['player_id', 'event'])

        fpl_mock = mock.MagicMock()

        async def mock_get_players(player_ids, include_summary, return_json):
            self.assertEqual(player_ids, None)
            self.assertEqual(include_summary, True)
            self.assertEqual(return_json, True)
            return test_data

        fpl_mock.get_players = mock_get_players

        fpl = FPLPandas(fpl=fpl_mock)
        actual_players_df, actual_history_past_df, actual_history_df, actual_fixture_df = fpl.get_players()

        assert_frame_equal(expected_players_df, actual_players_df)
        assert_frame_equal(expected_history_past_df, actual_history_past_df)
        assert_frame_equal(expected_history_df, actual_history_df)
        assert_frame_equal(expected_fixtures_df, actual_fixture_df)


    def test_get_players_with_ids(self):
        test_data = [{'id': 1, 'attr1': 'value11', 'attr2': 'value12',
                          'history_past': [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12'},
                                            {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22'}],
                          'history': [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                      {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                          'fixtures': [{'event': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                       {'event': 2, 'attr1': 'value21', 'attr2': 'value22'}]
                      },
                     {'id': 3, 'attr1': 'value21', 'attr2': 'value22',
                      'history_past': [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12'},
                                       {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22'}],
                      'history': [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                  {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                      'fixtures': [{'event': 1, 'attr1': 'value11', 'attr2': 'value12'},
                                   {'event': 2, 'attr1': 'value21', 'attr2': 'value22'}]
                      }]

        expected_players= [{'id': 1, 'attr1': 'value11', 'attr2': 'value12'},
                           {'id': 3, 'attr1': 'value21', 'attr2': 'value22'}]
        expected_history_past = [{'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                                 {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1},
                                 {'season_name': '2017/18', 'attr1': 'value11', 'attr2': 'value12', 'player_id': 3},
                                 {'season_name': '2018/19', 'attr1': 'value21', 'attr2': 'value22', 'player_id': 3}]
        expected_history = [{'fixture': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                         {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1},
                            {'fixture': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 3},
                            {'fixture': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 3}]
        expected_fixtures= [{'event': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 1},
                            {'event': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 1},
                            {'event': 1, 'attr1': 'value11', 'attr2': 'value12', 'player_id': 3},
                            {'event': 2, 'attr1': 'value21', 'attr2': 'value22', 'player_id': 3}]

        expected_players_df = pd.DataFrame.from_dict(expected_players).set_index('id').rename(index={'id': 'player_id'})
        expected_history_past_df = pd.DataFrame.from_dict(expected_history_past).set_index(['player_id', 'season_name'])
        expected_history_df = pd.DataFrame.from_dict(expected_history).set_index(['player_id', 'fixture'])
        expected_fixtures_df = pd.DataFrame.from_dict(expected_fixtures).set_index(['player_id', 'event'])

        fpl_mock = mock.MagicMock()

        async def mock_get_players(player_ids, include_summary, return_json):
            self.assertEqual(player_ids, [1, 3])
            self.assertEqual(include_summary, True)
            self.assertEqual(return_json, True)
            return test_data

        fpl_mock.get_players = mock_get_players

        fpl = FPLPandas(fpl=fpl_mock)
        actual_players_df, actual_history_past_df, actual_history_df, actual_fixture_df = fpl.get_players([1, 3])

        assert_frame_equal(expected_players_df, actual_players_df)
        assert_frame_equal(expected_history_past_df, actual_history_past_df)
        assert_frame_equal(expected_history_df, actual_history_df)
        assert_frame_equal(expected_fixtures_df, actual_fixture_df)

    def test_get_user_team_with_user(self):
        test_data = {'picks': [{'element': 1, 'attr1': 'value11', 'attr2': 'value12'},
                            {'element': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                     'chips': [{'attr1': 'value11', 'attr2': 'value12'}],
                     'transfers': {'attr1': 'value11', 'attr2': 'value12'}}

        expected_picks_df = pd.DataFrame.from_dict(test_data['picks']).set_index('element').rename(index={'element': 'player_id'})
        expected_chips_df = pd.DataFrame.from_dict(test_data['chips'])
        expected_transfers_df = pd.DataFrame.from_dict([test_data['transfers']])

        fpl_mock = mock.MagicMock()

        async def mock_login(email, password):
            self.assertEqual(email, 'email')
            self.assertEqual(password, 'password')

        async def mock_get_user_info():
            return {'player': {'entry': '123'}}

        async def mock_get_user_team(user_id):
            self.assertEqual(user_id, '123')
            return test_data

        fpl_mock.get_user_team = mock_get_user_team
        fpl_mock.get_user_info = mock_get_user_info
        fpl_mock.login = mock_login

        fpl = FPLPandas('email', 'password', fpl=fpl_mock)
        actual_picks_df, actual_chips_df, actual_transfers_df = fpl.get_user_team()

        assert_frame_equal(expected_picks_df, actual_picks_df)
        assert_frame_equal(expected_chips_df, actual_chips_df)
        assert_frame_equal(expected_transfers_df, actual_transfers_df)


    def test_get_user_team_with_user_id(self):
        test_data = {'picks': [{'element': 1, 'attr1': 'value11', 'attr2': 'value12'},
                            {'element': 2, 'attr1': 'value21', 'attr2': 'value22'}],
                     'chips': [{'attr1': 'value11', 'attr2': 'value12'}],
                     'transfers': {'attr1': 'value11', 'attr2': 'value12'}}

        expected_picks_df = pd.DataFrame.from_dict(test_data['picks']).set_index('element').rename(index={'element': 'player_id'})
        expected_chips_df = pd.DataFrame.from_dict(test_data['chips'])
        expected_transfers_df = pd.DataFrame.from_dict([test_data['transfers']])

        fpl_mock = mock.MagicMock()

        async def mock_login(email, password):
            self.assertEqual(email, 'email')
            self.assertEqual(password, 'password')

        async def mock_get_user_team(user_id):
            self.assertEqual(user_id, 456)
            return test_data

        fpl_mock.get_user_team = mock_get_user_team
        fpl_mock.login = mock_login

        fpl = FPLPandas('email', 'password', fpl=fpl_mock)
        actual_picks_df, actual_chips_df, actual_transfers_df = fpl.get_user_team(456)
        assert_frame_equal(expected_picks_df, actual_picks_df)
        assert_frame_equal(expected_chips_df, actual_chips_df)
        assert_frame_equal(expected_transfers_df, actual_transfers_df)

    def test_get_user_team_no_email(self):
        fpl_mock = mock.MagicMock()

        fpl = FPLPandas(None, 'password', fpl=fpl_mock)
        with self.assertRaisesRegex(ValueError, 'email'):
            fpl.get_user_team()

    def test_get_user_team_no_password(self):
        fpl_mock = mock.MagicMock()

        fpl = FPLPandas('email', None, fpl=fpl_mock)
        with self.assertRaisesRegex(ValueError, 'password'):
            fpl.get_user_team()

    def test_get_user_info(self):
        test_data = {'player': {'entry': '123'}}
        expected_df = pd.DataFrame.from_dict([test_data['player']])

        fpl_mock = mock.MagicMock()

        async def mock_login(email, password):
            self.assertEqual(email, 'email')
            self.assertEqual(password, 'password')

        async def mock_get_user_info():
            return {'player': {'entry': '123'}}

        fpl_mock.get_user_info = mock_get_user_info
        fpl_mock.login = mock_login

        fpl = FPLPandas('email', 'password', fpl=fpl_mock)
        actual_df = fpl.get_user_info()

        assert_frame_equal(expected_df, actual_df)


if __name__ == '__main__':
    unittest.main()
