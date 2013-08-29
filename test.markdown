# Introduction

## What Is Rez?
Rez is a suite of tools for resolving a list of ‘packages’ (versioned software) and their dependencies, into an environment that does not contain any version clashes. Rez also includes a cmake-based build system, which is integrated into the package resolution system, and a deployment system, for publishing new packages.

## What Is Rez Not?
Rez is not a production environment management system, it is a package configuration system. To illustrate the difference, consider:

“Package configuration” answers the question, “if I want this set of packages to function within a single environment, what set of packages, environment variables etc do I actually need?”

Whereas “Environment management” answers the question, “What set of packages do I need in this area of production, and how do I manage adding new packages, and updating versions?”

Whilst Rez is not an environment management system, it would make sense to build such a system on top of Rez, and that’s exactly what was done internally at Dr D studios. The environment management system determines what packages are needed where, then this package request is given to the underlying Rez system, which resolves the request into a working environment.

This decoupling allows the user who does not need to be working in a production environment (eg, someone developing core tools) to use only those packages they need. It also guarantees that only valid, non-clashing environments are ever generated.

# Overview
The ‘package resolution algorithm’ is the main component of Rez and is written in python, with supporting tools written in python and bash. It has cmake integration, and comes with a set of cmake modules for building common types of targets, such as python scripts. The python component is written as an API, so we can programmatically manage environment configuration in future.

There are four major tools that make up the system, and a smattering of support tools. They can be thought of as a stack, where the tools at the bottom underpin those at the top:

IMG

This manual will start with the basic concepts of the system, and will illustrate its use in a run-time context. Later chapters will introduce the build system support, and more advanced topics. Tools will be introduced from the bottom of the stack upwards - it is necessary to understand the underpinning tools first, before their dependent tools can be described.

A note on conventions in this document. Blue text like this illustrates commands run on the terminal, command output, or file contents. Green text like this represents file system structures.

# Basic Concepts
Rez manages packages. You request a list of packages from rez-config, and it resolves this request, if possible. If the resolution is not possible, the system can supply you with the relevant information to determine why this is so. You typically want to resolve a list of packages because you want to create an environment in which you can use them in combination, without conflicts occurring. A conflict occurs when there is a request for two or more different versions of the same package - a version clash.

Rez lets you describe the environment you want in a natural way. For example, you can say:

“I want an environment with...”
* “...the latest version of houdini”
* “...maya-2009.1”
* “...the latest rv and the latest maya and houdini-11.something”
* “...rv-3.something or greater”
* “...the latest houdini which works with boost-1.37.0”
* “...PyQt-2.2 or greater, but less than PyQt-4.5.3”

A package is a particular version of a piece of software, or possibly data or configuration information, that resides in a single physical location on disk. The rez system does not distinguish between external and internal software. Some examples of packages include:
* boost-1.33.1
* houdini-11.0.438
* foo-2.9.0
