import gitlab
import os 

class bcolors:
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

start = '[' + bcolors.BLUE + 'START' + bcolors.ENDC + '] : '
done = '[' + bcolors.YELLOW + 'DONE' + bcolors.ENDC + '] : '
success = '[' + bcolors.GREEN + 'SUCCESS' + bcolors.ENDC + '] : '
error = '[' + bcolors.RED + 'ERROR' + bcolors.ENDC + '] : '

pType = [start, done, success, error]

def log(printType, content):
    print(pType[printType] + content)

class gitlab_manager:
    def __init__(self, access_token, file_path, group_name):
        self.gl = gitlab.Gitlab('https://gitlab.com/', private_token=access_token)
        self.gl.auth()
        self.file_path = file_path
        self.group_name = group_name

    def create_allrepos(self):
        log(0, 'Create Gitlab Repositories')

        self.create_projects()
        self.join_members()
        self.deploy_keys()
        self.check_members_in()

        log(1, 'Create Gitlab Repositories')

    def create_projects(self):
        log(0, 'Create Projects')
        
        teams = open(self.file_path, 'r').readlines()
        
        group_id = self.gl.groups.list(search = self.group_name)[0].id
     
        for team in teams:
            project_name= team[:-1]
            project = self.gl.projects.create({'name': project_name, 'namespace_id': group_id})
            self.create_readme(project)
            self.developer_auth(project, 'master')

        log(1, 'Create Projects')

    def create_readme(self, project):
        content = self.group_name 
        commit_message = 'Initialize'
        project.files.create({'file_path': 'README.md', 'branch': 'master', 'content': content, 'commit_message': commit_message})

    def developer_auth(self, project, branch_name):
        branch = project.branches.get(branch_name)
        branch.protect(developers_can_push=True, developers_can_merge=True)

    def deploy_keys(self):
        log(0, 'Deploy Keys')

        teams = open(self.file_path, 'r').readlines()

        for team in teams:
            project_name = '%s/%s' % (self.group_name, team[:-1])
            print(project_name)
            project = self.gl.projects.get(project_name)

            key = project.keys.create({'title': 'YOUR_TITLE', 'key': open('YOUR_HOME/.ssh/id_rsa.pub').read()})
            key.can_push = True
            project.keys.enable(key.id)

        log(1, 'Deploy Keys')


    def join_members(self):
        log(0, 'Join Members')

        teams = open(self.file_path, 'r').readlines()

        for team in teams:
            students = team[:-1].split('_') 

            for username in students:
                if self.isGitlabMember(username) == False:
                    return

                project_name = '%s/%s' % (self.group_name, team[:-1])
                project = self.gl.projects.get(project_name)

                if self.join_member(project, username) == False:
                    log(3, ('%s didn\'t join the project' % username))
                else:
                    log(2, ('%s join the project' % username))

                # This is for adding another TA to the repository as MASTER's access authorization
                #if self.join_member(project, "TA_Username", access_lv=gitlab.MASTER_ACCESS) == False:
                #    log(3, 'TA didn\'t join the project')
                #else:
                #    log(2, 'TA join the project')

        log(1, 'Join Members')
        
    def join_member(self, project, username, access_lv=gitlab.DEVELOPER_ACCESS):
        members = project.members.list()

        for m in members:
            if m.username == '%s' % username:
                return True

        all_user_list = self.gl.users.list(search = username)

        user_id = -1

        for user in all_user_list:
            if user.username == "%s" % username:
                user_id = user.id

        try:
            member = project.members.create({'user_id': user_id, 'access_level': access_lv})
        except:
            return False

        return True


    def check_members_in(self):
        log(0, 'Check Member In Project')

        teams = open(self.file_path, 'r').readlines()

        for team in teams:
            students = team[:-1].split('_')

            for username in students:
                result = self.check_member_in(username, team[:-1])
                if result == 1:
                    log(2, '%s is in %s' % (username, team[:-1])) 
                elif result == 2:
                    log(3, '%s is NOT in %s' % (username, team[:-1])) 
                elif result == 3:
                    log(3, 'No one here in %s' % (team[:-1])) 
                elif result == 4:
                    log(3, 'No project : %s' % (team[:-1])) 

        log(1, 'Check Member In Project')
        
    def check_member_in(self, username, team_name):
        std_name = username
        project_name = "%s/%s" % (self.group_name, team_name)
        try:
          project = self.gl.projects.get(project_name)
          members = project.members.list()
          mem_len = len(members)

          if mem_len == 0:
            return 3

          for m in members:
            if m.username == "%s" % std_name:
                return 1

        except gitlab.exceptions.GitlabGetError:
           return 4

        return 2

    def isGitlabMember(self, username):
        if self.gl.users.list(search = username):
            log(2, username + ' Found')
        else:
            log(3, username + ' Not found')

access_token = ''
csv_path = ''
group_name = ''

gg = gitlab_manager(access_token, csv_path, group_name)

gg.create_allrepos()
#gg.deploy_keys()
