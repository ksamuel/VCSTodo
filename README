VCSTODO: a human and VCS friendly text based task manager 

VCSTODO is a CLI program in the same spirit as `Todotxt <http://todotxt.com/>`_ and many others.

It's in dev, unstable, and with absolutly no garanty it currently works or will ever do. It's just something I do as an experiment.

Features
=========

- Add tasks (content, and tags for now)
- List and filter tasks  (by tags, status, then order and limit)
- Mark a task as todo or done

The main benefit of vcstodo compared to the other projects:

- Tags
- (Very) Human friendly task file format
- One file per task, one directory for done tasks, one for todo task: it's designed to be commited in your VCS
- Multiuser suport (weak, but plan to improve)
- Planning for comments

Setup
======

pip install vcstodo

Usage
======

At your project root::

	tdo init

Add a task::

	tdo add "This is a very important task" 
	tdo add "A task with tags" --tags "stuff, that, matters"

List tasks::

	tdo lst
	tdo
	tdo --status done --withtags "stuff"

Mark task as done::

	tdo check 1

1 should be the task number given by `tdo lst`

Mark task as todo::

	tdo uncheck 1

Use --help with any command to learn about options.

Plans
=========

Do not count on it. It's just noted as a reminder for me. The project could die tomorrow.

- options shortcuts
- Comments
- Strong multi user capabilities
- Some commands to edit inline, and with a text editor
- Unit tests
- command completion
- Deep search command, maybe using 
- A plugin architecture with a API
- Git integration using a plugin
- Some UI
