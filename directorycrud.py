import os


class DirectoryNode:
    def __init__(self, name, is_folder=True):
        self.name = name
        self.is_folder = is_folder
        self.subdirectory = []


def create_directory(config):
    root = DirectoryNode(config["name"], True)
    create_subdirectory(root, config["contents"])
    return root


def create_subdirectory(parent_node, subdirectory_config):
    for child_config in subdirectory_config:
        child_name = child_config["name"]
        is_folder = child_config.get("is_folder", True)
        child_node = DirectoryNode(child_name, is_folder)
        parent_node.subdirectory.append(child_node)

        if is_folder:
            create_subdirectory(child_node, child_config["contents"])


def add_folder(root_node, path, folder_name):
    path_parts = path.split("/")
    current_node = root_node
    for part in path_parts:
        current_node = find_child_node_by_name(current_node, part)

        if current_node is None:
            return

    new_folder_node = DirectoryNode(folder_name)
    current_node.subdirectory.append(new_folder_node)


def remove_folder(root_node, path):
    path_parts = path.split("/")
    parent_node = None
    current_node = root_node

    for part in path_parts:
        parent_node = current_node
        current_node = find_child_node_by_name(current_node, part)

        if current_node is None:
            return

    if current_node.is_folder:
        parent_node.subdirectory.remove(current_node)
    else:
        print(f"Error: '{path}' is not a folder.")


def find_child_node_by_name(node, name):
    if node.name == name:
        return node
    for child in node.subdirectory:
        if child.name == name:
            return child
    return None


def find_folder_path(root_node, folder_name, current_path=""):
    if (current_path+root_node.name == folder_name or root_node.name == folder_name) and root_node.is_folder:
        return current_path + root_node.name

    for child in root_node.subdirectory:
        if child.is_folder:
            folder_path = find_folder_path(
                child, folder_name, current_path + root_node.name + "/"
            )
            if folder_path:
                return folder_path

    return None

def update_folder_name(root_node, old_name, new_name):
    folder_path = find_folder_path(root_node, old_name)
    if folder_path:
        folder_path_parts = folder_path.split("/")
        current_node = root_node

        for part in folder_path_parts:
            current_node = find_child_node_by_name(current_node, part)

        current_node.name = new_name
        print(f"Updated folder name from '{old_name}' to '{new_name}'.")
    else:
        print(f"Folder '{old_name}' not found in the directory tree.")


def print_directory_structure(node, indentation=""):
    print(indentation + node.name + ("/" if node.is_folder else ""))
    for child in node.subdirectory:
        print_directory_structure(child, indentation + "  ")

directory_info = {
    "name": "root",
    "contents": [
        {
            "name": "folder1",
            "is_folder": True,
            "contents": [
                {
                    "name": "file1.txt",
                    "is_folder": False
                },
                {
                    "name": "file2.txt",
                    "is_folder": False
                }
            ]
        },
        {
            "name": "folder2",
            "is_folder": True,
            "contents": [
                {
                    "name": "folder1",
                    "is_folder": True,
                    "contents": [
                        {
                            "name": "file3.txt",
                            "is_folder": False
                        }
                    ]
                }
            ]
        }
    ]
}

root = create_directory(directory_info)
print_directory_structure(root)

# Add a new folder
add_folder(root, "root/folder1", "new_folder")
print("After adding a new folder:")
print_directory_structure(root)


# Remove a folder
remove_folder(root, "root/folder2/subfolder1")
print("After removing a folder:")
print_directory_structure(root)


# Fetch the path of a folder
path = find_folder_path(root, "folder1")
print(f"The path of 'folder1' is: {path}")


# Update the name of a folder
update_folder_name(root, "root/folder1", "renamed_folder")
print("After updating the name of a folder:")
print_directory_structure(root)