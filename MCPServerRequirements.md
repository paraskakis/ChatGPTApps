# MCP Server Requirements
The "Emmanuel's Maven Lightning Lessons" MCP Server is meant to be used with ChatGPT and other LLMs or agents to help users discover and view or sign up for a lesson so they can boost their knowledge and career.
Lessons have occurred in the past, marked with the status "On Demand", in which case the user can watch the recording in the provided URL. Or they will happen in the future, in which case the status is "Scheduled" and the user can sign up at the provided URL.
The full description and outcome for each lesson is shown as well as the instructors and guest speakers.
**NOTE:** Use enums where possible and fully describe all parameters.

## Description
A comprehensive list of free, short Lightning Lessons on the Maven education platform by Emmanuel Paraskakis. The topics covered are APIs, MCP, Product Management, Technical PM Careers, and ChatGPT Apps.
Users can either view a recording, sign up for an upcoming live lesson, or learn which cohort-based course is connected to the topic so they can go deeper into it.
Lightning Lessons are conducted over Zoom and are practical and hands-on with skills you can use immediately. They are meant for tech-savvy mid-career professionals, especially those in the technology or software industry. They are conducted exclusively in the English language.
The main Instructor is Emmanuel Paraskakis, an entrepreneur, product management executive, and consultant at Level 250 with over 15 years of experience shaping products.

## Evals
### Golden Prompts
#### Direct Prompts
- Show me all Lightning Lessons by Emmanuel Paraskakis
- I'm searching for live training by Emmanuel Paraskakis
- Lessons on Maven about APIs
- All Maven lessons on MCP
#### Indirect Prompts
- I want to learn about APIs
- I want to know more about API Product Management
- Are there any free short courses on API Products
- How do I learn about MCP
- Video on Application Programming Interface
- Get better at Technical Product Management
- The basics of Model Context Protocol
- Short lesson on how to make ChatGPT Apps
#### Negative Prompts
- How to design a UI
- Learn the basics of Product Management
- Learn how to build apps
- Understand how to use AI
- Learn how to do management
- All the lessons on Maven

## Tools
1. Show information about Lightning Lessons

### Name: `getLessons`
### Description: Use this tool when the user wants to search for short lessons on topics such as APIs, Product Management. DO not use if they are looking for education outside of software, technology, or business. How it works: A user can request a partial text search and a list of lessons that meet the criteria is returned. The full data from each Lightning Lesson is shown. The search takes into account the Title, Description, Outcomes (both Titles and Descriptions), Instructor and Guest names, and Course Name. It should also be able to handle queries like `All` and `Every` gracefully.
### Metadata
#### set `readOnlyHint` to `true`
