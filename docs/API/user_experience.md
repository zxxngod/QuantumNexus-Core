# User Experience API

The User Experience API focuses on enhancing the interaction and satisfaction of users within the QuantumNexus ecosystem.

## Endpoints

### 1. Collect User Feedback

**POST** `/api/user_experience/feedback`

**Request Body:**
```json
1 {
2   "user_id": "unique_user_id",
3   "feedback": "User feedback here",
4   "rating": 5 // rating out of 5
5 }
```

**Response**:

```json
1 {
2   "feedback_id": "unique_feedback_id",
3   "status": "submitted"
4 }
```

### 2. Get User Experience Metrics
**GET** /api/user_experience/metrics/{user_id}

**Response**:

```json
1 {
2   "user_id": "unique_user_id",
3   "satisfaction_score": 85, // out of 100
4   "feedback_count": 10
5 }
```

**Examples**
Submit User Feedback
```bash
1 curl -X POST https://api.quantumnexus.com/api/user_experience/feedback \
2 -H "Authorization: Bearer YOUR_API_KEY" \
3 -H "Content-Type: application/json" \
4 -d '{
5   "user_id": "user123",
6   "feedback": "Great experience!",
7   "rating": 5
8 }'
```

**Error Handling**
The API will return appropriate error messages for invalid requests.

**Example**:

```json
1 {
2   "error": "Feedback submission failed",
3   "code": 400
4 }
```
