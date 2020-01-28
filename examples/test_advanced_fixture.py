'''
This module contains example uses of advanced fixture features such as delayed
initialization.
'''
from wtf import *


class MakeBuildFixture(Fixture):
    '''
    This fixture acts as a collector of Make Targets. Before the first test is
    executed its ``setup`` method will run. This will cause all MakeTarget
    fixtures which depend on this fixture to build using a single invocation of
    make.

    This fixture disables the lazy_init feature of Fixture objects. This allows
    this Fixture to build all required files at the same time without waiting
    for a single test to run. This is particularly useful for environments
    where build systems take an excesive amount of time to enumerate build
    targets.
    '''
    def __init__(self, *args, **kwargs):
        fixture.Fixture.__init__(self,
                # We'll build this fixture only once (on its first "use")
                build_once=True, 
                # This fixture will be built before any tests are executed
                # (It won't lazily wait until a test which requires it.)
                lazy_init=False, *args, **kwargs)
        self.targets = []

    def setup(self):
        super(MakeFixture, self).setup()
        targets = set(self.required_by)
        command = ['make']
        command.extend([target.target for target in targets])
        logger.log.debug('Executing command: %s' % command)
        helper.log_call(command)


class MakeTarget(Fixture):
    # Save a single MakeBuildFixture which we'll put every one of our targets
    # into.
    _make_fixture = MakeBuildFixture('Global Make Fixture')

    def __init__(self, target, *args, **kwargs):
        fixture.Fixture.__init__(self, name=target, *args, **kwargs)
        self.target = self.name

        # Fixtures can depend on other fixtures.
        #
        # All Make Targets depend on the MakeBuild to guarantee they will be
        # built.
        self.require(self._make_fixture)

    def setup(self):
        Fixture.setup(self)
        self.make_fixture.setup()
        return self

first_fixture = [
    MakeTarget('first-target'),
]

second_fixture = [
    MakeTarget('second-target'),
]

# This will create two separate tests.
# One test will receive the first_fixture list.
# One test will receive the second_fixture list.
@test.testfunction(fixtures=first_fixture)
@test.testfunction(fixtures=second_fixture)
def different_fixture_test(fixtures):
    print('Received fixture: "%s"', fixtures[0])
    assert 'first-target' in fixtures or 'second-target' in fixtures
