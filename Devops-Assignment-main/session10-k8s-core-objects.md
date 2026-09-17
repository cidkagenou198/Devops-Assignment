# 10. session10-k8s-core-objects

# 10. 01-rolling-update

```bash

## Step-by-Step Commands

### Step 1: Deploy v1
```bash
kubectl apply -f 01-rolling-update/deployment-v1.yaml
kubectl apply -f 01-rolling-update/service.yaml
```

Wait for all pods to be ready:
```bash
kubectl rollout status deployment/app-rolling
```

Expected output:
```text
deployment "app-rolling" successfully rolled out
```

PS D:\Dev-Ops kubernetes> cd  session10-k8s-core-objects  
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 01-rolling-update/deployment-v1.yaml
>> kubectl apply -f 01-rolling-update/service.yaml
deployment.apps/app-rolling created
service/app-rolling-service created

Check pods and their version label:
```bash
kubectl get pods -l app=app-rolling --show-labels
```

Expected output:
```text
NAME                           READY   STATUS    RESTARTS   AGE   LABELS
app-rolling-7b5f9d4c6-5kghm   1/1     Running   0          30s   app=app-rolling,version=v1
app-rolling-7b5f9d4c6-8mfnt   1/1     Running   0          30s   app=app-rolling,version=v1
app-rolling-7b5f9d4c6-d4zlt   1/1     Running   0          30s   app=app-rolling,version=v1
app-rolling-7b5f9d4c6-jkp2q   1/1     Running   0          30s   app=app-rolling,version=v1
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=app-rolling --show-labels
NAME                           READY   STATUS    RESTARTS   AGE   LABELS
app-rolling-7cdb64ff89-8zcjn   1/1     Running   0          41s   app=app-rolling,pod-template-hash=7cdb64ff89,version=v1
app-rolling-7cdb64ff89-cqlzb   1/1     Running   0          41s   app=app-rolling,pod-template-hash=7cdb64ff89,version=v1
app-rolling-7cdb64ff89-d9zdq   1/1     Running   0          41s   app=app-rolling,pod-template-hash=7cdb64ff89,version=v1
app-rolling-7cdb64ff89-fshbl   1/1     Running   0          41s   app=app-rolling,pod-template-hash=7cdb64ff89,version=v1

### Step 2: Check v1 in Browser / Terminal
```bash
# Minikube
curl http://$(minikube ip):30010
# OR
minikube service app-rolling-service --url
```

Expected: Page shows `VERSION: v1` with a dark background.

### Step 3: Trigger the Rolling Update to v2
```bash
kubectl apply -f 01-rolling-update/deployment-v2.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 01-rolling-update/deployment-v2.yaml
deployment.apps/app-rolling unchanged

### Step 4: Watch the Rollout Happen in Real Time (Run in a separate terminal)
```bash
# Terminal A: Watch pod churn
kubectl get pods -l app=app-rolling -w
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=app-rolling -w               
NAME                           READY   STATUS    RESTARTS   AGE
app-rolling-56bff6d88c-dzl8p   1/1     Running   0          21m
app-rolling-56bff6d88c-hn5bx   1/1     Running   0          20m
app-rolling-56bff6d88c-lsq8p   1/1     Running   0          20m
app-rolling-56bff6d88c-tnhcm   1/1     Running   0          20m

