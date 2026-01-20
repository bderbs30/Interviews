# InterviewExploration
Follow ups for questions I got in interviews (kinda curious you know)


So when I first thought about this problem, my initial instinct was to use a dictionary where the key is the absolute path and the value is the file object. Something like {"/home/user/file.txt": file_obj}.

But then I started thinking about the operations we need to support, specifically listing out files in a directory. If I want to list everything in /home/user/, I'd have to iterate through the entire dictionary and check if each key starts with that prefix. That's O(n) where n is the total number of files in the system. If we have millions of files, that's expensive.
So I thought, how can we reduce the search space? And that's when I realized a tree structure makes way more sense here. If you think about it, file systems are inherently hierarchical, every directory has one parent, and can have multiple children.

The idea is that each directory becomes a node, and it stores its children in a hash map keyed by name. So when I want to list /home/user/, I just traverse down from root to home to user, that's O(d) where d is the path depth, and each hop is O(1) because it's a hash map lookup. Then I just return the children of that node.

For the class design, I used a base Node class with FileNode and DirectoryNode subclasses. Files are leaves, they can't have children. Directories have a children dictionary. I added an is_directory property so we can check the node type without using isinstance, which felt cleaner from a design perspective.

The traversal logic is reused across all operations, add, delete, list, edit, so I extracted it into helper methods. Everything ends up being O(d) for path depth, which is typically pretty small compared to the total number of files.
