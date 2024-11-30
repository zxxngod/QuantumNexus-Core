# Deploying on Quantum Nexus

This tutorial will guide you through the process of deploying your application on the Quantum Nexus platform.

## Step 1: Prepare Your Application

Ensure your application is ready for deployment. This includes:

- Finalizing your smart contracts.
- Testing your application thoroughly.

## Step 2: Configure Deployment Settings

Create a deployment configuration file, e.g., `deploy.json`:

```json
1 {
2   "contract_id": "your_contract_id",
3   "network": "quantum_nexus",
4   "settings": {
5     "gas_limit": 3000000,
6     "value": 0
7   }
8 }
```

## Step 3: Deploy Your Application
Use the deployment command to deploy your application:

```bash
1 nexus deploy --config deploy.json
```

## Step 4: Verify Deployment
After deployment, verify that your application is running correctly:

```bash
1 curl -X GET https://api.quantumnexus.com/api/smart_contracts/{contract_id}
```

## Conclusion
Your application is now deployed on Quantum Nexus! Refer to the API documentation for further interactions.