# Terminal B: Keep curling the service continuously — zero errors!
while true; do curl -s http://$(minikube ip):30010 | grep VERSION; sleep 1; done
```

Expected pod watch output (you will see v1 pods Terminating as v2 pods start):
```text
NAME                           READY   STATUS              RESTARTS   AGE
app-rolling-7b5f9d4c6-5kghm   1/1     Running             0          2m      <- v1
app-rolling-7b5f9d4c6-8mfnt   1/1     Running             0          2m      <- v1
app-rolling-7b5f9d4c6-d4zlt   1/1     Running             0          2m      <- v1
app-rolling-7b5f9d4c6-jkp2q   1/1     Running             0          2m      <- v1
app-rolling-9c4d8f6b7-t2wnz   0/1     ContainerCreating   0          3s      <- v2 starting
app-rolling-9c4d8f6b7-t2wnz   1/1     Running             0          8s      <- v2 ready
app-rolling-7b5f9d4c6-5kghm   1/1     Terminating         0          2m      <- v1 killed
app-rolling-9c4d8f6b7-m8pxr   0/1     ContainerCreating   0          2s      <- v2 starting
...
```

Expected curl output (service stays alive the whole time):
```text
<p>VERSION: v1</p>
<p>VERSION: v1</p>
<p>VERSION: v2</p>    <- Gradually switches to v2
<p>VERSION: v2</p>
```

### Step 5: Verify v2 is Fully Deployed
```bash
kubectl rollout status deployment/app-rolling
```
http://127.0.0.1:60806

```text
deployment "app-rolling" successfully rolled out
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl rollout status deployment/app-rolling
deployment "app-rolling" successfully rolled out
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 
```bash
kubectl get pods -l app=app-rolling --show-labels
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=app-rolling --show-labels
NAME                           READY   STATUS    RESTARTS   AGE   LABELS
app-rolling-56bff6d88c-dzl8p   1/1     Running   0          26m   app=app-rolling,pod-template-hash=56bff6d88c,version=v2
app-rolling-56bff6d88c-hn5bx   1/1     Running   0          25m   app=app-rolling,pod-template-hash=56bff6d88c,version=v2
app-rolling-56bff6d88c-lsq8p   1/1     Running   0          25m   app=app-rolling,pod-template-hash=56bff6d88c,version=v2
app-rolling-56bff6d88c-tnhcm   1/1     Running   0          25m   app=app-rolling,pod-template-hash=56bff6d88c,version=v2

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 
All pods now show `version=v2`.

### Step 6: Check Rollout History
```bash
kubectl rollout history deployment/app-rolling
```

Expected output:
```text
deployment.apps/app-rolling
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
```
app-rolling-56bff6d88c-tnhcm   1/1     Running   0          25m   app=app-rolling,pod-template-hash=56bff6d88c,version=v2
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl rollout history deployment/app-rolling
deployment.apps/app-rolling 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

### Step 7: Rollback to v1 (One Command!)
```bash

```

Expected output:
```text
deployment.apps/app-rolling rolled back
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl rollout undo deployment/app-rolling
Warning: resource deployments/app-rolling was previously managed with 'kubectl apply'. Rolling back will not update the kubectl.kubernetes.io/last-applied-configuration annotation, which may cause unexpected behavior on future 'kubectl apply' operations. Consider using 'kubectl apply' with your previous configuration file instead.
deployment.apps/app-rolling rolled back
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 
Verify it rolled back:
```bash
kubectl get pods -l app=app-rolling --show-labels
# All pods show version=v1 again
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=app-rolling --show-labels
NAME                           READY   STATUS      RESTARTS   AGE   LABELS
app-rolling-56bff6d88c-dzl8p   0/1     Completed   0          28m   app=app-rolling,pod-template-hash=56bff6d88c,version=v2
app-rolling-86d7d44d5b-44p2k   1/1     Running     0          25s   app=app-rolling,pod-template-hash=86d7d44d5b,version=v1
app-rolling-86d7d44d5b-ggnfz   1/1     Running     0          33s   app=app-rolling,pod-template-hash=86d7d44d5b,version=v1
app-rolling-86d7d44d5b-mwzbk   1/1     Running     0          18s   app=app-rolling,pod-template-hash=86d7d44d5b,version=v1
app-rolling-86d7d44d5b-pk6t6   1/1     Running     0          8s    app=app-rolling,pod-template-hash=86d7d44d5b,version=v1
---

## Cleanup
```bash
kubectl delete -f 01-rolling-update/service.yaml
kubectl delete -f 01-rolling-update/deployment-v1.yaml
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl delete -f 01-rolling-update/service.yaml
>> kubectl delete -f 01-rolling-update/deployment-v1.yaml
service "app-rolling-service" deleted from default namespace
deployment.apps "app-rolling" deleted from default namespace
```

!image.png

# Version V2

!image.png

# 10. 02-blue-green

```bash

## Step-by-Step Commands

### Step 1: Deploy Both Environments Simultaneously
```bash
kubectl apply -f 02-blue-green/deployment-blue.yaml
kubectl apply -f 02-blue-green/deployment-green.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 02-blue-green/deployment-blue.yaml
>> kubectl apply -f 02-blue-green/deployment-green.yaml
deployment.apps/app-blue created
deployment.apps/app-green created
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

Wait for all 6 pods to be Ready:
```bash
kubectl get pods -l app=myapp --show-labels

