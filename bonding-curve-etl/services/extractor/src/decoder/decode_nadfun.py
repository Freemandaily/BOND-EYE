from typing import List
import aiohttp

class decode_nadfun:
    def __init__(self):
        self.session = None
        self.create_topic = '0xd37e3f4f651fe74251701614dbeac478f5a0d29068e87bbe44e5026d166abca9'
        self.buy_topic = '0x00a7ba871905cb955432583640b5c9fc6bdd27d36884ab2b5420839224638862'
        self.sell_topic = '0x0eb25df0e2137de8ce042eeaf39080d25f0c8d451372c99db69a4c0a298d0fa1'


    async def decode_for_token_creation(self,log_data:List[dict])->dict:
        # sys.exit()
        """
        Decodes log data to extract token creation details.
        Args:
            log_data (List[dict]): List of log entries.
        Returns:
            dict: A dictionary containing deployer_address, token_address, and fee_reciever, deployer_bought_amount.
        """
        if not log_data:
            return 
        
        token_creation_data = []
        for log in log_data:
            topics = [str(topic).lower() for topic in log.get('topics',[])]
            if topics and topics[0] == self.create_topic.lower():
                deployer_address =  topics[1][24:]
                token_address =  topics[2][24:]
                pool =  topics[3][24:]
                
                data_hex = log.get('data','0x')
                decoded_data = await self.decode_payload(bytes.fromhex(data_hex[2:]))
                new_token_data = {
                    'deployer_address':'0x'+ deployer_address,
                    'token_address':'0x'+ token_address,
                    'pool':'0x'+ pool,
                    'tx_hash':  log.get('transactionHash'),
                    'block_number': int(log.get('blockNumber'),16),
                    'block_timestamp': int(log.get('blockTimestamp','0'),16)
                }
                new_token_data.update(decoded_data)
                token_creation_data.append(new_token_data)


            # if topics and '0x' + topics[0] == self.buy_topic.lower():
            #     for crxt_data in token_creation_data:
            #         if crxt_data.get('token_address').lower() == '0x' + topics[2][24:] and crxt_data.get('tx_hash').lower() == '0x' + log.get('transactionHash').hex().lower():
            #             data_hex = log.get('data','0x').hex()
            #             datas = [data_hex[i:i+64] for i in range(0, len(data_hex), 64)]
            #             amount = int(datas[0],16)
            #             crxt_data.update(
            #                 {'deployer_bought_amount': str(amount)}
            #             )
            #             token_creation_data.remove(crxt_data)
            #             token_creation_data.append(crxt_data)
    
        return token_creation_data

    async def decode_payload(self,data: bytes):
        """
        Decode ABI-encoded payload for:
        - 3 dynamic strings: name, symbol, tokenURI
        - 3 uint256: virtualMon, virtualToken, targetTokenAmount
        """
        # Each slot is 32 bytes
        def read_uint256(offset):
            return int.from_bytes(data[offset:offset+32], "big")

        def read_string(offset):
            # Read the offset to string data
            str_offset = read_uint256(offset)
            # Read length of the string
            str_len = read_uint256(str_offset)
            # Read actual string bytes
            str_bytes = data[str_offset + 32 : str_offset + 32 + str_len]
            return str_bytes.decode("utf-8")

        # Decode dynamic strings
        name = read_string(0)      # slot 0
        symbol = read_string(32)   # slot 1
        tokenURI = read_string(64) # slot 2

        # Decode uint256 values
        virtualMon = read_uint256(96)          # slot 3
        virtualToken = read_uint256(128)       # slot 4
        targetTokenAmount = read_uint256(160)  # slot 5


        token_description = 'NadFun Token'
        website = 'https//:nad.fun'
        twitter = 'None'
        telegram = 'None'
        image_url = 'None'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=tokenURI) as response:

                if response.status == 200:
                    result = await response.json()
                    # print(json.dumps(result,indent=4))
                    token_description = result.get('description')
                    website = result.get('website','')
                    twitter = result.get('twitter','')
                    telegram = result.get('telegram')
                    image_url = result.get('image_uri')

        return {
            "name": name,
            "symbol": symbol,
            "tokenURI": tokenURI,
            "virtualMon": virtualMon,
            "virtualToken": virtualToken,
            "targetTokenAmount": targetTokenAmount,
            'token_description' : token_description, 
            'website': website ,
            'twitter' : twitter,
            'telegram': telegram, 
            'image_url' : image_url
        }


    async def decode_for_token_exchange(self,log_data:List[dict])->List[dict]:
        """
        Decodes log data to extract token purchase details.
        Args:
            log_data (List[dict]): List of log entries.
        Returns:
            dict: A dictionary containing purchaser_address, token_address, and purchase_amount.
        """
        if not log_data:
            return 
        
        token_exchange_data = []
        for log in log_data:
            topics = [str(topic) for topic in log.get('topics',[])]
            if topics and topics[0].lower() == self.buy_topic.lower():
                purchaser_address = topics[1][24:]
                token_address = topics[2][24:]
                data_hex = log.get('data','0x')
                datas = [data_hex[i:i+64] for i in range(0, len(data_hex), 64)]
                amount_in = int(datas[0],16)
                amount_out = int(datas[1],16)
                token_exchange_data.append({
                    'trader':'0x'+ purchaser_address,
                    'token_address':'0x'+ token_address,
                    'amount_in':str(amount_in),
                    'amount_out':str(amount_out),
                    'trade_direction':'buy',
                    'tx_hash': log.get('transactionHash'),
                    'block_number':int(log.get('blockNumber'),16),
                    'block_timestamp': int(log.get('blockTimestamp','0'),16)
                })
            if topics and topics[0].lower() == self.sell_topic.lower():
                seller_address =  topics[1][24:]
                token_address =  topics[2][24:]
                data_hex = log.get('data','0x')
                datas = [data_hex[i:i+64] for i in range(0, len(data_hex), 64)]
                amount_in = int(datas[0],16)
                amount_out = int(datas[1],16)
                token_exchange_data.append({
                    'trader':'0x'+seller_address,
                    'token_address':'0x'+token_address,
                    'amount_in':str(amount_in),
                    'amount_out': str(amount_out),
                    'trade_direction':'sell',
                    'tx_hash': log.get('transactionHash'),
                    'block_number': int(log.get('blockNumber'),16),
                    'block_timestamp': int(log.get('blockTimestamp','0'),16)
                })
        if token_exchange_data:
            print(f" Decoded {len(token_exchange_data)} token exchange entries.")
        return token_exchange_data
    


    


        