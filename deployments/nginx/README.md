# Install helm charts

## Nginx
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

## Cert manager
```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```
From [docs](https://cert-manager.io/docs/tutorials/acme/nginx-ingress/)

# Deploy
```bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace nginx \
  --set installCRDs=true

helm upgrade --install nginx ingress-nginx/ingress-nginx  --namespace nginx --create-namespace --values values.yaml

kubectl apply -f issuer.yaml
kubectl apply -f ingress.yaml 
```
