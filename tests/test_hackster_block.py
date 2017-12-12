import responses
import json
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..hackster_block import Hackster
from nio.block.terminals import DEFAULT_TERMINAL

SAMPLE_RESPONSE = {
    'metadata': {},
    'records': [
        {
            'id': 19589,
            'hid': '143801',
            'name': 'The \'Tennis Ball\' Garage Stop Light',
            'one_liner': 'Eliminate the need for a hanging tennis ball ...',
            'url': 'https://www.hackster.io/stuart/the-tennis-ball ...',
            'content_type': 'tutorial',
            'duration': 6,
            'difficulty': 'intermediate'
        }
    ]
}


class TestMojioVehicles(NIOBlockTestCase):

    def setUp(self):
        super().setUp()

    @responses.activate
    def test_request(self):
        blk = Hackster()

        responses.add(responses.POST, 'https://www.hackster.io/oauth/token',
                      json={}, status=200)
        responses.add(responses.GET, 'http://api.hackster.io/v2/projects',
                      body=json.dumps(SAMPLE_RESPONSE), status=200,
                      content_type='application/json')
        self.configure_block(blk, {
            'polling_interval': {
                'seconds': 0  # We will drive polls with signals
            },
            'queries': ['dummy']
        })
        blk.start()

        blk.process_signals([Signal()])
        self.assert_num_signals_notified(1)
        self.assertEqual(self.last_notified[DEFAULT_TERMINAL][0].name,
                         'The \'Tennis Ball\' Garage Stop Light')

        blk.stop()
