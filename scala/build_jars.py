import os
import glob
import shutil

import multiprocessing
from multiprocessing import Pool

cpu = multiprocessing.cpu_count() - 1
jars_dir = os.path.join(os.getcwd(), "jars")
scala_dir = 'target/scala-2.12'

if not os.path.exists(jars_dir):
    os.makedirs(jars_dir)

def build_jar_files(dir):
    """
    Build a list of directories via SBT    
    """
    print(f"* Building Jar files {dir}")
    cmd = f"cd {dir}/ && sbt clean assembly"
    
    exit_status = os.system(cmd)
    
    if exit_status:
        os._exit(exit_status)
    return exit_status

if __name__ == '__main__':
    
    # List of folders to build
    folders = ['ConvertCsvToParquet', 'QueryColumnParquet']
    with Pool(cpu) as p:
        p.map(build_jar_files, folders)
    
    p.close()
    p.terminate()

    # Note: This is not dynamic, as the Scala version is set manually above
    print("\nCopy All Jar Packages")
    for f in folders:
        file_path = os.path.join(os.getcwd(),f,scala_dir)
        files = glob.iglob(os.path.join(file_path, "*.jar"))
        for file in files:
            if os.path.isfile(file):
                print(f"* {file}")
                shutil.copy2(file, jars_dir)

    print(f"\nJar Location : {jars_dir}\n")
    print("\nFinished\n")