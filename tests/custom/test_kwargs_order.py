import pytest
def test_collision(get_contract):
    src = """
u: public(uint256)

@external
def foo():
    self.bar(1)

def bar(a:uint256=1, b:uint256=2, c:uint256=3):
    self.u = b + c
    """
    c = get_contract(src)
    c.foo()
    with pytest.raises(AssertionError):
        assert c.u() == 5

    # b=1, c=2
    assert c.u() == 3

def test_collision2(get_contract):
    src = """
u: public(uint256)

@external
def foo():
    self.bar(1, 2)

def bar(a:uint256=1, b:uint256=2, c:uint256=3):
    self.u = b + c
    """
    c = get_contract(src)
    c.foo()
    with pytest.raises(AssertionError):
        assert c.u() == 5

    # b=2, c=1
    assert c.u() == 3


def test_no_collision(get_contract):
    src = """
u: public(uint256)

@external
def foo():
    self.bar(1, 2, 3)

def bar(a:uint256=1, b:uint256=2, c:uint256=3):
    self.u = a + b + c
    """
    c = get_contract(src)
    c.foo()
    assert c.u() == 6
