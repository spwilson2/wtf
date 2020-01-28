import wtf.test as test
import wtf.fixture as fixture

# The only fixture built into the default wtf library is the ConfigFixture.
# The ConfigFixture
# A global config fixture is provided to all other fixtures.

class ConfigUserFixture(fixture.Fixture):
    def print_test_root(self):
        print(self.config['test_root'])

@test.testfunction(fixtures=[ConfigUserFixture()])
def test_print_root(fixtures):
    fixtures[0].config
