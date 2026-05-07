from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from project_flow.tools.tool_helmet_detection import tool_helmet_detection
from project_flow.tools.tool_report_db import tool_report_dbInput, tool_report_db
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class HelmetDetector():
    """HelmetDetector crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def helmet_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['helmet_detector'], # type: ignore[index]
            verbose=True,
            tools=[tool_helmet_detection()] # Adding the helmet detection tool to the agent
        )

    @agent
    def agent_helmet_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_helmet_analyzer'], # type: ignore[index]
            max_iter=3,
            verbose=True,
            tools=[tool_report_db()] # Adding the report database tool to the agent
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def helmet_detector_task(self) -> Task:
        return Task(
            config=self.tasks_config['helmet_detector_task'], # type: ignore[index]
            output_json= tool_report_dbInput
        )
    
    @task
    def task_helmet_analyzer(self) -> Task:
        return Task(
            config=self.tasks_config['task_helmet_analyzer'] # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the HelmetDetector crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
