import json
from v_astra.provider.gateway import OptimizationGateway, optimize_request_json
from v_astra.provider.request import optimize_request

def test_unknown_fields_preserved():
    payload = {"_vastra_provider":"anthropic","model":"claude","messages":[{"role":"user","content":"hello"}],"custom_field":{"keep":True}}
    optimized, report = optimize_request(payload)
    assert optimized["custom_field"] == {"keep": True}
    assert "_vastra_provider" not in optimized
    assert report.provider == "anthropic"

def test_gateway_sender():
    seen = {}
    def sender(request):
        seen.update(request)
        return {"ok": True}
    result = OptimizationGateway(sender).send({"model":"x","messages":[{"role":"user","content":"hello"}]})
    assert result.response == {"ok": True}
    assert seen["model"] == "x"

def test_json_round_trip():
    raw = json.dumps({"model":"x","messages":[{"role":"user","content":"hello"}]})
    optimized, report = optimize_request_json(raw)
    assert json.loads(optimized)["model"] == "x"
    assert report.original_bytes > 0

def test_non_object_rejected():
    try:
        optimize_request_json("[]")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
