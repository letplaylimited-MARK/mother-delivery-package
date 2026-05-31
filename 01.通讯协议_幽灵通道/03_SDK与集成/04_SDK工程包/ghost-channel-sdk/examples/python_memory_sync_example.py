import asyncio

from ghost_channel_sdk import GhostChannelSDK


async def main() -> None:
    sdk = GhostChannelSDK()
    result = await sdk.sync_memory_delta(
        source_role="secretary_v1",
        target_role="researcher_v1",
        old_state={"__version__": "v1"},
        new_state={"__version__": "v2"},
        semantic_filter="protocol scope",
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