Expected output (6 pods total — 3 blue, 3 green):
```text
NAME                         READY   STATUS    RESTARTS   AGE   LABELS
app-blue-6c8d9b5f4-5k9tz    1/1     Running   0          30s   app=myapp,slot=blue,version=v1
app-blue-6c8d9b5f4-8qmzj    1/1     Running   0          30s   app=myapp,slot=blue,version=v1
app-blue-6c8d9b5f4-r2lxp    1/1     Running   0          30s   app=myapp,slot=blue,version=v1
app-green-7d4f8c6b9-4hqnw   1/1     Running   0          28s   app=myapp,slot=green,version=v2
app-green-7d4f8c6b9-6kpzt   1/1     Running   0          28s   app=myapp,slot=green,version=v2
app-green-7d4f8c6b9-9trmq   1/1     Running   0          28s   app=myapp,slot=green,version=v2
```

```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=myapp --show-labels
NAME                        READY   STATUS    RESTARTS   AGE   LABELS
app-blue-5c69d7785c-9fgjj   1/1     Running   0          70s   app=myapp,pod-template-hash=5c69d7785c,slot=blue,version=v1
app-blue-5c69d7785c-ktk5s   1/1     Running   0          70s   app=myapp,pod-template-hash=5c69d7785c,slot=blue,version=v1
app-blue-5c69d7785c-vxb9w   1/1     Running   0          70s   app=myapp,pod-template-hash=5c69d7785c,slot=blue,version=v1
app-green-84df7f978-2ww9x   1/1     Running   0          70s   app=myapp,pod-template-hash=84df7f978,slot=green,version=v2
app-green-84df7f978-mnmfw   1/1     Running   0          70s   app=myapp,pod-template-hash=84df7f978,slot=green,version=v2
app-green-84df7f978-p72d9   1/1     Running   0          70s   app=myapp,pod-template-hash=84df7f978,slot=green,version=v2
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 
### Step 2: Point Service to BLUE (v1 goes LIVE)
```bash
kubectl apply -f 02-blue-green/service-blue.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 02-blue-green/service-blue.yaml
service/myapp-service created

Test Blue is serving traffic:
```bash
curl http://$(minikube ip):30020
# OR
minikube service myapp-service --url
```

Expected output (visible in browser or terminal):
```text
BLUE ENVIRONMENT
Version: v1 | Slot: BLUE (LIVE)
```

### Step 3: Confirm Service Selector Before the Switch
```bash
kubectl describe svc myapp-service | grep Selector
```

Expected output:
```text
Selector:   app=myapp,slot=blue
```
Selector:                 app=myapp,slot=blue
```bash
kubectl get endpoints myapp-service
```

