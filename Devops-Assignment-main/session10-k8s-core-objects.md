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

<img width="883" height="152" alt="image" src="https://github.com/user-attachments/assets/b46ba8d1-a269-4902-9e5c-0e735b3bfdb3" />


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
<img width="885" height="258" alt="image" src="https://github.com/user-attachments/assets/8eb5b0c5-0aa1-471e-953f-cb6ad09d92f9" />


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
<img width="891" height="95" alt="image" src="https://github.com/user-attachments/assets/383bbb4f-d2a3-4b24-b794-13337ed59547" />


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
<img width="879" height="110" alt="image" src="https://github.com/user-attachments/assets/ce2a9cb7-be3c-425d-8097-bfd8737960c8" />

```bash
kubectl get pods -l app=app-rolling --show-labels
```

<img width="883" height="314" alt="image" src="https://github.com/user-attachments/assets/88c3ecab-fc71-4d7f-a8b1-1e2d82a5a3b0" />

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
<img width="873" height="196" alt="image" src="https://github.com/user-attachments/assets/d796fe1b-4072-4b0b-bd0d-ff54d7f21400" />


### Step 7: Rollback to v1 (One Command!)
```bash

```

Expected output:
```text
deployment.apps/app-rolling rolled back
```
<img width="878" height="190" alt="image" src="https://github.com/user-attachments/assets/53535105-eb1e-4d9c-bb22-7711397dd125" />

Verify it rolled back:
```bash
kubectl get pods -l app=app-rolling --show-labels
# All pods show version=v1 again
```
<img width="874" height="309" alt="image" src="https://github.com/user-attachments/assets/57670339-ec26-430d-82da-2e4a7d684338" />

---

## Cleanup
```bash
kubectl delete -f 01-rolling-update/service.yaml
kubectl delete -f 01-rolling-update/deployment-v1.yaml
```

<img width="859" height="142" alt="image" src="https://github.com/user-attachments/assets/23566bc6-6212-4b95-9229-72031958b0b4" />

```
```
# Version V1
<img width="1599" height="720" alt="image" src="https://github.com/user-attachments/assets/c58a0bb7-0e35-4f25-a0bb-f3aa5bf2ba86" />

# Version V2

<img width="1872" height="803" alt="image" src="https://github.com/user-attachments/assets/1b7a0ac7-0429-4dd9-812e-2d51c3367332" />


# 10. 02-blue-green
```
```bash

## Step-by-Step Commands

### Step 1: Deploy Both Environments Simultaneously
```bash
kubectl apply -f 02-blue-green/deployment-blue.yaml
kubectl apply -f 02-blue-green/deployment-green.yaml
```
<img width="880" height="159" alt="image" src="https://github.com/user-attachments/assets/67610309-312a-49d4-9548-9bcf31929c72" />


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
<img width="866" height="84" alt="image" src="https://github.com/user-attachments/assets/c2f9001c-4fd3-4073-92bc-b12559dd2b06" />


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
<img width="822" height="132" alt="image" src="https://github.com/user-attachments/assets/7555ad6a-6679-411e-87d2-f4d4971ee40b" />

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
<img width="872" height="529" alt="image" src="https://github.com/user-attachments/assets/bdb4f75d-1562-4bd7-9fc1-a73f1964b3ae" />


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
<img width="818" height="117" alt="image" src="https://github.com/user-attachments/assets/405ef4ca-1c03-47e7-b475-b99af55b9a6e" />


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
<img width="871" height="175" alt="image" src="https://github.com/user-attachments/assets/9426efc5-ab7b-4701-9444-d51ba11a579b" />

```
```
<img width="1875" height="883" alt="image" src="https://github.com/user-attachments/assets/51c4f4dd-7330-4484-a7c9-3c00f6b7bc12" />

```
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
<img width="878" height="93" alt="image" src="https://github.com/user-attachments/assets/23704752-0148-4bc1-b4b6-99a82a9657db" />


### Step 2: Deploy the Service
```bash
kubectl apply -f 03-canary/service.yaml
```
<img width="860" height="60" alt="image" src="https://github.com/user-attachments/assets/43eeafcb-8c1a-450f-ad3d-a5103e2f732e" />


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
<img width="652" height="312" alt="image" src="https://github.com/user-attachments/assets/313ea860-7996-4d48-9de5-93eb4f94fa15" />

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
<img width="710" height="107" alt="image" src="https://github.com/user-attachments/assets/61372a1e-f658-4240-b28c-f08f410c6fba" />


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

<img width="691" height="972" alt="image" src="https://github.com/user-attachments/assets/e1249aaf-4e43-4a11-9f0f-98b60877b516" />


### Step 6: Increase Canary Traffic to 30% (3 out of 10 Pods)
```bash
kubectl scale deployment app-canary --replicas=3
kubectl scale deployment app-stable --replicas=7
```
<img width="690" height="126" alt="image" src="https://github.com/user-attachments/assets/432ee81f-ef1b-430e-b605-8b83e0c9aaa4" />


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

<img width="684" height="117" alt="image" src="https://github.com/user-attachments/assets/0b462951-6028-4ca2-bd95-a77fac8ada3c" />


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

<img width="685" height="136" alt="image" src="https://github.com/user-attachments/assets/5efd1642-5319-48dd-b3dd-e0e3131304bd" />

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
<img width="691" height="134" alt="image" src="https://github.com/user-attachments/assets/2b6a01eb-3979-4e72-8a45-d56897b77bab" />

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

<img width="696" height="128" alt="image" src="https://github.com/user-attachments/assets/e24215c1-625d-4d10-95c3-7af72ccc901c" />


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

<img width="664" height="134" alt="image" src="https://github.com/user-attachments/assets/689d680a-968c-4cc4-9b3d-48af40be9750" />

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
<img width="398" height="171" alt="image" src="https://github.com/user-attachments/assets/24bbd4af-db4c-4958-bd0e-c4efe5159d7a" />


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
<img width="696" height="156" alt="image" src="https://github.com/user-attachments/assets/6562d01f-6f54-4319-bc80-3c96683c0e67" />


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
<img width="688" height="117" alt="image" src="https://github.com/user-attachments/assets/4e868ea3-a9dd-46ff-8283-ad5e08dde8fc" />

```
```
![Recreate v1](https://github.com/user-attachments/assets/2a9321d4-303f-44c0-bc07-7eafb0ee2c64)
![Recreate v2](https://github.com/user-attachments/assets/b2ee19e4-9b54-48f5-8a4e-c6ab61fe33b4)



