# Smart Contracts API

The Smart Contracts API allows you to create, deploy, and manage smart contracts on the QuantumNexus platform.

## Endpoints

### 1. Create Smart Contract

**POST** `/api/smart_contracts`

**Request Body:**

```json
1 {
2   "name": "ContractName",
3   "code": "contract code here",
4   "parameters": {
5     "param1": "value1",
6     "param2": "value2"
7   }
8 }
```

**Response**:

```json
1 {
2   "contract_id": "unique_contract_id",
3   "status": "created"
4 }
```

### 2. Deploy Smart Contract
**POST** /api/smart_contracts/{contract_id}/deploy

**Response**:

```json
1 {
2   "transaction_id": "unique_transaction_id",
3   "status": "deployed"
4 }
```

### 3. Get Smart Contract Details
**GET** /api/smart_contracts/{contract_id}

**Response**:

```json
1 {
2   "contract_id": "unique_contract_id",
3   "name": "ContractName",
4   "code": "contract code here",
5   "status": "active"
6 }
```
## Examples
Create and Deploy a Smart Contract

```bash
1 curl -X POST https://api.quantumnexus.com/api/smart_contracts \
2 -H "Authorization: Bearer YOUR_API_KEY" \
3 -H "Content-Type: application/json" \
4 -d '{
5   "name": "MyContract",
6   "code": "contract code here",
7   "parameters": {}
8 }'
```

### Error Handling
In case of an error, the API will return an appropriate HTTP status code along with an error message.

**Example**:

```json
1 {
2   "error": "Invalid contract code",
3   "code": 400
4 }
```

