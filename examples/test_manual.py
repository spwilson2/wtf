import wtf.test as test

# The testfunction wrapper is just syntatic sugar around a TestFunction object.
# A TestFunction object can be created manualy as follows:

def simple_testfunction1(fixtures):
    pass

test.TestFunction(simple_testfunction1)


# Tests can also be created by traditional objects.
#
# This can be useful in cases where more advanced logic is required or test
# functionality might be reusable.

class ReusableTest(test.TestCase):
    def complex_logic(self, diff):
        print('Doing some complex shared logic')
        print('The difference is I do: %s' % str(diff))

    def diff_logic(self):
        self.complex_logic('ReusableTest')

    def execute(self, fixtures):
        self.diff_logic()


class CopiedTest(ReusableTest):
    def diff_logic(self):
        self.complex_logic('CopiedTest')

# Allocate both tests supplying their name so they are enumerated by the
# system.
ReusableTest('reusable_test_case')
CopiedTest('copied_test_case')
