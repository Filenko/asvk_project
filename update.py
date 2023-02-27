import git
import shutil
import os

repo_url = "https://github.com/Filenko/asvk_project.git"

if os.path.exists("current_version"):
    repo = git.Repo("current_version")
    repo.remotes.origin.pull()
else:
    git.Repo.clone_from(repo_url, "current_version")

working_type = int(input("Write 1 if you on central computer and 2 if in server: "))

if working_type == 1:
    src_file = "./current_version/central_server/balance.py"
    dst_file = "./balance.py"
    shutil.copy(src_file, dst_file)
    src_file = "./current_version/central_server/config.py"
    dst_file = "./config.json"
    shutil.copy(src_file, dst_file)
elif working_type == 2:
    src_file = "./current_version/on_server.py"
    dst_file = "./on_server.py"
    shutil.copy(src_file, dst_file)

