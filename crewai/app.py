import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "REDACTED"

researcher_llm = LLM(
    model="REDACTED",
    base_url="REDACTED",
    api_key="REDACTED",
    api_version="REDACTED",
    temperature=0,
)
researcher = Agent(
    role="Senior Research Analyst",
    goal="Research cutting edge AI advancements",
    backstory="You work at a tech think tank, analysing AI trends",
    verbose=True,
    tools=[SerperDevTool()],
    llm=researcher_llm,
)

writer_llm = LLM(
    model="REDACTED",
    base_url="REDACTED",
    api_key="REDACTED",
    api_version="REDACTED",
    temperature=0,
)
writer = Agent(
    role="Content strategist",
    goal="Create engaging content from research",
    backstory="You are a skilled writer transforming research into engaging articles",  # noqa E501
    verbose=True,
    llm=writer_llm,
)


task1 = Task(
    description="Analyze AI Advancements during the cold war and provide a detailed report.",  # noqa E501
    expected_output="Research report in bullet points",
    agent=researcher,
)
task2 = Task(
    description="Write a blog post based on the research report",
    expected_output="Write a full blog post (at least 4 paragraphs)",
    agent=writer
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()

print("Final Response:")
print(result)
