Task 1: Docker Container Networking

<img width="483" height="187" alt="image" src="https://github.com/user-attachments/assets/9e23ffed-3022-4cb8-90f0-9304b2db8736" />

<img width="1250" height="120" alt="image" src="https://github.com/user-attachments/assets/c7770e73-3364-44d3-b1a1-0413bb2c7286" />

<img width="596" height="180" alt="image" src="https://github.com/user-attachments/assets/d5f73599-0d1b-437e-907e-ce371976893c" />

<img width="595" height="196" alt="image" src="https://github.com/user-attachments/assets/017d7a2d-1d69-4add-9280-6e1b288fbca4" />




Task 2: Host Network

<img width="654" height="285" alt="image" src="https://github.com/user-attachments/assets/9fcefa4b-6a15-40ca-a564-8e3bd5d6149b" />

<img width="753" height="51" alt="image" src="https://github.com/user-attachments/assets/2443b306-5549-4d9b-89dc-8e2fd9130454" />

working proof
<img width="744" height="211" alt="image" src="https://github.com/user-attachments/assets/2b1ced83-dc0c-4a58-850e-c319297c03ba" />


Task 3: Bind Mount
<img width="1451" height="725" alt="image" src="https://github.com/user-attachments/assets/45dc309d-b3b0-4ace-b2f3-86dbd901865e" />

<img width="1161" height="416" alt="image" src="https://github.com/user-attachments/assets/9d6dd8fd-880e-4337-b191-1b09ee386ba7" />


Task 4: Overlay Network
Docker overlay networks provide multi-host container networking. They create a distributed virtual network across multiple Docker hosts, allowing containers or Swarm services on different hosts to communicate. Overlay networks are commonly used with Docker Swarm for distributed applications.


Example: 



Docker Host 1                    Docker Host 2
┌───────────────┐                ┌───────────────┐
│ Container A   │                │ Container B   │
│   10.x.x.x    │                │   10.x.x.x    │
└───────┬───────┘                └───────┬───────┘
        │                                │
        └──────── Overlay Network ───────┘
                    │
             Docker networking
