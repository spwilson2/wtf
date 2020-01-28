import wtf.test as test

@test.testfunction
def basic_test():
    print('This test will pass!')
    assert True


@test.testfunction
def basic_failing_test():
    print('This test will fail!')
    assert False


@test.testfunction(tag='tagged')
def tagged_test():
    print('This test will run when --tags=tagged')
    pass
