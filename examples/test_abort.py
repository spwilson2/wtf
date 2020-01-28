import wtf.test as test

# Tests can abort during execution.
#
# This can be used to skip a test if some given system requirement isn't
# available.

# This will mark the test with a non-failure status.
@test.testfunction(tag='Abort')
def simple_abort_test1(fixtures):
    test.abort('Abort this test.')