Expected output (3 blue pod IPs):
```text
NAME             ENDPOINTS                                         AGE
myapp-service    10.244.0.10:80,10.244.0.11:80,10.244.0.12:80    45s
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get endpoints myapp-service
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME            ENDPOINTS                                      AGE
myapp-service   10.244.0.15:80,10.244.0.16:80,10.244.0.17:80   3m17s

### Step 4: THE SWITCH — Flip 100% Traffic to GREEN (v2) Instantly
```bash
kubectl apply -f 02-blue-green/service-green.yaml
```

Expected output:
```text
service/myapp-service configured
```

Test Green is now live:
```bash
curl http://$(minikube ip):30020
```

Expected output:
```text
GREEN ENVIRONMENT
Version: v2 | Slot: GREEN (STANDBY -> PROMOTED)
```

Verify the selector changed:
```bash
kubectl describe svc myapp-service | grep Selector
```

Expected output:
```text
Selector:   app=myapp,slot=green
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 02-blue-green/service-green.yaml
service/myapp-service configured
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl describe svc myapp-service | grep Selector
grep : The term 'grep' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:38
+ kubectl describe svc myapp-service | grep Selector
+                                      ~~~~
    + CategoryInfo          : ObjectNotFound: (grep:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl describe svc myapp-service                
Name:                     myapp-service
Namespace:                default
Labels:                   app=myapp
Annotations:              <none>
Selector:                 app=myapp,slot=green

The switch from Blue to Green happened in **milliseconds** — a single `kubectl apply` changed the routing.

### Step 5: Verify Endpoints Changed
```bash
kubectl get endpoints myapp-service
```

Expected output (now shows 3 green pod IPs):
```text
NAME             ENDPOINTS                                         AGE
myapp-service    10.244.0.20:80,10.244.0.21:80,10.244.0.22:80    10s
```

### Step 6: Rollback — Flip Back to Blue in Under 5 Seconds
```bash
kubectl apply -f 02-blue-green/service-blue.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get endpoints myapp-service
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME            ENDPOINTS                                      AGE
myapp-service   10.244.0.18:80,10.244.0.19:80,10.244.0.20:80   4m22s
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

Confirm Blue is serving again:
```bash
curl http://$(minikube ip):30020
# Output: BLUE ENVIRONMENT
```
image output
### Step 7: Decommission the Old Blue Environment (After Green is Confirmed Stable)
```bash
kubectl delete deployment app-blue
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl delete deployment app-blue
deployment.apps "app-blue" deleted from default namespace

---

## Cleanup
```bash
kubectl delete -f 02-blue-green/service-blue.yaml
kubectl delete -f 02-blue-green/deployment-blue.yaml
kubectl delete -f 02-blue-green/deployment-green.yaml
```
deployment.apps "app-blue" deleted from default namespace
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl delete -f 02-blue-green/service-blue.yaml
>> kubectl delete -f 02-blue-green/deployment-blue.yaml
>> kubectl delete -f 02-blue-green/deployment-green.yaml
service "myapp-service" deleted from default namespace
Error from server (NotFound): error when deleting "02-blue-green/deployment-blue.yaml": deployments.apps "app-blue" not found
deployment.apps "app-green" deleted from default namespace
```

!image.png

# 10. 03-canary

```bash
## Step-by-Step Commands

### Step 1: Deploy Stable v1 (9 Pods = 90% Traffic)
```bash
kubectl apply -f 03-canary/deployment-stable.yaml
```

Wait until all 9 stable pods are running:
```bash
kubectl rollout status deployment/app-stable
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 03-canary/deployment-stable.yaml
deployment.apps/app-stable created

### Step 2: Deploy the Service
```bash
kubectl apply -f 03-canary/service.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 03-canary/service.yaml
service/myapp-canary-service created

### Step 3: Test — All Traffic Goes to Stable v1
```bash
for i in $(seq 1 10); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
```

Expected output (10 out of 10 requests hit stable):
```text
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
app-stable-6ffb777f9d-5cvcp   1/1     Running   0          10m
app-stable-6ffb777f9d-7x84r   1/1     Running   0          10m
app-stable-6ffb777f9d-cmgsf   1/1     Running   0          10m
app-stable-6ffb777f9d-ghmfs   1/1     Running   0          10m
app-stable-6ffb777f9d-jbm4t   1/1     Running   0          10m
app-stable-6ffb777f9d-jnvt8   1/1     Running   0          10m
app-stable-6ffb777f9d-lfcvp   1/1     Running   0          10m
app-stable-6ffb777f9d-qlm9w   1/1     Running   0          10m
app-stable-6ffb777f9d-zw82j   1/1     Running   0          10m
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

### Step 4: Deploy the Canary v2 Pod (1 Pod = 10% Traffic)
```bash
kubectl apply -f 03-canary/deployment-canary.yaml
```

Wait until the canary pod is running:
```bash
kubectl get pods -l app=myapp-canary --show-labels
```

Expected output (9 stable + 1 canary = 10 pods total):
```text
NAME                           READY   STATUS    LABELS
app-stable-6d7f8c5b4-2mqpt    1/1     Running   app=myapp-canary,track=stable,version=v1
app-stable-6d7f8c5b4-4krgn    1/1     Running   app=myapp-canary,track=stable,version=v1
app-stable-6d7f8c5b4-7jxqz    1/1     Running   app=myapp-canary,track=stable,version=v1
...  (9 stable total)
app-canary-9b6d4e7c8-5fmpx    1/1     Running   app=myapp-canary,track=canary,version=v2
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get deployments
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
app-canary   0/1     1            0           5s
app-stable   7/7     7            7           15m

### Step 5: Verify Traffic Split in Real Time
```bash
for i in $(seq 1 20); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
```

Expected output (approximately 1-2 canary hits out of 20):
```text
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
CANARY v2   <- approximately 1 in 10 requests hits the canary
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
STABLE v1
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
app-stable-6ffb777f9d-5cvcp   1/1     Running   0          13m   10.244.0.24   minikube   <none>           <none>
app-stable-6ffb777f9d-7x84r   1/1     Running   0          13m   10.244.0.26   minikube   <none>           <none>
app-stable-6ffb777f9d-cmgsf   1/1     Running   0          13m   10.244.0.21   minikube   <none>           <none>
app-stable-6ffb777f9d-ghmfs   1/1     Running   0          13m   10.244.0.23   minikube   <none>           <none>
app-stable-6ffb777f9d-jbm4t   1/1     Running   0          13m   10.244.0.28   minikube   <none>           <none>
app-stable-6ffb777f9d-jnvt8   1/1     Running   0          13m   10.244.0.25   minikube   <none>           <none>
app-stable-6ffb777f9d-lfcvp   1/1     Running   0          13m   10.244.0.27   minikube   <none>           <none>
app-stable-6ffb777f9d-qlm9w   1/1     Running   0          13m   10.244.0.29   minikube   <none>           <none>
app-stable-6ffb777f9d-zw82j   1/1     Running   0          13m   10.244.0.22   minikube   <none>           <none>
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
app-stable-6ffb777f9d-5cvcp   1/1     Running   0          13m   10.244.0.24   minikube   <none>           <none>
app-stable-6ffb777f9d-7x84r   1/1     Running   0          13m   10.244.0.26   minikube   <none>           <none>
app-stable-6ffb777f9d-cmgsf   1/1     Running   0          13m   10.244.0.21   minikube   <none>           <none>
app-stable-6ffb777f9d-ghmfs   1/1     Running   0          13m   10.244.0.23   minikube   <none>           <none>
app-stable-6ffb777f9d-jbm4t   1/1     Running   0          13m   10.244.0.28   minikube   <none>           <none>
app-stable-6ffb777f9d-jnvt8   1/1     Running   0          13m   10.244.0.25   minikube   <none>           <none>
app-stable-6ffb777f9d-lfcvp   1/1     Running   0          13m   10.244.0.27   minikube   <none>           <none>
app-stable-6ffb777f9d-qlm9w   1/1     Running   0          13m   10.244.0.29   minikube   <none>           <none>
app-stable-6ffb777f9d-zw82j   1/1     Running   0          13m   10.244.0.22   minikube   <none>           <none>
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get svc myapp-canary-service
NAME                   TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
myapp-canary-service   NodePort   10.99.71.29   <none>        80:30030/TCP   13m
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get endpoints myapp-canary-service
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                   ENDPOINTS                                                  AGE
myapp-canary-service   10.244.0.21:80,10.244.0.22:80,10.244.0.23:80 + 6 more...   13m
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> minikube ip
192.168.49.2
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> curl.exe http://192.168.49.2:30030

### Step 6: Increase Canary Traffic to 30% (3 out of 10 Pods)
```bash
kubectl scale deployment app-canary --replicas=3
kubectl scale deployment app-stable --replicas=7
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl scale deployment app-canary --replicas=3
>> kubectl scale deployment app-stable --replicas=7
deployment.apps/app-canary scaled
deployment.apps/app-stable scaled
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

Verify endpoints updated:
```bash
kubectl get endpoints myapp-canary-service
# Now shows 10 endpoints: 7 stable IPs + 3 canary IPs
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get endpoints myapp-canary-service
>> 
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                   ENDPOINTS                                                  AGE
myapp-canary-service   10.244.0.21:80,10.244.0.22:80,10.244.0.23:80 + 7 more...   15m
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

Re-run the traffic test:
```bash
for i in $(seq 1 10); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
# Expect approximately 3 CANARY v2 in 10 requests
```

### Step 7A: Promote Canary to 100% (Canary is Healthy)
```bash
# Scale canary to full replicas and remove stable
kubectl scale deployment app-canary --replicas=9
kubectl scale deployment app-stable --replicas=0
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl scale deployment app-canary --replicas=9
>> kubectl scale deployment app-stable --replicas=0
deployment.apps/app-canary scaled
deployment.apps/app-stable scaled
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

All 10 requests now hit v2:
```bash
for i in $(seq 1 5); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
# CANARY v2 x5
```

After confirming stable, clean up old stable deployment:
```bash
kubectl delete deployment app-stable
```

### Step 7B: Rollback Canary (Canary is Broken)
```bash
kubectl scale deployment app-canary --replicas=0
kubectl scale deployment app-stable --replicas=9
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl scale deployment app-canary --replicas=0
>> kubectl scale deployment app-stable --replicas=9
deployment.apps/app-canary scaled
deployment.apps/app-stable scaled
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 
All traffic instantly returns to v1 stable:
```bash
for i in $(seq 1 5); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done
# STABLE v1 x5
```

---

## Cleanup
```bash
kubectl delete -f 03-canary/service.yaml
kubectl delete -f 03-canary/deployment-canary.yaml
kubectl delete -f 03-canary/deployment-stable.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl delete -f 03-canary/service.yaml
>> kubectl delete -f 03-canary/deployment-canary.yaml
>> kubectl delete -f 03-canary/deployment-stable.yaml
service "myapp-canary-service" deleted from default namespace
deployment.apps "app-canary" deleted from default namespace
deployment.apps "app-stable" deleted from default namespace

```

# 10.  04-recreate

```bash

## Step-by-Step Hands-on Demonstration

### Step 1: Deploy Version 1 (3 replicas)
```bash
kubectl apply -f 04-recreate/deployment-v1.yaml
kubectl apply -f 04-recreate/service.yaml
```

Output:
```text
deployment.apps/app-recreate created
service/app-recreate-service created
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl apply -f 04-recreate/deployment-v1.yaml
>> kubectl apply -f 04-recreate/service.yaml
deployment.apps/app-recreate created
service/app-recreate-service created
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

Verify pods are running:
```bash
kubectl get pods -l app=app-recreate
```

Output:
```text
NAME                            READY   STATUS    RESTARTS   AGE
app-recreate-5899479b69-84x9q   1/1     Running   0          22s
app-recreate-5899479b69-q2f7m   1/1     Running   0          22s
app-recreate-5899479b69-z8l2k   1/1     Running   0          22s
```

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=app-recreate
NAME                            READY   STATUS    RESTARTS   AGE
app-recreate-6c78cb55bb-8pjqb   1/1     Running   0          20s
app-recreate-6c78cb55bb-llx97   1/1     Running   0          20s
app-recreate-6c78cb55bb-p8lfl   1/1     Running   0          20s

Test access via NodePort 30040:
```bash
curl http://localhost:30040
```

Output:
```html
<html><body style="background:#1b262c;color:#0f4c81;font-family:monospace;font-size:2.5em;text-align:center;padding-top:20vh">
<p style="color:#bbe1fa">STRATEGY: RECREATE</p>
<p style="color:#3282b8">VERSION: v1</p>
<p style="font-size:0.4em;color:#bbe1fa">All v1 pods will be killed before v2 starts</p>
</body></html>
```

---

### Step 2: Trigger the Recreate Update

Open two terminal windows side-by-side to watch the downtime behavior:

#### Terminal 1: Watch pods in real time
```bash
kubectl get pods -l app=app-recreate -w
```

#### Terminal 2: Apply the v2 deployment
```bash
kubectl apply -f 04-recreate/deployment-v2.yaml
```

Observe Terminal 1:
```text
NAME                            READY   STATUS        RESTARTS   AGE
app-recreate-5899479b69-84x9q   1/1     Terminating   0          84s
app-recreate-5899479b69-q2f7m   1/1     Terminating   0          84s
app-recreate-5899479b69-z8l2k   1/1     Terminating   0          84s
app-recreate-5899479b69-84x9q   0/1     Terminating   0          87s
app-recreate-5899479b69-q2f7m   0/1     Terminating   0          87s
app-recreate-5899479b69-z8l2k   0/1     Terminating   0          87s

PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl get pods -l app=app-recreate -w
NAME                            READY   STATUS    RESTARTS   AGE
app-recreate-6c78cb55bb-8pjqb   1/1     Running   0          12m
app-recreate-6c78cb55bb-llx97   1/1     Running   0          12m
app-recreate-6c78cb55bb-p8lfl   1/1     Running   0          12m

# NOTICE: ZERO PODS ARE RUNNING AT THIS POINT (DOWNTIME WINDOW)

app-recreate-7774c869c8-d42wz   0/1     Pending            0          0s
app-recreate-7774c869c8-k9x12   0/1     Pending            0          0s
app-recreate-7774c869c8-m78qp   0/1     Pending            0          0s
app-recreate-7774c869c8-d42wz   0/1     ContainerCreating  0          1s
app-recreate-7774c869c8-k9x12   0/1     ContainerCreating  0          1s
app-recreate-7774c869c8-m78qp   0/1     ContainerCreating  0          1s
app-recreate-7774c869c8-d42wz   1/1     Running            0          4s
app-recreate-7774c869c8-k9x12   1/1     Running            0          4s
app-recreate-7774c869c8-m78qp   1/1     Running            0          4s
```

---

### Step 3: Observe the Outage During Recreate

If you run a curl loop during the transition:
```bash
while true; do curl -s --connect-timeout 1 http://localhost:30040 | grep -o 'VERSION: [^<]*' || echo "[OUTAGE] Connection failed"; sleep 0.5; done
```

Output:
```text
VERSION: v1
VERSION: v1
[OUTAGE] Connection failed
[OUTAGE] Connection failed
[OUTAGE] Connection failed
VERSION: v2 (UPGRADED)
VERSION: v2 (UPGRADED)
```

VERSION: v1
VERSION: v1
[OUTAGE] Connection failed
[OUTAGE] Connection failed
[OUTAGE] Connection failed
VERSION: v2 (UPGRADED)
VERSION: v2 (UPGRADED)
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

This live output clearly proves to students why Recreate has downtime and why it must be used intentionally during scheduled maintenance windows.

---

### Step 4: Verify Version 2

```bash
curl http://localhost:30040
```

Output:
```html
<html><body style="background:#0f4c81;color:#ffffff;font-family:monospace;font-size:2.5em;text-align:center;padding-top:20vh">
<p style="color:#bbe1fa">STRATEGY: RECREATE</p>
<p style="color:#00ffcc">VERSION: v2 (UPGRADED)</p>
<p style="font-size:0.4em;color:#ffffff">Successfully replaced after full shutdown</p>
</body></html>
```

---

### Step 5: Rollback Demonstrationwwwwwwww

If v2 has an issue and you must revert to v1:
```bash
kubectl rollout undo deployment/app-recreate
```

Output:
```text
deployment.apps/app-recreate rolled back
```

Check rollout status:
```bash
kubectl rollout status deployment/app-recreate
```

Output:
```text
deployment "app-recreate" successfully rolled out
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl rollout undo deployment/app-recreate
Warning: resource deployments/app-recreate was previously managed with 'kubectl apply'. Rolling back will not update the kubectl.kubernetes.io/last-applied-configuration annotation, which may cause unexpected behavior on future 'kubectl apply' operations. Consider using 'kubectl apply' with your previous configuration file instead.
deployment.apps/app-recreate rolled back
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 

---

## Strategy Comparison Matrix

| Strategy | Downtime? | Cost / Resource Overhead | Rollback Speed | Best Used For |
|---|---|---|---|---|
| **RollingUpdate** | Zero downtime | Low (+25% capacity during update) | Fast (`kubectl rollout undo`) | Default for stateless web apps and microservices |
| **Blue-Green** | Zero downtime | High (200% capacity required) | Instant (update service selector) | Mission-critical apps requiring atomic cutover and instant rollback |
| **Canary** | Zero downtime | Low (only small extra canary pool) | Fast (scale canary down to 0) | High-traffic services needing real-user validation before full rollout |
| **Recreate** | Yes (brief outage) | Zero (no surge capacity needed) | Slower (requires killing v2 and starting v1) | Schema migrations, RWO storage locks, dev environments |

---

## Cleanup
```bash
kubectl delete -f 04-recreate/service.yaml
kubectl delete -f 04-recreate/deployment-v2.yaml
```
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> kubectl delete -f 04-recreate/service.yaml
>> kubectl delete -f 04-recreate/deployment-v2.yaml
service "app-recreate-service" deleted from default namespace
deployment.apps "app-recreate" deleted from default namespace
PS D:\Dev-Ops kubernetes\session10-k8s-core-objects> 
```

!image.png

!image.png

#
