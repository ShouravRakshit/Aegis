from .example_agent import *
from collections import defaultdict

class LeaderAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survivor_locations = defaultdict(list)

    @override
    def handle_message(self, smr: SEND_MESSAGE_RESULT) -> None:
        super().handle_message(smr)
        if "Survivor location:" in smr.msg:
            survivor_location = smr.msg.split("Survivor location:")[-1].split(";")[0].strip()
            self.survivor_locations[survivor_location].append(smr.from_agent_id)
            self.assign_agents_to_survivors()

    def assign_agents_to_survivors(self):
        assignments = defaultdict(list)
        for location, agents in self.survivor_locations.items():
            for i, agent_id in enumerate(agents):
                assignments[agent_id].append(location)
                if len(assignments[agent_id]) >= 2:
                    break

        for agent_id, locations in assignments.items():
            message = f"Assigned survivor locations: {', '.join(locations)}"
            self._agent.send(SEND_MESSAGE([agent_id], message))
            BaseAgent.log(LogLevels.Always, f"Message sent to {agent_id}: {message}")

    @override
    def think(self) -> None:
        BaseAgent.log(LogLevels.Always, "Leader thinking")
        # Leader specific thinking logic can be added here
        pass
