import pytest

from vyper.compiler import compile_code
from vyper.compiler.settings import OptimizationLevel, Settings
from vyper.exceptions import StaticAssertionException

code = """
@external
def foo():
    assert 1 == 2
"""


@pytest.mark.parametrize("use_venom", [True, False], ids=["venom", "legacy"])
def test_no_static_assert(use_venom, get_contract, tx_failed):
    # without the flag, compile_code should raise StaticAssertionException
    settings = Settings(optimize=OptimizationLevel.GAS, experimental_codegen=use_venom)
    with pytest.raises(StaticAssertionException):
        compile_code(code, output_formats=["bytecode"], settings=settings)

    # with the flag, it should compile but revert at runtime
    settings = Settings(
        optimize=OptimizationLevel.GAS,
        experimental_codegen=use_venom,
        no_static_assert=True,
    )
    c = get_contract(code, compiler_settings=settings)
    with tx_failed():
        c.foo()


div_by_zero_code = """
@external
def foo() -> uint256:
    x: uint256 = 0
    return 1 / x
"""


def test_no_static_assert_div_by_zero(get_contract, tx_failed):
    # without the flag, compile_code should raise StaticAssertionException
    settings = Settings(optimize=OptimizationLevel.GAS, experimental_codegen=True)
    with pytest.raises(StaticAssertionException):
        compile_code(div_by_zero_code, output_formats=["bytecode"], settings=settings)

    # with the flag, it should compile but revert at runtime
    settings = Settings(
        optimize=OptimizationLevel.GAS,
        experimental_codegen=True,
        no_static_assert=True,
    )
    c = get_contract(div_by_zero_code, compiler_settings=settings)
    with tx_failed():
        c.foo()
