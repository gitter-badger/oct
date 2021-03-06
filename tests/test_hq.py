import os
import sys
import unittest
import shutil
import json
from multiprocessing import Process
from oct_turrets.turret import Turret
from oct_turrets.utils import load_file, validate_conf
from oct.utilities.run import run, main
from oct.utilities.newproject import create_project


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def run_turret():
    """Run a simple turret for testing the hq
    """
    module = load_file(os.path.join(BASE_DIR, 'fixtures', 'v_user.py'))
    config = validate_conf(os.path.join(BASE_DIR, 'fixtures', 'turret_config.json'))
    turret = Turret(config, module)
    turret.start()


def run_bad_turret():
    module = load_file(os.path.join(BASE_DIR, 'fixtures', 'bad_user.py'))
    config = validate_conf(os.path.join(BASE_DIR, 'fixtures', 'turret_config.json'))
    turret = Turret(config, module)
    turret.start()


class CmdOpts(object):
    project_dir = '/tmp/oct-test'
    project_name = '.'


class HQTest(unittest.TestCase):

    def setUp(self):
        self.turret = Process(target=run_turret)
        self.turret.start()
        self.bad_turret = Process(target=run_bad_turret)
        self.bad_turret.start()
        create_project('/tmp/oct-test')

        # update the runtime for the project
        with open(os.path.join(BASE_DIR, 'fixtures', 'config.json')) as f:
            data = json.load(f)

        with open(os.path.join('/tmp/oct-test', 'config.json'), 'w') as f:
            json.dump(data, f)

    def test_run_hq(self):
        """Test hq
        """
        run(CmdOpts())

    def test_run_argparse(self):
        """Test runing hq with command line arguments
        """
        sys.argv = sys.argv[:1]
        opts = CmdOpts()
        sys.argv += [opts.project_name, "-d", opts.project_dir]
        main()

    def test_create_errors(self):
        """Test errors when creating project
        """
        with self.assertRaises(OSError):
            create_project('/tmp')

    def tearDown(self):
        shutil.rmtree('/tmp/oct-test')
        self.turret.terminate()
        self.bad_turret.terminate()
        if os.path.isfile('/tmp/results.sqlite'):
            os.remove('/tmp/results.sqlite')

if __name__ == '__main__':
    unittest.main()
