# importing librarries
import datetime
from difflib import diff_bytes
import hashlib
import json
from xmlrpc.client import NOT_WELLFORMED_ERROR
from flask import Flask,jsonify,request


# Structuring the blockchain
class Blockchain:


    # Genesis block creation
    def __init__(self):
        self.chain=[]
        self.create_block(owner="creater",reg_no='007',proof=0,previous_hash='0')

    # create block
    def create_block(self,owner,reg_no,proof,previous_hash):
        block={'owner':owner,'reg_no':reg_no,
                'index':len(self.chain)+1 ,
                'timestamp':str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash
              }    
        self.chain.append(block)
        return block

    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False

        while check_proof is False:
            hash_value=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_value[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1    

        return new_proof
    def hash(self,block):
        # json.dums is use to convert dictionary to strings
         encoded_block=json.dumps(block).encode()
         return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1

        while block_index < len(chain):
            block=chain[block_index]
            if block['previous_hash']!=self.hash(previous_block):
                return False
            
            previous_proof=previous_block['proof']
            proof=block['proof']

            hash_value=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_value[:4]!='0000':
                # Block is tempered
                return False
            previous_block=block
            block_index+=1 
        return True   

    def get_last_block(self):
       return self.chain[-1]       
     

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)
  
   
    