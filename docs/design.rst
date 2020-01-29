Design Document
===============


This document is meant to plan and define the design of wtf.


Test Components
===============

Test components are the components which are available for use by test writers.

- TestCase
  - Tags - Enable grouping of tests
- TestSuite 
- Fixture


Default Fixtures:
- Result Collector
- Sandboxer - Run in separate process
- Logger (Wrap stdout/stderr)

Test Case
---------

Test Suite
----------

A TestSuite is just a collection of tests. Tests within a Test Suite are
tightly coupled. They can be thought of as multi-part tests. TestCase objects
in a TestSuite are executed in order and if one fails, remaining tests in the
TestSuite will be skipped. Tests in a TestSuite are guaranteed to be run on
a single executor.

Fixtures
--------

Fixtures form a dependency tree. Some global phony fixtures exist which custom
fixtures can depend on to guarantee their build times. 

Phony Dependencies:
- Global: The fixture si built beginning before any test is executed
- Environment: The fixture need to be built any time it's placed in a new
  context (E.g. on a separate thread/machine)
- Test: The fixture is built at the start of each test

Tests are all enumerated in the same module space. This means that any fixtures
created in a module will be shared across tests.

Test System Components
======================

Test system components refers to components which are internal to the test
framework. 

- TestCase
    - Tags
- Fixture
- Test Server - The separate test server component will schedule execution of tests.
- Test Client - The separate test client component will execute a test and report results.

- TODO Test Runner - Configurable? 
    E.g. Enable failfast, Enable Ctrl-C, Enable multithreaded/multisystem/multicore
- TODO Sandboxing? - Through a fixture?, 
      E.g. Interaction w/ test (pause), Timeouts, Dockerenv, pyenv
- TODO Logging? - Through a fixture?
- TODO Config? - Through a fixture?


Requirements:
- Run expensive tests at the same time
- Run tests in a docker environment
- Run tests in a separate process
- Tests need to share a built fixture 
- Log test results to a single log
- Log test results to individual logs
- Parse + Log output from subprocesses during a test



TODO Figure out interaction between fixtures and multiple test runners

Test Item Discovery
-------------------

Discovery of test items will be automatic. I.e. it isn't necessary to specify
a list of tests.

Test modules should be able to include other test modules without adding their
tests to the global test list. The test discovery method will only enumerate
tests in the current test module.

Test Server
-----------

The test server is responsible for:

- Initial discovery of all tests and fixtures
- Spawning of the initial test client
- Scheduling execution of tests and fixture builds on client(s)

Test Client
-----------

The Test Client is responsible for:

- Receiving test information from the server
- Building Fixtures
- Executing tests
- Reporting results to the server

Test Execution
--------------

NOTE: A fail-fast fixture could be added:
- Depend on the Test phony fixture (so it's built before each test)
- On test teardown save the test result
- On test setup check if the result == Failed, if so skip the test.
- TODO Issue would be sharing the state across multiple systems. The fixture
  would have to be synchronized across a network.

Goals
=====

This test framework should be as simple as possible. The intent of this
framework is to define default scaffolding that is required by just about any
test writer. 

This framework should prefer to only offer items which couldn't be provided in
any other sane way.  For example, this framework provides a kill signal
handler. In theory this could be offered by a global fixture. However, setup
and tear-down of the fixture could lead to unexpected handling if the handler
were invoked just before test start or just after test completion. Rather than
implementing this feature as a default provided fixture, we implement this at
the library level since this is the only sane location.


Testing Phases
==============

There are distinct phases of execution of the testing framework:

1. The test server starts main method.

2. The test server enumerates all tests and fixtures in a single process by
walking the tree of the argument supplied directory and executing each file.

3. The test server constructs a default test client which will handle both
builds of fixtures execution of tests.

4. The test server will send an RPC telling the test client to build the list of
given (global) fixtures. The test client will build those fixtures, and respond to the
server when the setup of all fixtures is complete.

5. The test server will now try to schedule tests. To do so, the test server
will send an RPC telling the client to build each fixture required for the
test, the client will respond with the result of each build. The server will
send a command to run the test, the client will respond with the result.

    How will shared fixtures work in a multi-client scenario?

    - The server will enforce that fixtures which are used across tests are not
      shared across different test clients.
    - The server fixture enumeration must maintain information indicating that
      a fixture is shared between multiple tests.
    - A property will be added to Fixtures which enables them to be re-built if
      a new client is used. This fixture will be a tri-state to indicate preference
      for rebuilding: "single-client", "single-client-preferred", "multi-client".
      - A single client fixture will never allow test which share the fixture to
        run on a separate client - even if another client is completely unused.
      - A single client preferred will allow the test to move to a different client
        and the fixture to be torn-down and set up if there are no other tests
        capable of running on another client.
      - The scheduler will give no preference to re-use a shared fixture on given
        client if the multi-client state is given.


The test scheduling algorithm looks like this::
    
    pass


- Test server starts
- Test server enumerates all tests
- Test server constructs a local test client
- Test server schedules construction of global fixtures on client(s)

Execution Phase Loop:
- Test server schedules construction of fixtures on client
- Test server schedules execution of test on client
- Test clients report results
