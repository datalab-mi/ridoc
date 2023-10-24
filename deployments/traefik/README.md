
# Reverse proxy traefik for test
[base tuto](https://doc.traefik.io/traefik/user-guides/crd-acme/)

LoadBalancer services turned to ClusterIp to begin small

## Install custom ressources for traefik v2
```bash
# Install Traefik Resource Definitions:
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.9/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml

# Install RBAC for Traefik:
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.9/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```
## Deploy traefik stuffs

```bash
kubectl apply -f .
```

Forward traefik dashboard service
```bash
 kubectl port-forward service/traefik-dashboard-service 8080:8080
 ```

 Forward traefik service
 ```bash
  kubectl port-forward service/traefik 8000:80
  ```

:tada:  [test](http://localhost:8000) frontend !

## Add client certificate to paranoid mode !

Reproduce [base tuto](https://www.nerdieworks.nl/posts/client-certificate-authentication-with-traefik/)

## Links

Twincity [old backend](https://github.com/twin-city/infra/blob/main/traefik/03-deployment.yaml)

# Alternative installation with Helm 

```bash
helm upgrade --install --values deployments/traefik/values.yaml traefik traefik/traefik --namespace traefik
```

Plus besoin de gérer les certificats https car on utilise ceux du neud kube.

