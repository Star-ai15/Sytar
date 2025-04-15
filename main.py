
import os, base64, json, asyncio, aiohttp, time
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.publickey import PublicKey
from spl.token.async_client import AsyncToken

RPC_URL = "https://api.mainnet-beta.solana.com"
PRESALE_SK = base64.b64decode(os.environ["PRESALE_SECRET"])
PRESALE_KP = Keypair.from_secret_key(PRESALE_SK)
PRESALE_ADDR = PRESALE_KP.public_key
STAR_MINT = PublicKey("7Hajt3Yc7MQhWwNsUAxdUgcLH7M59u1bDpZ79E5Zkmat")
STAR_PER_SOL = 300000000/700  # example ratio

async def main():
    client = AsyncClient(RPC_URL)
    token = AsyncToken(client, STAR_MINT, PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"), PRESALE_KP)
    processed=set()
    while True:
        sigs = (await client.get_signatures_for_address(PRESALE_ADDR, limit=20)).value
        for s in sigs:
            if s.signature in processed or s.err: continue
            tx = await client.get_transaction(s.signature)
            sender = tx.transaction.message.account_keys[0]
            sol_in = (tx.meta.post_balances[0]-tx.meta.pre_balances[0])/1e9
            if sol_in<=0: continue
            star_amt = int(sol_in*STAR_PER_SOL*1_000_000)
            ix = await token.transfer(PRESALE_ADDR, sender, PRESALE_ADDR, star_amt, 6)
            print("Airdropped", star_amt, "STAR to", sender)
            processed.add(s.signature)
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(main())
