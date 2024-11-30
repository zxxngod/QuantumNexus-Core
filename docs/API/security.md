# Security API

The Security API provides features for managing security protocols, including encryption and identity verification.

## Endpoints

### 1. Generate Quantum Key Pair

**POST** `/api/security/keys/generate`

**Response:**
```json
1 {
2   "public_key": "generated_public_key",
3   "private_key": "generated_private_key"
4 }
```

2. Encrypt Data
**POST** /api/security/encrypt

Request Body:

```json
1 {
2   "data": "sensitive data here",
3   "public_key": "recipient_public_key"
4 }
```
Response:

```json
1 {
2   "encrypted_data": "encrypted_data_here"
3 }
```

### 3. Decrypt Data
**POST** /api/security/decrypt

Request Body:

```json
1 {
2   "encrypted_data": "encrypted_data_here",
3   "private_key": "your_private_key"
4 }
```

Response:

```json
1 {
2   "decrypted_data": "sensitive data here"
3 }
```
**Examples**
Generate a Quantum Key Pair
```bash
1 curl -X POST https://api.quantumnexus.com/api/security/keys/generate \
2 -H "Authorization: Bearer YOUR_API_KEY"
```

**Error Handling**
The API will return appropriate error messages for invalid requests.

**Example**:

```json
1 {
2   "error": "Invalid public key",
3   "code": 400
4 }
```
