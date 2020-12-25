"""
    Build Project Scala and Java Jar Files
    Original Source: https://github.com/databricks/LearningSparkV2
"""
import os
import sys

import multiprocessing
from multiprocessing import Pool

cpu = multiprocessing.cpu_count() - 1

def build_jar_files(dir):
    """
    Build a list of directories via SBT    
    """
    print(f"\n* Building Jar files {dir}\n")
    cmd = f"cd {dir}/ && sbt clean package"
    
    exit_status = os.system(cmd)
    
    if exit_status:
        os._exit(exit_status)
    return exit_status

if __name__ == '__main__':
    # List of folders to build
    folders = ["TopTenReporters"]
    with Pool(cpu) as p:
        p.map(build_jar_files, folders)
    
    p.close()
    p.terminate()
    print("\n* Finished\n")