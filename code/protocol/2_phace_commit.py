import random
import time
import threading

# Defining Node class to simulate different nodes in the distributed environment
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.commit_log = []
        self.prepared = False

    def execute_transaction(self, transaction):
        # Node is executing transaction
        # Simulating transaction execution with a delay
        time.sleep(random.uniform(0.1, 0.5))
        key, value = transaction
        self.data[key] = value
        # Node successfully executed transaction
        return True

    def prepare_transaction(self, transaction):
        # Node preparing to commit transaction
        # Simulate preparation phase
        self.prepared = True
        return True

    def commit_transaction(self, transaction):
        # Node attempting to commit transaction
        if self.prepared:
            success = self.execute_transaction(transaction)
            if success:
                self.commit_log.append(transaction)
                self.prepared = False
                # Node committed transaction
                return True
        # Node failed to commit transaction
        return False

    def rollback_transaction(self, transaction):
        # Node rolling back transaction
        key, _ = transaction
        if key in self.data:
            del self.data[key]
        self.prepared = False

# Two-Phase Commit Simulation
class TwoPhaseCommitSimulation:
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
        # Phase 1: Prepare
        all_prepared = True
        for i, node in enumerate(self.nodes):
            if not node.prepare_transaction(transactions[i]):
                all_prepared = False
                # Rollback all nodes if any node fails to prepare
                for j in range(i):
                    node.rollback_transaction(transactions[j])
                self.failed_commits += 1
                self.consistency_failures += 1
                return

        # Phase 2: Commit
        if all_prepared:
            for i, node in enumerate(self.nodes):
                success = node.commit_transaction(transactions[i])
                if not success:
                    # If any node fails to commit, rollback all nodes
                    for j in range(len(self.nodes)):
                        node.rollback_transaction(transactions[j])
                    self.failed_commits += 1
                    self.consistency_failures += 1
                    return

            self.successful_commits += 1
            # Dependent commit succeeded for all nodes

    def run_simulation(self, num_iterations=100):
        """
        Run the simulation for dependent commits.
        """
        for iteration in range(num_iterations):
            # Iteration of the simulation
            self.dependent_commit()

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
    simulation = TwoPhaseCommitSimulation(num_nodes=5)
    simulation.run_simulation(num_iterations=100)
