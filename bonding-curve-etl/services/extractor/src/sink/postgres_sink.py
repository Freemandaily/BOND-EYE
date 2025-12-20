import os
import time
from psycopg2 import pool
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class PostgresSink:
    def __init__(self, dsn=None, minconn=1, maxconn=5):
        if dsn is None:
            user = os.getenv("POSTGRES_USER", "freeman")
            password = os.getenv("POSTGRES_PASSWORD", 1234)
            host = os.getenv("POSTGRES_HOST", "postgres")
            port = os.getenv("POSTGRES_PORT", 5432)
            db = os.getenv("POSTGRES_DB", "Extractor_db")
            dsn = f"dbname={db} user={user} password={password} host={host} port={port}"
        self.pool = pool.ThreadedConnectionPool(minconn, maxconn, dsn)



    def insert_token_creations(self, rows: List[Dict]):
        if not rows:
            return
        
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                for r in rows:
                    cur.execute("""
                        INSERT INTO token_creations (token_address, deployer_address, pool,
                                tx_hash,block_number,block_timestamp,name,
                                virtualMon,virtualToken,targetTokenAmount,token_description,
                                website,twitter,telegram,image_url,symbol
                                )
                        VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)
                        ON CONFLICT (token_address) DO UPDATE SET
                        deployer_address = EXCLUDED.deployer_address,
                        pool = EXCLUDED.pool,
                        block_number = EXCLUDED.block_number,
                        tx_hash = EXCLUDED.tx_hash;
                    """, (r.get('token_address'), r.get('deployer_address'), r.get('pool'), 
                          r.get('tx_hash'), 
                          str(r.get('block_number')), str(r.get('block_timestamp')),
                          r.get('name'),r.get('virtualMon'),r.get('virtualToken'),
                          str(r.get('targetTokenAmount')),r.get('token_description'),r.get('website'),
                          r.get('twitter'),r.get('telegram'),r.get('image_url'),r.get('symbol')
                          ))
            conn.commit()
            print("Inserted/Updated token creations successfully.")
            time.sleep(3)
        except Exception as e:
            print("PostgresSink insert_token_creations error:", e)
        # finally:
        #     self.pool.putconn(conn)

    def insert_token_trades(self, rows: List[Dict]):
        if not rows:
            return 
        
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                for r in rows:
                    cur.execute("""
                        INSERT INTO token_trades (token_address, trader, amount_in,amount_out, trade_direction, tx_hash, block_number,block_timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s,%s,%s)
                        ON CONFLICT (tx_hash) DO UPDATE SET
                        trader = EXCLUDED.trader,
                        trade_direction = EXCLUDED.trade_direction,
                        block_number = EXCLUDED.block_number,
                        tx_hash = EXCLUDED.tx_hash;
                    """, (r.get('token_address'), r.get('trader'), str(r.get('amount_out')),str(r.get('amount_out')), r.get('trade_direction'), r.get('tx_hash'), str(r.get('block_number')), str(r.get('block_timestamp'))))
            conn.commit()
            print("Inserted/Updated token trades successfully.")
            time.sleep(2)
        except Exception as e:
            print("PostgresSink insert_token_trades error:", e)
        # finally:
        #     self.pool.putconn(conn)

    def close(self):
        self.pool.closeall()