from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, PublicKey

def main():
    # Setup mainnet
    setup('mainnet')
    
    # Generate some test private keys and their corresponding uncompressed addresses
    test_keys = [
        '0000000000000000000000000000000000000000000000000000000000000001',
        '0000000000000000000000000000000000000000000000000000000000000002',
        '0000000000000000000000000000000000000000000000000000000000000003',
        '0000000000000000000000000000000000000000000000000000000000000004',
        '0000000000000000000000000000000000000000000000000000000000000005',
        '0000000000000000000000000000000000000000000000000000000000000006',
        '0000000000000000000000000000000000000000000000000000000000000007',
        '0000000000000000000000000000000000000000000000000000000000000008',
        '0000000000000000000000000000000000000000000000000000000000000009',
        '000000000000000000000000000000000000000000000000000000000000000A',
    ]
    
    print("Private Key (hex) | Uncompressed Address")
    print("-" * 60)
    
    for priv_key_hex in test_keys:
        # Create private key from hex
        priv_key = PrivateKey(secret_exponent=int(priv_key_hex, 16))
        
        # Get the public key (uncompressed)
        pub_key = priv_key.get_public_key()
        
        # Get the address (uncompressed)
        address = pub_key.get_address(compressed=False)
        
        print(f"{priv_key_hex} | {address.to_string()}")
        
        # Also print the first few addresses for testing
        if len(priv_key_hex) <= 10:  # Only print first few for brevity
            print(f"  First few addresses starting with {address.to_string()[:3]}")
            for i in range(3):
                test_key = PrivateKey(secret_exponent=int(priv_key_hex, 16) + i + 1)
                test_pub = test_key.get_public_key()
                test_addr = test_pub.get_address(compressed=False)
                print(f"  {test_addr.to_string()}")

if __name__ == "__main__":
    main()
