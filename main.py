import asyncio
from web3 import Web3

# Put your RPC link from provider
ETHEREUM_NODE_URL = "https://rpc.rpc/" 

# Enter the gwei ammount at which you would like to perform the transaction
GWEI = 20 

# Put price that you want to bridge
eth_quantity_to_bridge = 0.001 

# Put your private keys as shown => 'yourprivate',
PRIVATE_KEYS = ['privatekey',
                'privatekey',
                'privatekey',
                ]

w3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE_URL))

CONTRACT_ABI = [{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EthWithdrawalFinalized","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"txId","type":"uint256"},{"indexed":False,"internalType":"bytes32","name":"txHash","type":"bytes32"},{"indexed":False,"internalType":"uint64","name":"expirationTimestamp","type":"uint64"},{"components":[{"internalType":"uint256","name":"txType","type":"uint256"},{"internalType":"uint256","name":"from","type":"uint256"},{"internalType":"uint256","name":"to","type":"uint256"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"uint256","name":"gasPerPubdataByteLimit","type":"uint256"},{"internalType":"uint256","name":"maxFeePerGas","type":"uint256"},{"internalType":"uint256","name":"maxPriorityFeePerGas","type":"uint256"},{"internalType":"uint256","name":"paymaster","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256[4]","name":"reserved","type":"uint256[4]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256[]","name":"factoryDeps","type":"uint256[]"},{"internalType":"bytes","name":"paymasterInput","type":"bytes"},{"internalType":"bytes","name":"reservedDynamic","type":"bytes"}],"indexed":False,"internalType":"struct IMailbox.L2CanonicalTransaction","name":"transaction","type":"tuple"},{"indexed":False,"internalType":"bytes[]","name":"factoryDeps","type":"bytes[]"}],"name":"NewPriorityRequest","type":"event"},{"inputs":[{"internalType":"uint256","name":"_l2BlockNumber","type":"uint256"},{"internalType":"uint256","name":"_l2MessageIndex","type":"uint256"},{"internalType":"uint16","name":"_l2TxNumberInBlock","type":"uint16"},{"internalType":"bytes","name":"_message","type":"bytes"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"}],"name":"finalizeEthWithdrawal","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"uint256","name":"_l2GasLimit","type":"uint256"},{"internalType":"uint256","name":"_l2GasPerPubdataByteLimit","type":"uint256"}],"name":"l2TransactionBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_l2TxHash","type":"bytes32"},{"internalType":"uint256","name":"_l2BlockNumber","type":"uint256"},{"internalType":"uint256","name":"_l2MessageIndex","type":"uint256"},{"internalType":"uint16","name":"_l2TxNumberInBlock","type":"uint16"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"internalType":"enum TxStatus","name":"_status","type":"uint8"}],"name":"proveL1ToL2TransactionStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_blockNumber","type":"uint256"},{"internalType":"uint256","name":"_index","type":"uint256"},{"components":[{"internalType":"uint8","name":"l2ShardId","type":"uint8"},{"internalType":"bool","name":"isService","type":"bool"},{"internalType":"uint16","name":"txNumberInBlock","type":"uint16"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"bytes32","name":"value","type":"bytes32"}],"internalType":"struct L2Log","name":"_log","type":"tuple"},{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"}],"name":"proveL2LogInclusion","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_blockNumber","type":"uint256"},{"internalType":"uint256","name":"_index","type":"uint256"},{"components":[{"internalType":"uint16","name":"txNumberInBlock","type":"uint16"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct L2Message","name":"_message","type":"tuple"},{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"}],"name":"proveL2MessageInclusion","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_contractL2","type":"address"},{"internalType":"uint256","name":"_l2Value","type":"uint256"},{"internalType":"bytes","name":"_calldata","type":"bytes"},{"internalType":"uint256","name":"_l2GasLimit","type":"uint256"},{"internalType":"uint256","name":"_l2GasPerPubdataByteLimit","type":"uint256"},{"internalType":"bytes[]","name":"_factoryDeps","type":"bytes[]"},{"internalType":"address","name":"_refundRecipient","type":"address"}],"name":"requestL2Transaction","outputs":[{"internalType":"bytes32","name":"canonicalTxHash","type":"bytes32"}],"stateMutability":"payable","type":"function"}]
CONTRACT_ADDRESS = w3.to_checksum_address('0x32400084C286CF3E17e7B677ea9583e60a000324')

zksync_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
eth_quantity = w3.to_wei(eth_quantity_to_bridge, 'ether')


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

    transaction_data = function_call.build_transaction({
        'from': wallet_address,
        'gas': 150096,
        'gasPrice': w3.to_wei(GWEI, 'gwei'),
        'nonce': w3.eth.get_transaction_count(wallet_address),
    })

    signed_transaction = w3.eth.account.sign_transaction(transaction_data, private_key)
    txn = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"***** Transaction: https://etherscan.io/tx/{txn} *****")


async def main():
    keys = {}
    for KEY in PRIVATE_KEYS:
        account = w3.eth.account.from_key(KEY)
        wallet_address = account.address
        keys[KEY] = wallet_address

    while True:
        gas_price = w3.eth.gas_price
        gwei_gas_price = w3.from_wei(gas_price, 'gwei')

        if gwei_gas_price < GWEI:
            tasks = [interact_with_contract(keys[key],key) for key in keys.keys()]
            await asyncio.gather(*tasks)

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
