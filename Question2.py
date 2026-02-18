class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root):
    max_sum = float('-inf')

    def maxGain(node):
        nonlocal max_sum
        if not node:
            return 0

        left_gain = max(maxGain(node.left), 0)
        right_gain = max(maxGain(node.right), 0)

        current_path = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path)

        return node.val + max(left_gain, right_gain)

    maxGain(root)
    return max_sum

# Run example when file is executed directly
if __name__ == "__main__":
    # Create a sample binary tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)

    # Call function and print result
    result = maxPathSum(root)
    print("Maximum Path Sum:", result)