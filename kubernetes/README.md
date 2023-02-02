# Kubernetes Concepts Cheat Sheet

* **[Cluster](https://kubernetes.io/docs/concepts/overview/components/)**:
    * **[Node](https://kubernetes.io/docs/concepts/architecture/nodes/)**: worker machine, e.g. VM of [minikube](https://kubernetes.io/docs/tasks/tools/#minikube)
        * **Container Runtime**:
            * Container Runtime Engines, implementing **CRI** (Container Runtime Interface):
              * Default: Containerd, uses [Docker](https://www.docker.com/).
              * Others: Cri-o, Rkt, Kata, Virtlet (uses VM), etc.
            * **[Pod](https://kubernetes.io/docs/concepts/workloads/pods/)**: logical host with set of Containers, shared network and storage, as in `docker-compose`
                * Pod is immutable: you (or controller) have to delete and create a pod to "update" it.
                * **[Containers](https://kubernetes.io/docs/concepts/containers/container-environment/)**: running Images, e.g. Docker containers
                    * **[Image](https://kubernetes.io/docs/concepts/containers/images/)**: e.g. Docker image
                    * **[hostname](https://kubernetes.io/docs/concepts/containers/container-environment/#container-information)**: name of Pod
                    * DNS resolver uses CoreDNS server
                * **[Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)**: links to external persistent storage
            * **kube-proxy**: Pod allowing network requests to Pods at this Node
        * **kubelet**: agent making sure Containers are running in Pods at this Node
            * **[Lease](https://kubernetes.io/docs/concepts/architecture/leases/)**: Object with `renewTime` updated on every heart beat of `kubelet`

    * **Control Plane**: `kubectl get pods --namespace=kube-system`
        * **kube-apiserver**: **API** server, entry point of Control Plane
            * **CLI**: **[kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)**, kubeadm, etc.
            * **[SDK](https://kubernetes.io/docs/reference/using-api/client-libraries/)**
            * **[API reference](https://kubernetes.io/docs/reference/kubernetes-api/)**
        * **etcd**: consistent HA KV store of Cluster **State**
        * **kube-controller-manager**: runs Controllers
            * **[Controller](https://kubernetes.io/docs/concepts/architecture/controller/)**: loop calling API to get its kind of objects to Desired State
            * E.g. **Job Controller** detects new Job has no Pods, asks API to create Pods, checks Job, updates Job status, asks API to delete Pods
        * **kube-scheduler**: selects Node for new Pod
        * **[cloud-controller-manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/)**: runs Controllers syncing K8s Objects with cloud resources
            * E.g. **Node Controller** detects new cloud servers, creates K8s Node Objects, checks health of Nodes, deletes Nodes from Cluster
        * [Addons:](https://kubernetes.io/docs/concepts/cluster-administration/addons/)
            * **CoreDNS**: DNS server required for Services
            * **[storage-provisioner](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)**: auto-provisioning of storage on demand

    * **Object**: computational, storage, networking, etc. resource, tracked at Cluster State
        * **Config**: describes `apiVersion`, `kind` of the Object, `metadata` (`namespace`, `name`, `labels`), `spec` - its **Desired State**
            * [Example](https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/application/deployment.yaml)
            * Sent by SDK or by `kubectl apply -f configs/object.yaml` as JSON to API
            * Low-level CRUD [best practice](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/):
                * `kubectl diff -Rf configs/`
                * `kubectl apply -Rf configs/`
                * While `--prune` flag is [in alpha](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/#how-to-delete-objects)
                  and `kubectl apply` fails for empty `configs/` dir:  
                  `kubectl delete -f configs/object.yaml && git rm $_`
            * Use [Helm](https://helm.sh/) for high-level CRUD, K8s package manager, templating (scripting) of K8s configs.
        * Kinds of Objects not defined above:
            * **[Workload](https://kubernetes.io/docs/concepts/workloads/controllers/)**: Controllers that schedule Pods - smallest workload units
                * **[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)**: low-level, how many replicas of Pod are desired
                * **[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)**: most popular, ReplicaSet with rolling updates
                * **[StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)**: ReplicaSet for stateful app. Reserves resources for each of its unique ordered Pods: network name, volume, etc.
                * **[DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)**: ensures all (or some) Nodes run given Pod
                * **[Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/)**: one-off task retrying its Pods until given number of successful completions
                * **[CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)**: creates Job on a repeating schedule
            * **[Network](https://kubernetes.io/docs/concepts/services-networking/)**:
                * **[Service](https://kubernetes.io/docs/concepts/services-networking/service/)**: exposes all Pods matching `selector` to a (usually external) network
                  * **[ServiceTypes](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)**:
                    * **[ClusterIP](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)**: default, internal IP address routes to each matching Pod. Such Service can be exposed externally e.g. via Ingress.
                      * **[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)**: rules (usually by HTTP /path) route external HTTP(S) traffic to multiple Services
                    * **[NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)**: static port on external IP address of each Node (`NodeIP:NodePort`) in a Cluster routes to auto-created ClusterIP Service
                    * **[LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)**: most popular, Cloud LB routes to auto-created (usually a NodePort) Service
            * **[Storage](https://kubernetes.io/docs/concepts/storage/)**:
              * **Volume**: a file directory (numerous types), defined with `name` in Pod, mounted in Container to a `mountPath`, dies with its Pod
              * **PersistentVolume** or **PV**: like Volume, but lives outside of Pods, can be mounted via PersistentVolumeClaim only
              * **PersistentVolumeClaim**:
                * Declares storage requirements
                * Binds to matching unbound PersistentVolume, if any
                * Can be referenced in a Volume of a Pod - the only way to use PersistentVolume in a Pod
              * **StorageClass**: what storage is available in this Cluster from numerous possible types, defines `provisioner` driver, etc
            * **[Config](https://kubernetes.io/docs/concepts/configuration/)**:
              * **ConfigMap**: non-secret key-values, used in Pod as a Volume or as `env` vars with `valueFrom.configMapKeyRef`, that can be passed to `command` args
              * **Secret**: a secret ConfigMap, types are Docker-registry creds, any Opaque data, Tls cert
            * **[CRD](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#create-a-customresourcedefinition)**: Custom Resource Definition

    * Networking Rules:
      * External - Cloud LB, etc - `kube-proxy` - Service - `kube-proxy` - Pod
      * Pod-Pod and Pod-Node in the same Cluster talk via internal IP addresses
      * Container-Container in the same Pod talk via localhost port, IPC if process namespace is shared, volume if shared

    * **[Security](https://kubernetes.io/docs/concepts/security/)**:
      * User or Pod sends request to K8s API server, passing:
        * **Authentication**:
          * **X509 Client Cert**: CN=user, Org=group
          * **Static Password File**: password,user,uid,"group1,.."
          * **Static Token File**: token,user,uid,"group1,.."
          * **Bearer Token** or **Bootstrap Token**: `Authorization: Bearer ...`
          * **Service Account Token**: static file or signed by TLS private key of API Server
          * **OpenID Connect Token (OIDC)**: JWT using ID token from OAuth2 token response
        * **Authorization**: which actions are allowed
          * **Role**: defines `rules` to allow do `verbs` (e.g. `list`) with `resources` (e.g. `pods`)
          * **ClusterRole**: a cluster-wide Role without `metadata.namespace`
          * **RoleBinding**: grants Role or ClusterRole (limited to namespace) to `subjects` of type User, Group, ServiceAccount
          * **ClusterRoleBinding**: a cluster-wide RoleBinding without `metadata.namespace`, can `roleRef` ClusterRole only
        * **Admission Control**: uses numerous **Admission Controllers** for rate limit, policies, other constraints

    * Etc **[Concepts](https://kubernetes.io/docs/concepts/)**
