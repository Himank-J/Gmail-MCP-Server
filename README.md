## Overview

Gmail MCP server - Connecting Gmail and LLM using MCP

## Project

- using functionalities of Gmail applications we create tools to send mail, create draft, mark email as read and more...
- The aim is to to manually convert an LLM into an Agent without using any framework. Using iterative prompting we get our LLM to utilise tools and send email to required receipient

## Demo
[![Watch how Gmail MCP server works](https://img.youtube.com/vi/QLJ6gHT2mnI/0.jpg)](https://www.youtube.com/watch?v=QLJ6gHT2mnI)

## Code Details

[MCP Server](mcp_server_gmail.py)

This is the server file that enlists all the tools that our LLM can use. Below is the main code that opens FreeForm app, creates a rectangle and adds text inside it.

[MCP Client](mcp_client_gmail.py)

This is the client file that uses MCP to send the query to the server.
