import os
import sys
from click.testing import CliRunner
from swsscommon.swsscommon import SonicV2Connector
from utilities_common.db import Db

from .utils import get_result_and_return_code

import show.main as show

test_path = os.path.dirname(os.path.abspath(__file__))
mock_db_path = os.path.join(test_path, "mirror_input")

modules_path = os.path.dirname(test_path)
scripts_path = os.path.join(modules_path, "acl_loader")

class TestShowMirror(object):
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["PATH"] += os.pathsep + scripts_path
        print(os.pathsep + scripts_path)
        os.environ["UTILITIES_UNIT_TESTING"] = "1"

    def test_mirror_show(self):
        from .mock_tables import dbconnector
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config
        expected_output = """\
ERSPAN Sessions
Name    Status    SRC IP    DST IP    GRE    DSCP    TTL    Queue    Policer    Monitor Port    SRC Port    Direction
------  --------  --------  --------  -----  ------  -----  -------  ---------  --------------  ----------  -----------

SPAN Sessions
Name       Status    DST Port    SRC Port    Direction    Queue    Policer
---------  --------  ----------  ----------  -----------  -------  ---------
session1   active    Ethernet30  Ethernet40  both
session2   active    Ethernet7   Ethernet8   both
session11  active    Ethernet9   Ethernet10  rx
session15  active    Ethernet2   Ethernet3   tx
"""

        return_code, result = get_result_and_return_code('main.py show session')
        print("return_code: {}".format(return_code))
        print("result = {}".format(result))
        dbconnector.dedicated_dbs = {}
        assert return_code == 0
        assert result == expected_output

