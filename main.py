```python
import asyncio
from web3 import Web3

# Your RPC link from provider
ETHEREUM_NODE_URL = "https://rpc.rpc/"

# Gwei amount for the transaction
GWEI = 20 

# Amount to bridge
eth_quantity_to_bridge = 0.001 

# Your private keys
PRIVATE_KEYS = ['privatekey1', 'privatekey2', 'privatekey3']

w3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE_URL))

CONTRACT_ABI = [
    # Contract ABI here
]

CONTRACT_ADDRESS = w3.toChecksumAddress('0x32400084C286CF3E17e7B677ea9583e60a000324')

zksync_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
eth_quantity = w3.toWei(eth_quantity_to_bridge, 'ether')

async def interact_with_contract(wallet_address, private_key):
    contract_address_l2 = wallet_address
    l2_value = eth_quantity
    calldata = b''
    l2_gas_limit = 733664
    l2_gas_per_pubdata_byte_limit = 800
    factory_deps = []
    refund_recipient = wallet_address

    function_call = zksync_contract.functions.requestL2Transaction(
        contract_address_l2,
        l2_value,
        calldata,
        l2_gas_limit,
        l2_gas_per_pubdata_byte_limit,
        factory_deps,
        refund_recipient
    )

    transaction_data = function_call.buildTransaction({
        'from': wallet_address,
        'gas': 150096,
        'gasPrice': w3.toWei(GWEI, 'gwei'),
        'nonce': w3.eth.getTransactionCount(wallet_address),
    })

    signed_transaction = w3.eth.account.signTransaction(transaction_data, private_key)
    txn = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print(f"***** Transaction: https://etherscan.io/tx/{txn.hex()} *****")

async def main():
    accounts = {}
    for KEY in PRIVATE_KEYS:
        account = w3.eth.account.from_key(KEY)
        wallet_address = account.address
        accounts[account] = wallet_address

    while True:
        gas_price = w3.eth.gasPrice
        gwei_gas_price = w3.fromWei(gas_price, 'gwei')

        if gwei_gas_price < GWEI:
            tasks = [interact_with_contract(accounts[account], KEY) for account, KEY in accounts.items()]
            await asyncio.gather(*tasks)

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
```
