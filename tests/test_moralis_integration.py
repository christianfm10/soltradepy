import os

import pytest

from soltradepy.services.moralis.moralis_service import MoralisService


@pytest.mark.moralis_integration
@pytest.mark.smoking
@pytest.mark.skipif(
    not pytest.config.getoption("--smoking")
    or not pytest.config.getoption("--moralis-integration"),
    reason="Skipping smoking tests unless --smoking is specified",
)
@pytest.mark.skipif(
    os.getenv("MORALIS_API_KEY") is None,
    reason="MORALIS_API_KEY environment variable not set",
)
@pytest.mark.asyncio
async def test_real_moralis_sync(session):
    api_key = os.getenv("MORALIS_API_KEY")
    if not api_key:
        print("No MORALIS_API_KEY set, skipping real Moralis test.")
        pytest.skip("No MORALIS_API_KEY set, skipping real Moralis test.")

    service = MoralisService(api_key=api_key, session=session)

    result = await service.sync_graduated_tokens(limit=2)
    print(result)

    assert result["saved"] > 0
    assert result["next_cursor"] is not None
