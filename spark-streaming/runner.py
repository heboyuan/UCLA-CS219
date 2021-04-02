from analyzer import Cluster

c = Cluster()

c.register_master("spark://vagrant.vm:7077")

c.add_dependency("decoder.py")

c.register_flatmap("decode_line")
c.register_map("message_count")
c.register_state_update("update_count")

c.run()
