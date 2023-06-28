# Sample Test App for Outbound API call

Testing if outbound ip address could be fixed with NAT Gateway.

## Pre-requisites
* Resource group

## Deploying external API app

This demo used Azure App Service with `Python 3.11` runtime.

Deploy external-api with `SCM_DO_BUILD_DURING_DEPLOYMENT` set to `1` & `pip install -r requirements.txt && python -m uvicorn main:app --host 0.0.0.0` as startup command.

After deployment, try `curl <YOUR_URL>` to see if it works.
It needs to reply with `{"message":"Hello World"}`.

## Running in local

Update `main.py` request url to the external api app.

```python
response = requests.get(<YOUR_URL>)
```

```bash
cd api-call-app
docker build -t outbound-test-app .
docker run -p 80:80 outbound-test-app
```
Go to `localhost:80` in browser.

Press `Click me` button to see `Hello World`.

## Upload the image to Azure Container Registry

1. Create Azure Container Registry
```bash
az acr create --resource-group myResourceGroup --name <acrName> --sku Basic
```

2. Login to the registry
```bash
az acr login --name <acrName>
```

3. Get ACR server name.
```bash
az acr list --resource-group myResourceGroup --query "[].{acrLoginServer:loginServer}" --output table
```

4. Change the image name & tag
```bash
docker tag outbound-test-app <acrLoginServer>/outbound-test-app:v1
```

5. Push images to registry
```bash
docker push <acrLoginServer>/outbound-test-app:v1
```

## Deploying to Azure Kubernets Service
1. Create AKS
```bash
az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1 --enable-addons monitoring --generate-ssh-keys --attach-acr <acrName>
```

2. Get AKS credentials
```bash
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```
3. Update manifest file
```bash
vi outbound-test-app.yaml
```
Replace image name with your ACR image name.
```yaml
containers:
      - name: outbound-test-app
        image: <acrLoginServer>/outbound-test-app:v1
```

4. Deploy app
```bash
kubectl apply -f outbound-test-config.yml
``` 
