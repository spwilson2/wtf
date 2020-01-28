import os
import shutil
import subprocess
import tempfile

import wtf.test as test
import wtf.fixture as fixture
import wtf.wrappers as wrappers

class TempdirFixture(fixture.Fixture):
    def __init__(self, *args, **kwargs):
        fixture.Fixture.__init__(self, build_once=False, *args, **kwargs)

    def setup(self):
        # Setup will be called before the test begins
        self.tmpdir = tempfile.mkdtemp()

    def teardown(self):
        # Teardown will be called after the test completes
        # This will be called even if the test fails
        shutil.rmtree(self.tmpdir)

@test.testfunction(fixtures=[TempdirFixture()])
def test_tempdir_fixture(fixtures):
    tmpdir_fixture = fixtures[0]
    d = tmpdir_fixture.tmpdir
    assert os.path.isdir(d)
    subprocess.check_call(['touch', os.path.join(d, 'file')])
