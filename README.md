# JackOS-Compiler
JackOS-Compiler
The JackOS-Compiler is a project developed as part of the Nand2Tetris course, which guides learners through building a modern computer system from first principles. This compiler translates high-level Jack programming language code into VM (Virtual Machine) code, serving as an intermediate step before converting to Hack assembly language.

Project Structure
The repository contains the following key components:

code/: Directory housing the source code of the compiler.
README.md: This file, providing an overview and instructions for the project.
Features
Jack to VM Translation: Converts Jack language code into VM code, facilitating further translation to Hack assembly language.
Syntax Analysis: Implements a tokenizer and parser to analyze Jack code syntax.
Symbol Table Management: Manages variable and subroutine declarations and their scopes.
VM Code Generation: Produces VM commands corresponding to the parsed Jack code.
