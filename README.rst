==========================
 Socket Reuse Experiments
==========================

These are experiments for re-using a socket between processes in
Python.

There are times where you want to take an address (host and port) and
share that with multiple processes. For example, `Circus
<https://circus.readthedocs.org/en/latest/for-ops/sockets/#sockets>`_
is a tool that allows you to create a socket and pass the file
descriptor to other processes, that can use that descriptor to use the
socket. When this happens, the operating system will select a process
to handle messages on the socket.

Sockets can also reuse an address (http://linux.die.net/man/7/socket
SO_REUSEADDR) that has already been binded to, assuming the other
process or thread uses the same `SO_REUSEADDR` settings as the
original binding process and process uses the same user ID. It should
also be noted, this is a feature specific to linux. `LWN
<https://lwn.net>`_ has an `excellent discussion
<https://lwn.net/Articles/542629/>`_ of the topic.
