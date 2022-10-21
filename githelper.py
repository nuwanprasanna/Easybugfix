from git import Repo
def git_push(path, COMMIT_MESSAGE):
    try:
        repo = Repo(path)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')
