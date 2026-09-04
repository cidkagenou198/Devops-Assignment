Task 1: Docker Container Networking

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)



Task 2: Host Network

![alt text](image-4.png)
![alt text](image-5.png)
working proof
![alt text](image-6.png)

Task 3: Bind Mount
![alt text](image-7.png)
![alt text](image-8.png)

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
