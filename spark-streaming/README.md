start-master.sh
start-slave.sh spark://vagrant.vm:7077

docker exec -it app bash
bash start.sh

python3 runner.py






vagrant ssh -- -L 8081:10.0.2.15:8081
vagrant ssh -- -L 4040:10.0.2.15:4040