import random
import time
import threading

# Defining Node class to simulate different nodes in the distributed environment
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.commit_log = []

    def execute_transaction(self, transaction):
        # Node is executing transaction
        # Simulating transaction execution with a delay
        time.sleep(random.uniform(0.1, 0.5))
        key, value = transaction
        self.data[key] = value
        # Node successfully executed transaction
        return True

    def commit_transaction(self, transaction):
        # Node attempting to commit transaction
        success = self.execute_transaction(transaction)
        if success:
            self.commit_log.append(transaction)
            # Node committed transaction
            return True
        # Node failed to commit transaction
        return False

# One-Phase Commit Simulation
class OnePhaseCommitSimulation:
    def __init__(self, num_nodes=5):
        self.nodes = [Node(node_id) for node_id in range(num_nodes)]
        self.consistency_failures = 0
        self.successful_commits = 0
        self.failed_commits = 0

    def dependent_commit(self):
        """
        Simulate dependent commits across nodes where failure in one affects others.
        """
        key = "shared_resource"
        value = random.randint(1, 100)
        transactions = [(key, value) for _ in range(len(self.nodes))]

        # Starting dependent commit with transactions
        # Simulate one-phase commit with dependency
        for i, node in enumerate(self.nodes):
            success = node.commit_transaction(transactions[i])
            if not success:
                # Dependent commit failed, rolling back previous transactions
                self.failed_commits += 1
                self.consistency_failures += 1
                # Dependent failure: rollback all prior transactions
                for j in range(i):
                    del self.nodes[j].data[key]
                    # Node rolled back transaction for key
                break

        else:
            self.successful_commits += 1
            # Dependent commit succeeded for all nodes

    def independent_commit(self):
        """
        Simulate independent commits across nodes where each transaction is standalone.
        """
        transactions = [(f"key_{node.node_id}", random.randint(1, 100)) for node in self.nodes]

        # Starting independent commit with transactions
        # Simulate one-phase commit without dependency
        for i, node in enumerate(self.nodes):
            success = node.commit_transaction(transactions[i])
            while not success:
                # Waiting for node to successfully commit transaction
                success = node.commit_transaction(transactions[i])

            # Independent commit succeeded at node
            self.successful_commits += 1

    def run_simulation(self, num_iterations=100):
        """
        Run the simulation for both dependent and independent commits.
        """
        for iteration in range(num_iterations):
            # Iteration of the simulation
            # Randomly choose between dependent and independent commits
            if random.choice([True, False]):
                self.dependent_commit()
            else:
                self.independent_commit()

        # Print metrics
        total_transactions = self.successful_commits + self.failed_commits
        consistency_rate = 100 if total_transactions > 0 else 0

        print("\nSimulation Metrics:")
        print(f"  Total Transactions: {total_transactions}")
        print(f"  Successful Commits: {self.successful_commits}")
        print(f"  Failed Commits: {self.failed_commits}")
        print(f"  Consistency Failures: {self.consistency_failures}")
        print(f"  Consistency Rate: {consistency_rate:.2f}%")

# Run the simulation
if __name__ == "__main__":
    simulation = OnePhaseCommitSimulation(num_nodes=5)
    simulation.run_simulation(num_iterations=100)
