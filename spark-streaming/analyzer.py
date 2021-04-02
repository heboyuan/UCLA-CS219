import subprocess
import signal

skeleton_file = "analyzer_base.py"
warning_template = """
===============================================
{}
===============================================
"""


class Cluster():

    def __init__(self, urf_module_name="udf", urf_module_path="udf.py"):
        self.flatmap_funciton_name = []
        self.map_funciton_name = []
        self.state_update_funciton_name = []
        self.master_url = ""
        self.dependency_file = [urf_module_path]
        self.urf_module_name = urf_module_name

    def register_master(self, master_url):
        self.master_url = master_url

    def update_udf(self, urf_module_name, urf_module_path):
        self.urf_module_name = urf_module_name
        self.dependency_file[0] = urf_module_path

    def add_dependency(self, *args):
        for arg in args:
            self.dependency_file.append(arg)

    def register_flatmap(self, *args):
        for arg in args:
            self.flatmap_funciton_name.append(arg)

    def register_map(self, *args):
        for arg in args:
            self.map_funciton_name.append(arg)

    def register_state_update(self, *args):
        for arg in args:
            self.state_update_funciton_name.append(arg)

    def print(self):
        print("spark master url")
        print(self.master_url)
        print("dependency")
        print(self.dependency_file)
        print("flatmap functions")
        print(self.flatmap_funciton_name)

    def construct_command(self):
        spark_commandline = "spark-submit --master {} ".format(self.master_url)
        if self.dependency_file:
            spark_commandline += "--files {} ".format(
                ",".join(self.dependency_file))
        spark_commandline += "{} {} {} {} {}".format(
            skeleton_file, self.urf_module_name, ",".join(self.flatmap_funciton_name), ",".join(self.map_funciton_name), ",".join(self.state_update_funciton_name))
        return spark_commandline

    def run(self):
        print(self.construct_command())
        process = subprocess.Popen(
            self.construct_command(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode('ascii'))
            retval = process.poll()
        except:
            print(warning_template.format("shutting down spark"))
            process.send_signal(signal.SIGINT)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode('ascii'))
            retval = process.poll()
            print(warning_template.format("finish shut down"))
