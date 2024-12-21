from vyper import compile_code

def test_value_kw(get_contract):
    src = """
@external
@payable
def foo(_target: address) -> Bytes[32]:
    response: Bytes[32] = raw_call(_target, method_id("someMethodName()"), max_outsize=32, value=msg.value)
    return response

@external
@payable
def bar(_target: address) -> Bytes[32]:
    success: bool = False
    response: Bytes[32] = b""
    x: uint256 = 123
    success, response = raw_call(
        _target,
        abi_encode(x, method_id=method_id("someMethodName(uint256)")),
        max_outsize=32,
        value=msg.value,
        is_delegate_call=True,
        revert_on_failure=False
        )
    assert success
    return response
    """

    assert compile_code(src) is not None