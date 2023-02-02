# Kubernetes Concepts Cheat Sheet

* **[Cluster](https://kubernetes.io/docs/concepts/overview/components/)**:
    * **[Node](https://kubernetes.io/docs/concepts/architecture/nodes/)**: worker machine, e.g. VM of [minikube](https://kubernetes.io/docs/tasks/tools/#minikube)
        * **Container Runtime**: [Docker](https://www.docker.com/) by default
            * **[Pod](https://kubernetes.io/docs/concepts/workloads/pods/)**: logical host with set of Containers, shared network and storage, as in `docker-compose`
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
            * **storage-provisioner**: [TODO](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)

    * **Object**: computational, storage, networking, etc. resource, tracked at Cluster State
        * **Config**: describes **Kind** of Object, **Name** and **Labels** to identify it, and **Spec** - its **Desired State**
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
            * **[Workload](https://kubernetes.io/docs/concepts/workloads/controllers/)**:
                * **[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)**: how many replicas of Pod are desired
                * **[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)**: ReplicaSet with rolling updates
                * **[StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)**: ReplicaSet for stateful app
                * **[DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)**: ensures all (or some) Nodes run given Pod
                * **[Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/)**: one-off task retrying Pods until given number of successful completions
                * **[CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)**: creates Job on a repeating schedule
            * **[Network](https://kubernetes.io/docs/concepts/services-networking/)**:
                * **[Service](https://kubernetes.io/docs/concepts/services-networking/service/)**: exposes Pods to external network
                * TODO
            * **[Storage](https://kubernetes.io/docs/concepts/storage/)**: TODO
            * **[Config](https://kubernetes.io/docs/concepts/configuration/)**: TODO
            * **[CRD](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#create-a-customresourcedefinition)**: Custom Resource Definition
            * Etc **[Concepts](https://kubernetes.io/docs/concepts/)**: TODO
