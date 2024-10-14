import random
import time
import threading
import socket

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
        if random.random() < 0.1:  # Simulating a random failure
            return False  # Failure flag
        time.sleep(random.uniform(0.1, 0.5))
        key, value = transaction
        self.data[key] = value
        # Node successfully executed transaction
        return True

    def prepare_transaction(self, transaction):
        # Node preparing to commit transaction
        # Simulate preparation phase
        if random.random() < 0.1:  # Simulating a random failure
            return False  # Failure flag
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

# Defining Coordinator Node class to manage the two-phase commit
class CoordinatorNode(Node):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.participants = []

    def add_participant(self, node):
        self.participants.append(node)

    def two_phase_commit(self, transaction):
        # Phase 1: Prepare
        all_prepared = True
        for participant in self.participants:
            if not participant.prepare_transaction(transaction):
                all_prepared = False
                # Rollback all participants if any participant fails to prepare
                for rollback_node in self.participants:
                    rollback_node.rollback_transaction(transaction)
                return False

        # Phase 2: Commit
        if all_prepared:
            for participant in self.participants:
                if not participant.commit_transaction(transaction):
                    # If any participant fails to commit, rollback all participants
                    for rollback_node in self.participants:
                        rollback_node.rollback_transaction(transaction)
                    return False

        return True

# Two-Phase Commit Simulation
class TwoPhaseCommitSimulation:
    def __init__(self, num_nodes=5):
        self.coordinator = CoordinatorNode(node_id="Coordinator")
        self.nodes = [Node(node_id) for node_id in range(num_nodes)]
        for node in self.nodes:
            self.coordinator.add_participant(node)
        self.consistency_failures = 0
        self.successful_commits = 0
        self.failed_commits = 0

    def dependent_commit(self):
        """
        Simulate dependent commits across nodes where failure in one affects others.
        """
        key = "shared_resource"
        value = random.randint(1, 100)
        transaction = (key, value)

        # Simulate network failure by randomly deciding if the coordinator can reach participants
        if random.random() < 0.1:
            # Network failure: Coordinator cannot reach participants
            self.failed_commits += 1
            self.consistency_failures += 1
            return

        # Starting dependent commit with coordinator managing the process
        success = self.coordinator.two_phase_commit(transaction)
        if success:
            self.successful_commits += 1
        else:
            self.failed_commits += 1
            self.consistency_failures += 1

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
