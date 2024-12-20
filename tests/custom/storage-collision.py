import pytest

def test_collision(get_contract):
    src = """
u: public(uint256)
u1: public(uint256)
u2: public(uint256)


@external
@nonreentrant
def foo():
    self.u = 5
    self.u1 = 5
    self.u2 = 5
    """

    c = get_contract(src)
    c.foo()
    with pytest.raises(AssertionError):
        print(c.u())
        print(c.u1())
        print(c.u2())
        assert c.u() == 5
        assert c.u1() == 5
        assert c.u2() == 5

