import os
import glob
import shutil

import multiprocessing
from multiprocessing import Pool

# NOTE: Set to the version of Scala you are using.
scala_dir = 'target/scala-2.12'

cpu = multiprocessing.cpu_count() - 2
jars_dir = os.path.join(os.getcwd(), "jars")

if not os.path.exists(jars_dir):
    os.makedirs(jars_dir)

def build_jar_files(dir):
    """
    Build a list of directories via SBT    
    """
    print(f"[info] Building Jar file for: {dir}")
    cmd = f"cd {dir}/ && sbt clean package"
    exit_status = os.system(cmd)
    
    if exit_status:
        os._exit(exit_status)
    return exit_status


if __name__ == '__main__':

    folders = ['CsvDownload']
    with Pool(cpu) as p:
        p.map(build_jar_files, folders)
    p.close()
    p.terminate()

    # Note: This is not dynamic. The Scala version is set manually above
    for f in folders:
        file_path = os.path.join(os.getcwd(),f,scala_dir)
        files = glob.iglob(os.path.join(file_path, "*.jar"))
        for file in files:
            if os.path.isfile(file):
                print(f"[info] copy jar file: {file}")
                shutil.copy2(file, jars_dir)
    print(f"[info] jar location: {jars_dir}")
    print("\nFinished\n")
