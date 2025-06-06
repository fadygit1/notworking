from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.script import Script

def main():
    # setup the network
    setup('testnet')

    
    # Generate some test private keys and their corresponding uncompressed addresses
    test_keys = [
        '0000000000000000000000000000000000000000000000000000000000000001',
        '0000000000000000000000000000000000000000000000000000000000000002',
        '0000000000000000000000000000000000000000000000000000000000000003',
        '0000000000000000000000000000000000000000000000000000000000000004',
        '0000000000000000000000000000000000000000000000000000000000000005',
    ]
    
    print("Private Key (hex) | Uncompressed Address")
    print("-" * 60)
    
    for priv_key_hex in test_keys:
        # Create private key from hex
        priv_key = PrivateKey(secret_exponent=int(priv_key_hex, 16))
        
        # Get the public key (uncompressed)
        pub_key = priv_key.get_public_key()
        
        # Get the address (uncompressed)
        address = pub_key.get_address()
        
        print(f"{priv_key_hex} | {address.to_string()}")

if __name__ == "__main__":
    main()
