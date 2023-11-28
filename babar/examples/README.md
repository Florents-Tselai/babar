The `.py` files in this directory / packages serve both as examples
of usage, and as test cases for babar itself.

Each python file should be a self-contained installable extension.

### `pystring.py` 
A simple extension implemented as a wrapper around Python's 
string functionality. Mainly used to flesh out the API of babar it self.

### `pgllm.py` 

An extension built around the beautiful [llm](https://llm.datasette.io/) library/tool.

This examples requires special llm plugins which you can install like 
```bash
llm install llm-clip
llm embed -m clip -c 'Hello world'
```