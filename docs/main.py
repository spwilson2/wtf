def enumerate_cases():
    '''Enumerate all test cases in the given directory tree.'''
    pass

def create_fixture_tree(test_cases):
    '''Create a Fixture DAG based on the fixtures attached to the given test cases.'''
    pass

def build_globals(fixtures):
    '''Build any global fixtures from the given fixture DAG.'''
    pass

def schedule_tests(tests, fixture_dag):
    pass

# Enumerate tests and fixtures
tests = enumerate_cases()
# Fixtures are attached to the test_cases, invert the tree
fixtures = create_fixture_tree(tests)
# Build global fixtures
#build_globals(fixtures)
# Schedule tests to run
handle = schedule_tests(tests)
# Use the scheduled test handle to wait for and collect all test results
results = collect_results(handle)

# TODO: Add hooks to post-process results.
process_results(results)
