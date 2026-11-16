class VacuumAgent:
    def __init__(self, start_location="A"):
        self.location = start_location

    def act(self, environment):
        current_status = environment[self.location]
        print(f"\n[Agent Status] Location: {self.location} | Status: {current_status}")

        if current_status == "Dirty":
            print(f"-> Action: SUCK (Cleaning {self.location}...)")
            environment[self.location] = "Clean"
        elif self.location == "A":
            print("-> Action: MOVE RIGHT (Moving to Room B)")
            self.location = "B"
        elif self.location == "B":
            print("-> Action: MOVE LEFT (Moving to Room A)")
            self.location = "A"


def run_simulation(steps=4):
    environment = {"A": "Dirty", "B": "Dirty"}
    agent = VacuumAgent(start_location="A")
    
    print("Initial Environment State:", environment)
    
    for step in range(1, steps + 1):
        print(f"\n--- Time Step {step} ---")
        agent.act(environment)
        print("Current Environment State:", environment)

    if environment["A"] == "Clean" and environment["B"] == "Clean":
        print("\n Goal State Achieved: Both rooms are completely clean!")
    else:
        print("\n Simulation ended before both rooms were cleaned.")


if __name__ == "__main__":
    run_simulation()
