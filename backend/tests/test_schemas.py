import sys
sys.path.insert(0, 'D:\\Mimo\\ai-gateway')

from backend.api.schemas import (
    Message, ChatCompletionRequest, Usage, ChatCompletionResponse,
    Choice, ChatCompletionChunk, ChunkChoice, ModelInfo, ModelList
)
from pydantic import ValidationError

errors = 0

# Test 1: All imports work
print("Test 1: All imports... PASS")

# Test 2: Message validation
msg = Message(role='user', content='Hello')
assert msg.role == 'user'
assert msg.content == 'Hello'
print("Test 2: Message creation... PASS")

# Test 3: Message with invalid role
try:
    Message(role='invalid', content='Hello')
    print("Test 3: Message invalid role... FAIL")
    errors += 1
except ValidationError:
    print("Test 3: Message invalid role rejected... PASS")

# Test 4: ChatCompletionRequest
req = ChatCompletionRequest(model='gpt-4', messages=[msg])
assert req.stream is False
assert req.temperature is None
print("Test 4: ChatCompletionRequest... PASS")

# Test 5: Temperature validation
try:
    ChatCompletionRequest(model='gpt-4', messages=[msg], temperature=3)
    print("Test 5: Temperature > 2... FAIL")
    errors += 1
except ValidationError:
    print("Test 5: Temperature > 2 rejected... PASS")

# Test 6: top_p validation
try:
    ChatCompletionRequest(model='gpt-4', messages=[msg], top_p=1.5)
    print("Test 6: top_p > 1... FAIL")
    errors += 1
except ValidationError:
    print("Test 6: top_p > 1 rejected... PASS")

# Test 7: max_tokens validation
try:
    ChatCompletionRequest(model='gpt-4', messages=[msg], max_tokens=0)
    print("Test 7: max_tokens < 1... FAIL")
    errors += 1
except ValidationError:
    print("Test 7: max_tokens < 1 rejected... PASS")

# Test 8: Usage
usage = Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15)
assert usage.total_tokens == 15
print("Test 8: Usage... PASS")

# Test 9: ChatCompletionResponse
resp = ChatCompletionResponse(
    id='test-123',
    created=1234567890,
    model='gpt-4',
    choices=[Choice(index=0, message=Message(role='assistant', content='Hi'))],
    usage=usage
)
assert resp.object == 'chat.completion'
print("Test 9: ChatCompletionResponse... PASS")

# Test 10: Choice
ch = Choice(index=0, message=Message(role='assistant', content='Hi'), finish_reason='stop')
assert ch.finish_reason == 'stop'
print("Test 10: Choice... PASS")

# Test 11: ChatCompletionChunk
chunk = ChatCompletionChunk(
    id='test-456',
    created=1234567890,
    model='gpt-4',
    choices=[ChunkChoice(index=0, delta={'role': 'assistant', 'content': 'Hi'})]
)
assert chunk.object == 'chat.completion.chunk'
print("Test 11: ChatCompletionChunk... PASS")

# Test 12: ChunkChoice
cc = ChunkChoice(index=0, delta={'content': 'world'}, finish_reason='length')
assert cc.finish_reason == 'length'
print("Test 12: ChunkChoice... PASS")

# Test 13: ModelInfo
mi = ModelInfo(id='gpt-4', created=1234567890, owned_by='openai')
assert mi.object == 'model'
print("Test 13: ModelInfo... PASS")

# Test 14: ModelList
ml = ModelList(data=[mi])
assert ml.object == 'list'
print("Test 14: ModelList... PASS")

# Test 15: Empty model list
ml_empty = ModelList(data=[])
assert len(ml_empty.data) == 0
print("Test 15: Empty ModelList... PASS")

print(f"\n{'='*40}")
if errors == 0:
    print(f"All 15 tests PASSED")
else:
    print(f"{errors} tests FAILED")
    sys.exit(1)
