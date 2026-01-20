# InterviewExploration
Follow-ups for questions I got in interviews (kinda curious, you know)


## Filesystem 

So when I first thought about this problem, my initial instinct was to use a dictionary where the key is the absolute path and the value is the file object. Something like {"/home/user/file.txt": file_obj}.

But then I started thinking about the operations we need to support, specifically listing out files in a directory. If I want to list everything in /home/user/, I'd have to iterate through the entire dictionary and check if each key starts with that prefix. That's O(n), where n is the total number of files in the system. If we have millions of files, that's expensive.
So I thought, how can we reduce the search space? And that's when I realized a tree structure makes way more sense here. If you think about it, file systems are inherently hierarchical; every directory has one parent and can have multiple children.

The idea is that each directory becomes a node, and it stores its children in a hash map keyed by name. So when I want to list /home/user/, I just traverse down from root to home to user, that's O(d) where d is the path depth, and each hop is O(1) because it's a hash map lookup. Then I just return the children of that node.

For the class design, I used a base Node class with FileNode and DirectoryNode subclasses. Files are leaves; they can't have children. Directories have a children's dictionary. I added an is_directory property so we can check the node type without using isinstance, which felt cleaner from a design perspective.

The traversal logic is reused across all operations, add, delete, list, and edit, so I extracted it into helper methods. Everything ends up being O(d) for path depth, which is typically pretty small compared to the total number of files.


## Secured Linked List

We want to create a secure linked list that has a hashvalue. Similar to regular linked lists, we'll have the node value and the next pointer (where the next pointer points to the next node in the list)


python
```
class Node:

def __init__(value: str, next: Node):
    self.value = value
    self.next = next

```

We want to add a field called hash_value containing the hash for the current node. We can assume there is a helper function called calc_hash(input: str)


The hash value is calculated in two ways
1. If the next pointer is None, the hash value = calc_hash(node.val)
2. If the next pointer isn't None, the hash value = calc_hash(node.val + str(node.next.hash_value))

We want to implement two functions

def add(value: str) 

Add a value to the head of the linked list

def is_valid_chain(): -> bool

Validate the entire chain according to the conditions of how a hash should be computed 


These were the two functions that were proposed during the interview - I've thought of two more that we can do



def remove(index):


remove the node at the index value from the linkedlist


Approach:
For this method, we'll need to recompute the hash for all nodes up until the node we're removing. We also need to relink after we remove the node


def insert(index, value):

Approach:
Similar to remove we'll need to recompute the preceding nodes in the linked list up until the index we just inserted the node at - we'll also need to modify the points surrounding 
The node we just inserted to relink the node properly











