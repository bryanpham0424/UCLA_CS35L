import os
import sys
import zlib

# Bryan Pham UID: 105-105-100

# Do a topological sort on a top level .git directory,
# then print the results in a readable format


# Defining the Node class as given in the instructions
class CommitNode:
    def __init__(self, commit_hash):
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# Find the top level .git directory starting at the current directory


def find_git_dir():
    # get the current working directory
    is_git = os.getcwd()
    while is_git != '/':
        if os.path.exists(".git"):
            break
        os.chdir("../")
        is_git = os.getcwd()
    # Reached the beginning of the absolute filepath
    if is_git == '/':
        sys.exit("Not inside a git repository")
    # This line below will give the absolute path,
    # and then leaves us in the .git/refs/heads where all the branches are
    path = ".git/refs/heads"
    git_path = os.path.join(is_git, path)
    return is_git, git_path

# Find the local branch names


def get_local_branch_names():
    # directory and ~/.git/refs/heads
    git_path = find_git_dir()[1]
    os.chdir(git_path)

    # dictionary of local branches
    branches_dict = {}
    for root, dirs, fil in os.walk('.'):
        for curr_file in fil:
            branch_file = os.path.join(root, curr_file)
            hash_val = open(branch_file, 'r').read().strip()
            if hash_val not in branches_dict:
                branches_dict[hash_val] = set()
            branches_dict[hash_val].add(branch_file[2:])

    return branches_dict


def get_parent_commits(git_dir, commit_hash):
    obj_dir = os.path.join(git_dir, '.git/objects/')
    os.chdir(obj_dir)

    parent_commits = set()
    dir_name = commit_hash[0:2]
    sub_folder_name = commit_hash[2:]

    filename = os.path.join(dir_name, sub_folder_name)
    compressed_contents = open(filename, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents).decode()
    decompressed_contents = decompressed_contents.split('\n')
    for decompressed_line in decompressed_contents:
        index = decompressed_line.find('parent')
        if index != -1:
            par_comm = decompressed_line[index+6:].strip()
            parent_commits.add(par_comm)

    return parent_commits

# Create the commit graph


def build_commit_graph(git_dir, local_branch_heads):
    # Dictionary will map the commit hash to the node
    commit_nodes = {}
    # Hash value of the root nodes
    root_hashes = set()
    # contains all visited nodes when traversing the commit graph
    visited = set()

    stack = []
    for key, item in local_branch_heads.items():
        stack.append(key)
    while stack:
        commit_hash = stack.pop()
        if commit_hash not in visited:
            visited.add(commit_hash)
            if commit_hash not in commit_nodes:
                new_commit_node = CommitNode(commit_hash)
                commit_nodes[commit_hash] = new_commit_node
            commit_node = commit_nodes[commit_hash]
            commit_node.parents = get_parent_commits(git_dir, commit_hash)
            if not commit_node.parents:
                root_hashes.add(commit_hash)
            for p_hash in commit_node.parents:
                if p_hash not in visited:
                    stack.append(p_hash)
                if p_hash not in commit_nodes:
                    new_commit_node = CommitNode(p_hash)
                    commit_nodes[p_hash] = new_commit_node
                commit_nodes[p_hash].children.add(commit_hash)

    return commit_nodes, root_hashes

# Topological Sort on all commits using Depth First Search
# Pseudocode was given by the TAs for this function


def get_topo_ordered_commits(commit_nodes, root_hashes):
    order = []
    visited = set()
    temp_stack = []

    stack = sorted(root_hashes)
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            while temp_stack and v not in commit_nodes[temp_stack[-1]].children:
                order.append(temp_stack.pop())

            temp_stack.append(v)
            for child in sorted(commit_nodes[v].children):
                if child not in visited:
                    stack.append(child)
    while temp_stack:
        order.append(temp_stack.pop())

    return order

# This function was given by the TAs


def print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches):
    jumped = False
    for i in range(len(topo_ordered_commits)):
        commit_hash = topo_ordered_commits[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branches = sorted(
            head_to_branches[commit_hash]) if commit_hash in head_to_branches else []
        print(commit_hash + (' ' + ' '.join(branches) if branches else ''))
        if i+1 < len(topo_ordered_commits) and topo_ordered_commits[i+1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')


def topo_order_commits():
    git_dir = find_git_dir()[0]
    local_branch_heads = get_local_branch_names()
    commit_nodes, root_hashes = build_commit_graph(git_dir, local_branch_heads)
    topo_ordered_commits = get_topo_ordered_commits(commit_nodes, root_hashes)
    print_topo_ordered_commits_with_branch_names(
        commit_nodes, topo_ordered_commits, local_branch_heads)


if __name__ == '__main__':
    topo_order_commits()
