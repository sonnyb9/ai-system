from controller.context import ContextManager


def test_context_manager_adds_messages():
    context = ContextManager(max_messages=5)
    context.add_message("user", "hello")
    context.add_message("assistant", "hi")

    messages = context.get_messages()
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_context_manager_prunes_old_messages():
    context = ContextManager(max_messages=3)
    for i in range(5):
        context.add_message("user", f"msg {i}")

    assert len(context) == 3
    assert context.get_last_message()["content"] == "msg 4"
