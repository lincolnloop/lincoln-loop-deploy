def bootstrap():
    local("virtualenv ve")
    local("mkdir src")
    local("python grab_repos.py")
    