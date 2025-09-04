# Basic Kubernetes deployment

Using minikube, create a cluster by using `minikube start`.

Verify that the cluster has been created using `kubectl get nodes`, the command line output should look like this:

```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   37s   v1.33.1
```

To get a more detailed look at the individual pods use `kubectl get pods -A`

```
NAMESPACE     NAME                               READY   STATUS    RESTARTS     AGE
kube-system   coredns-674b8bbfcf-k2mhc           1/1     Running   0            39s
kube-system   etcd-minikube                      1/1     Running   0            44s
kube-system   kube-apiserver-minikube            1/1     Running   0            45s
kube-system   kube-controller-manager-minikube   1/1     Running   0            44s
kube-system   kube-proxy-rcpl2                   1/1     Running   0            39s
kube-system   kube-scheduler-minikube            1/1     Running   0            44s
kube-system   storage-provisioner                1/1     Running   1 (8s ago)   43s
```

Now to setup a deployment on the created clutser, run `kubectl apply -f deployment/nginx-deployment.yaml`. This applies the configuration yaml file found in the deployment folder to launch an nginx server across three pods.

```
NAMESPACE     NAME                                READY   STATUS    RESTARTS        AGE
default       nginx-deployment-647677fc66-cjk7c   1/1     Running   0               29s
default       nginx-deployment-647677fc66-kvffx   1/1     Running   0               29s
default       nginx-deployment-647677fc66-ts2nn   1/1     Running   0               29s
kube-system   coredns-674b8bbfcf-k2mhc            1/1     Running   0               7m52s
kube-system   etcd-minikube                       1/1     Running   0               7m57s
kube-system   kube-apiserver-minikube             1/1     Running   0               7m58s
kube-system   kube-controller-manager-minikube    1/1     Running   0               7m57s
kube-system   kube-proxy-rcpl2                    1/1     Running   0               7m52s
kube-system   kube-scheduler-minikube             1/1     Running   0               7m57s
kube-system   storage-provisioner                 1/1     Running   1 (7m21s ago)   7m56s
```

We now have three nginx pods prefixed with the metadata name we specified in the deployment yaml file.

One of the features of a deployment is that it will maintain the state configured in the yaml file. If for instance we try and kill a pod, it will automatically create a new one. 

If you run `kubectl pod delete nginx-deployment-647677fc66-cjk7c` and check the pod output, you will still see three pods, but a new pod has been started up in place of the deleted one.

```
NAMESPACE     NAME                                READY   STATUS    RESTARTS        AGE
default       nginx-deployment-647677fc66-g9pds   1/1     Running   0               3s
default       nginx-deployment-647677fc66-kvffx   1/1     Running   0               2m44s
default       nginx-deployment-647677fc66-ts2nn   1/1     Running   0               2m44s
```

To properly shut down a deployment, set the number of replicas to 0. This can be done imperatively using `kubectl scale deployment/nginx-deployment --replicas=0`. If you check the pods with `kubectl get pods`, you will see the message `No resources found in default namespace.` i.e. there are no more pods left. Of course the control plane is still up, which you can see with `kubectl get pods -A`, but all worker pods have been shut down:

```
NAMESPACE     NAME                               READY   STATUS    RESTARTS      AGE
kube-system   coredns-674b8bbfcf-k2mhc           1/1     Running   0             19m
kube-system   etcd-minikube                      1/1     Running   0             19m
kube-system   kube-apiserver-minikube            1/1     Running   0             19m
kube-system   kube-controller-manager-minikube   1/1     Running   0             19m
kube-system   kube-proxy-rcpl2                   1/1     Running   0             19m
kube-system   kube-scheduler-minikube            1/1     Running   0             19m
kube-system   storage-provisioner                1/1     Running   1 (18m ago)   19m
```

To shutdown everything run `minikube stop`, and optionally `minikube delete` to completely remove everything.

Calls to `kubectl get pods` or `kubectl get nodes` will throw errors since there is no control plane to connect to.
