#!/bin/bash

name_to_delete="pre-install-kibana-kibana"
namespace="ridoc"
# Get a list of available resource types
resource_types=$(kubectl api-resources --verbs=list -o name | cut -d / -f 2)
kubectl delete configmaps kibana-kibana-helm-scripts -n ridoc
kubectl delete -n ridoc secrets kibana-kibana-es-token
kubectl delete pods --field-selector status.phase=Failed -n ridoc
kubectl delete -n ridoc deployment kibana-kibana

for resource in $resource_types; do
    # List resources with the specified name
    resource_list=$(kubectl get $resource -n $namespace --field-selector metadata.name=$name_to_delete --ignore-not-found=true --output=custom-columns=:.metadata.name --no-headers)
    if [ -n "$resource_list" ]; then
        # Delete resources with the specified name
        echo "Delete $resource $resource_list"
        kubectl delete $resource -n $namespace --field-selector metadata.name=$name_to_delete --ignore-not-found=true
    fi
done
