# Governance API

The Governance API allows you to manage decentralized governance structures, including DAOs and voting mechanisms.

## Endpoints

### 1. Create DAO```markdown
**POST** `/api/governance/daos`

**Request Body:**
```json
1 {
2   "name": "DAOName",
3   "description": "Description of the DAO",
4   "members": ["member1", "member2"]
5 }
```

**Response**:

```json
1 {
2   "dao_id": "unique_dao_id",
3   "status": "created"
4 }
```

### 2. Submit Vote
**POST** /api/governance/daos/{dao_id}/vote

Request Body:

```json
1 {
2   "proposal_id": "unique_proposal_id",
3   "vote": "yes" // or "no"
4 }
```

**Response**:

```json
1 {
2   "vote_id": "unique_vote_id",
3   "status": "voted"
4 }
```

### 3. Get DAO Details
**GET** /api/governance/daos/{dao_id}

**Response**:

```json
1 {
2   "dao_id": "unique_dao_id",
3   "name": "DAOName",
4   "description": "Description of the DAO",
5   "members": ["member1", "member2"],
6   "proposals": [
7     {
8       "proposal_id": "unique_proposal_id",
9       "title": "Proposal Title",
10       "status": "active"
11     }
12   ]
13 }
```

**Error Handling**
The API will return appropriate error messages for invalid requests.

**Example**:

```json
1 {
2   "error": "Invalid member ID",
3   "code": 400
4 }
```

