import random
import time

class OnePhaseCommit:
    def __init__(self, participants):
        self.participants = participants

    def execute_transaction(self):
        print("\nStarting One-Phase Commit transaction...")
        decision = self.commit_phase()
        if decision:
            print("Transaction committed successfully.")
        else:
            print("Transaction aborted.")

    def commit_phase(self):
        # Coordinator sends transaction to participants and gets their response
        for participant in self.participants:
            time.sleep(0.5)  # Simulate delay
            if not participant.process_transaction():
                return False  # If any participant cannot commit, transaction is aborted
        return True  # If all participants can commit, transaction is committed

class Participant:
    def __init__(self, name):
        self.name = name

    def process_transaction(self):
        # Simulate whether the participant can commit or not
        can_commit = random.choice([True, True, False])  # Higher chance of committing
        if can_commit:
            print(f"Participant {self.name}: Ready to commit.")
            return True
        else:
            print(f"Participant {self.name}: Unable to commit. Aborting...")
            return False

if __name__ == "__main__":
    # Create a list of participants
    participants = [Participant(f"P{i+1}") for i in range(5)]
    
    # Create an instance of OnePhaseCommit
    opc = OnePhaseCommit(participants)
    
    # Execute the transaction
    opc.execute_transaction()
