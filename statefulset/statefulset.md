# Statefulsets vs Deployments

Now that we've done a basic deployment, let's talk about statefulsets. Deployments are good for applications which are stateless and don't need data persistence e.g. web servers. Statefulsets, like their name suggests, are for applications which are state sensitive and do need data persistence e.g. databases.

To a launch a statefulset, you can still use the same declarative workflow of invoking `kubectl apply`, but this time we'll point it to a different configuration file. 

```
kubectl apply -f statefulset/postgres-statefulset.yaml
```

If you inspect `statefulset/postgres-statefulset.yaml` and compare it with `deployment/Basic-Deployment.md`, you'll notice a few key differences. Firstly, rather than the kind being a `Deployment`, it is now a `Statefulset`. Secondly, you'll notice some extra details under the `containers` subfield and we'll also have an extra section in the `spec` called `VolumeClaimTemplates`:

```
spec:
  ...
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

A VolumeClaimTemplate This is one of the features that distinguish a statefulset from a deployment. When applied, it tells Kubernetes to create a Persistent Volume Claim (PVC), which allows the application to connect to a specified subset of storage allocated to the cluser. It can be thought of like the relationship between an image and a container. An image (VolumeClaimTemplate) is a blueprint for which an actual container (PVC) is created and runs. So when a statefulset is launched, it will also create a PVC if one doesn't exist already.

To see this in action, first create the statefulset using `kubectl apply -f statefulset/postgres-statefulset.yaml`.

Then wait a few seconds for the application to start up. Again, you can check on its progress by using `kubectl get pods -A`.

Once the pod has started up, run `kubectl get pvc`, the output should look something like this:

```
NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
data-postgres-db-0   Bound    pvc-4bef7ac4-fc21-48f4-b0b3-1b1f464e51e6   10Gi       RWO            standard       <unset>                 2m22s
```

The name comes from a combination of two things, the name of the VolumeClaimTemplate we specified in the Statefulset yaml file, `data`, as well as the name of the statefulset itself, `postgres-db`. It also has the attributes which we specified in the configuration, with a capacity of 10 Gi and a ReadWriteOnce access mode. We didn't specify the storage class, but by default it's `standard`.

By design, the PVC will persist and retain its data even after the statefulset is shutdown. To verify this, let's first load the database with some data. 

Open up an interactive shell and login to psql with this command:

```
kubectl exec -it postgres-db-0 -- psql -U postgres
```

Then run the following SQL code, it will create a dummy user table with randomly generated ages, usernames and signup dates:

```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    age INT,
    signup_date DATE
);

INSERT INTO users (username, age, signup_date)
SELECT
    'user_' || gs,                      -- usernames like user_1 … user_1000
    (random() * 60 + 18)::int,          -- random ages between 18–78
    CURRENT_DATE - (random() * 365)::int -- random signup date within past year
FROM generate_series(1, 1000) gs;
```

Once the command has been executed, you can check that it has been created with `SELECT * FROM users LIMIT 1;`, the output should be something like this:

```
 id | username | age | signup_date
----+----------+-----+-------------
  1 | user_1   |  66 | 2025-03-27
(1 row)
```

We're now going to check for data persistence by shutting down the postgres instance. Exit out of the postgres shell, and run `kubectl scale statefulset postgres-db --replicas=0 && kubectl delete statefulset postgres-db`. Once the pod has been shutdown, run `kubectl get pvc` to verify that the PVC still exists.

Now start up the statefulset again with `kubectl apply -f statefulset/postgres-statefulset.yaml` and login to the psql interface like before. This time, you will see that the `users` table still exists, verify by running `SELECT * FROM users LIMIT 1;`, you should get the same output as before.

However, if you run `kubectl delete pvc data-postgres-db-0`, the attached volume will be erased and the data will no longer exist. If you're building an actual application or working in production, be very careful when running this command!

### List of commands

`kubectl apply -f statefulset/postgres-statefulset.yaml`: Creates/updates the statefulset as specified in the yaml file
`kubectl get pvc`: Lists out all Persistent Volume Claims (PVC)
`kubectl exec -it postgres-db-0 -- psql -U postgres`: Runs an interactive shell and logins to the psql inteface
`kubectl scale statefulset postgres-db --replicas=0 && kubectl delete statefulset postgres-db`: Scales down and deletes the statefulset

`kubectl delete pvc data-postgres-db-0`: Deletes the PVC for the Statefulset. **WARNING, if you run this command, your data will be permanently deleted unless it has been backed up elsewhere!**

SQL commands are also stored in `statefulset/init.sql`.
