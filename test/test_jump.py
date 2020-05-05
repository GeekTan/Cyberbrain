def test_jump(tracer):
    a = []
    b = "b"
    c = "c"

    tracer.init()

    if a:  # POP_JUMP_IF_FALSE
        pass  # JUMP_FORWARD
    else:
        x = 1

    if not a:  # POP_JUMP_IF_TRUE
        x = 2

    x = a != b != c  # JUMP_IF_FALSE_OR_POP
    x = a == b or c  # JUMP_IF_TRUE_OR_POP

    # TODO: Test JUMP_ABSOLUTE. This requires loop instructions to be Implemented.

    tracer.register()

    assert tracer.events == [
        {"target": "x", "value": 1, "sources": set()},
        {"target": "x", "value": 2, "sources": set()},
        # This is a known defect. We have no way to know `x` comes from `a`, because
        # the result of `a != b` only determines whether to jump to execute `b != c`.
        # I think it's fine though.
        {"target": "x", "value": True, "sources": {"b", "c"}},
        # Same defect here.
        {"target": "x", "value": "c", "sources": {"c"}},
    ]