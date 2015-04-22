import os
import subprocess


ADSM_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# TODO: Change this for os specific stuff
git = '"' + os.path.join(ADSM_DIR, 'src', 'git', 'bin', 'git.exe') + '" '


def update_is_needed():
    print("Checking for updates...")
    try:
        os.chdir(ADSM_DIR)

        command = git + ' rev-parse --abbrev-ref HEAD'
        current_branch = subprocess.check_output(command, shell=True).decode().strip()

        # Go ahead and fetch the current branch
        command = git + ' fetch origin ' + current_branch
        subprocess.call(command, shell=True)

        command = git + ' rev-parse FETCH_HEAD'
        fetched_sha = subprocess.check_output(command, shell=True).decode().strip()
        command = git + ' rev-parse HEAD'
        head_sha = subprocess.check_output(command, shell=True).decode().strip()

        if fetched_sha != head_sha:
            print("An update is required.")
            return True
        print("There are currently no updates.")
        return False
    except:
        print ("Failed in checking if an update is required!")
        return False
    finally:
        os.chdir(os.path.join(ADSM_DIR, 'src'))

    
def reset_and_update_adsm():
    try:
        print("Resetting all files to base state...")

        command = git + ' clean -f'
        subprocess.call(command, shell=True)  # trying to get rid of new files that were added
        
        command = git + ' reset --hard'
        subprocess.call(command, shell=True)
        
        command = git + ' clean -f -d'
        subprocess.call(command, shell=True)
        
        print("Attempting to update files...")
        command = git + ' rev-parse --abbrev-ref HEAD'
        current_branch = subprocess.check_output(command, shell=True).decode().strip()

        # Go ahead and fetch the current branch
        command = git + ' fetch origin ' + current_branch
        subprocess.call(command, shell=True)

        command = git + ' rebase FETCH_HEAD'
        git_status = subprocess.check_output(command, shell=True)

        print("Successfully updated.")
        return True
    except:
        print("Failed to update!")
        try:
            command = git + ' reset --hard'
            subprocess.call(command, shell=True)
        except:
            print("Failed to reset files! You are probably in a bad state.")
        return False


def update_adsm():
    if update_is_needed():
        print("Attempting to update files...")
        try:
            command = git + ' stash'
            subprocess.call(command, shell=True)  # trying to get rid of settings.sqlite3 change
            command = git + ' reset --hard'
            subprocess.call(command, shell=True)

            command = git + ' rebase FETCH_HEAD'
            git_status = subprocess.check_output(command, shell=True)
            # TODO: Make sure the pull actually worked

            print("Successfully updated.")
            return True
        except:
            print("Failed to update!")
            try:
                command = git + ' reset'
                subprocess.call(command, shell=True)
                print("Reset to original state.")
            except:
                print("Failed to gracefully reset to original state!")

            return False
        finally:
            command = git + ' stash apply'
            subprocess.call(command, shell=True)  # TODO: What if the stash apply has a conflict?
    else:
        return True
